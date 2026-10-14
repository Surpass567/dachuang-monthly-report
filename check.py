# -*- coding: utf-8 -*-
"""
模板自检脚本 —— 改完 .tex 或 .cls 后跑一遍
用法：
    python check.py                  # 检查当前目录所有 .tex
    python check.py 某个文件.tex
"""
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(HERE, 'template')   # .tex 与 .cls 都放这里


def find_xelatex():
    cands = [
        r'D:\soft\texlive\2026\bin\windows\xelatex.exe',
        shutil.which('xelatex'),
        r'C:\texlive\2025\bin\windows\xelatex.exe',
        r'C:\texlive\2024\bin\windows\xelatex.exe',
    ]
    for c in cands:
        if c and os.path.exists(c):
            return c
    return None


def check_braces(path):
    """括号平衡 + \newenvironment 参数组检查"""
    tex = open(path, encoding='utf-8').read()
    lines = []
    for ln in tex.split('\n'):
        out, i = [], 0
        while i < len(ln):
            if ln[i] == '%' and (i == 0 or ln[i - 1] != '\\'):
                break
            out.append(ln[i]); i += 1
        lines.append(''.join(out))
    body = '\n'.join(lines)

    problems = []
    depth = 0
    for n, ln in enumerate(body.split('\n'), 1):
        for ch in ln:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth < 0:
                    problems.append(f'第{n}行 多余的右括号')
                    depth = 0
    if depth != 0:
        problems.append(f'有 {depth} 个左括号未闭合')

    # \newenvironment 必须有两个参数组
    for m in re.finditer(r'\\newenvironment\*?\{([^}]*)\}', body):
        rest = body[m.end():m.end() + 600]
        d = 0; groups = 0; i = 0; started = False
        while i < len(rest):
            if rest[i] == '{':
                d += 1; started = True
            elif rest[i] == '}':
                d -= 1
                if started and d == 0:
                    groups += 1
                    started = False
                    if groups == 2:
                        break
            i += 1
        if groups < 2:
            ln = body[:m.start()].count('\n') + 1
            problems.append(f'第{ln}行 \\newenvironment{{{m.group(1)}}} 只找到 {groups} 个参数组（应为 2）')

    return problems


