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


def compile_and_report(xelatex, texfile):
    stem = os.path.splitext(texfile)[0]
    logf = stem + '.log'
    for junk in ['.aux', '.log', '.out', '.toc', '.pdf']:
        p = stem + junk
        if os.path.exists(p):
            os.remove(p)
    cwd = os.path.dirname(os.path.abspath(texfile))
    for _ in range(2):
        subprocess.run([xelatex, '-interaction=nonstopmode',
                        os.path.basename(texfile)],
                       cwd=cwd, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
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
    return dict(overfull=of, missing=mc, errors=er, pages=pages, errmsgs=errs[:5])


def main():
    if sys.argv[1:]:
        targets = sys.argv[1:]
    elif os.path.isdir(TEMPLATE_DIR):
        targets = sorted(f for f in os.listdir(TEMPLATE_DIR)
                         if f.endswith('.tex'))
    else:
        targets = []
    if not targets:
        print('没有找到 .tex 文件（请放在 template/ 目录下）')
        return

    xelatex = find_xelatex()
    if not xelatex:
        print('找不到 xelatex，只能做静态检查')
    else:
        print('xelatex:', xelatex)
    print()

    allok = True
    for t in targets:
        path = t if os.path.isabs(t) else os.path.join(TEMPLATE_DIR, t)
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
                      and r['errors'] == 0)
                if not ok:
                    allok = False
                tag = 'PASS' if ok else 'FAIL'
                print(f"  编译: [{tag}] Overfull={r['overfull']} "
                      f"Missing={r['missing']} Error={r['errors']} "
                      f"页数={r['pages']}")
                for e in r['errmsgs']:
                    print('    ', e)
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