def check_refs(path):
    """
    检查交叉引用：
      ① ref 指向的 label 不存在  -> PDF 里会显示两个问号
      ② 手写的章节号（§2.2 这种）  -> 一旦增删章节就会错位
      ③ 图片文件不存在
    """
    tex = open(path, encoding='utf-8').read()
    # 去注释
    lines = []
    for ln in tex.split('\n'):
        out, i = [], 0
        while i < len(ln):
            if ln[i] == '%' and (i == 0 or ln[i - 1] != '\\'):
                break
            out.append(ln[i]); i += 1
        lines.append(''.join(out))
    body = '\n'.join(lines)

    problems = []
    labels = set(re.findall(r'\\label\{([^}]+)\}', body))
    refs = {}
    for m in re.finditer(r'\\(?:ref|eqref|autoref)\{([^}]+)\}', body):
        ln = body[:m.start()].count('\n') + 1
        refs.setdefault(m.group(1), ln)

    # ① 悬空引用
    for name, ln in sorted(refs.items(), key=lambda x: x[1]):
        if name not in labels:
            problems.append(
                f'第{ln}行 \\ref{{{name}}} 没有对应的 \\label —— '
                f'PDF 里会显示「??」，请补 \\label{{{name}}}')

    # 未被引用的标签（提醒，不算错误）
    unused = sorted(labels - set(refs))

    # ② 手写章节号
    for m in re.finditer(r'§\s*(\d+(?:\.\d+)*)', body):
        ln = body[:m.start()].count('\n') + 1
        problems.append(
            f'第{ln}行 手写章节号「§{m.group(1)}」—— '
            f'请改用 \\ref{{标签}}，否则增删章节后会错位')

    # ③ 图片文件
    base = os.path.dirname(os.path.abspath(path))
    for m in re.finditer(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', body):
        img = m.group(1).strip()
        if not os.path.exists(os.path.join(base, img)):
            ln = body[:m.start()].count('\n') + 1
            problems.append(f'第{ln}行 图片不存在: {img}')

    return problems, unused


def compile_and_report(xelatex, texfile):
    stem = os.path.splitext(texfile)[0]
    logf = stem + '.log'
    for junk in ['.aux', '.log', '.out', '.toc', '.pdf']:
        p = stem + junk
        if os.path.exists(p):
            os.remove(p)
    cwd = os.path.dirname(os.path.abspath(texfile))

    # 确保 .cls 与被检查文件同目录（报告放在 reports/ 时也要能找到）
    cls_src = os.path.join(TEMPLATE_DIR, 'ydzjreport.cls')
    cls_dst = os.path.join(cwd, 'ydzjreport.cls')
    copied = False
    if os.path.exists(cls_src) and \
            os.path.abspath(cls_src) != os.path.abspath(cls_dst):
        if not os.path.exists(cls_dst):
            import shutil
            shutil.copy(cls_src, cls_dst)
            copied = True

    for _ in range(3):          # 跑 3 遍，保证交叉引用与浮动体收敛
        subprocess.run([xelatex, '-interaction=nonstopmode',
                        os.path.basename(texfile)],
                       cwd=cwd, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)

    if copied and os.path.exists(cls_dst):
        os.remove(cls_dst)      # 清理临时拷贝

    if not os.path.exists(os.path.join(cwd, os.path.basename(logf))):
        return None
    raw = open(os.path.join(cwd, os.path.basename(logf)),
               encoding='utf-8', errors='replace').read()
    of = len(re.findall(r'Overfull \\hbox', raw))
    mc = len(re.findall(r'Missing character', raw))
    er = len(re.findall(r'(?m)^! ', raw))
    pages = ''
    m = re.search(r'Output written on .*?\((\d+) page', raw)
    if m:
        pages = m.group(1)
    errs = re.findall(r'(?m)^! .{0,90}', raw)

    # 编译日志里的「未定义引用」警告（比源码检查更权威）
    undef = re.findall(r'LaTeX Warning: Reference `([^\']*)\' on page (\d+) undefined', raw)
    if not undef:
        undef = re.findall(r'LaTeX Warning: There were undefined references', raw)

    return dict(overfull=of, missing=mc, errors=er, pages=pages,
                errmsgs=errs[:5], undef=undef)


def main():
    if sys.argv[1:]:
        targets = sys.argv[1:]
    else:
        # 递归扫描 template/、reports/、examples/ 下的所有 .tex
        targets = []
        for sub in ('template', 'reports', 'examples'):
            d = os.path.join(HERE, sub)
            if os.path.isdir(d):
                for f in sorted(os.listdir(d)):
                    if f.endswith('.tex'):
                        targets.append(os.path.join(d, f))
    if not targets:
        print('没有找到 .tex 文件（放在 template/ reports/ examples/ 下）')
        return

    xelatex = find_xelatex()
    if not xelatex:
        print('找不到 xelatex，只能做静态检查')
    else:
        print('xelatex:', xelatex)
    print()

    allok = True
    for t in targets:
        path = t if os.path.isabs(t) else os.path.join(HERE, t)
        if not os.path.exists(path):
            print(f'[跳过] 文件不存在: {t}')
            continue
        print('=' * 66)
        print(os.path.basename(path))
        print('=' * 66)

        probs = check_braces(path)
        if probs:
            allok = False
            print('  括号检查: 有问题')
            for p in probs:
                print('    -', p)
        else:
            print('  括号检查: 通过')

        # 交叉引用检查（防 ?? 与手写章节号）
        rprobs, unused = check_refs(path)
        if rprobs:
            allok = False
            print('  引用检查: 有问题')
            for p in rprobs:
                print('    -', p)
        else:
            print('  引用检查: 通过')
        if unused:
            print('    提示: 这些 \\label 没有被引用 -> %s' % ', '.join(unused))

        cls = os.path.join(TEMPLATE_DIR, 'ydzjreport.cls')
        if os.path.exists(cls):
            cp = check_braces(cls)
            if cp:
                allok = False
                print('  ydzjreport.cls: 有问题')
                for p in cp:
                    print('    -', p)

        if xelatex:
            r = compile_and_report(xelatex, path)
            if r is None:
                allok = False
                print('  编译: 失败（无日志）')
            else:
                ok = (r['overfull'] == 0 and r['missing'] == 0
                      and r['errors'] == 0 and not r['undef'])
                if not ok:
                    allok = False
                tag = 'PASS' if ok else 'FAIL'
                print(f"  编译: [{tag}] Overfull={r['overfull']} "
                      f"Missing={r['missing']} Error={r['errors']} "
                      f"页数={r['pages']}")
                for e in r['errmsgs']:
                    print('    ', e)
                if r['undef']:
                    print('    ! 编译日志里有未定义引用（PDF 会显示 ??）:')
                    for u in r['undef'][:5]:
                        if isinstance(u, tuple):
                            print('        \\ref{%s} 在第 %s 页未定义' % u)
                        else:
                            print('        ', u)
        print()

    print('=' * 66)
    print('总结:', '全部通过' if allok else '存在问题，见上文')
    print('=' * 66)
    print()
    print('提交前还要人工核对：')
    print('  [ ] 数字与单位之间有空格（2.8 mm）')
    print('  [ ] 没有 emoji / 圈号')
    print('  [ ] 表格不超过 6 列')
    print('  [ ] 图表都被正文引用')
    print('  [ ] 阶段一：有复现的环境+步骤+结果')
    print('  [ ] 阶段二：「与预期的差异」「尚不能确定的」非空')


if __name__ == '__main__':
    main()
