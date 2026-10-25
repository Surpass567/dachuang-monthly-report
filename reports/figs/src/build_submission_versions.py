"""Generate submission text and separately numbered figure/table attachments."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

import fitz

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / '提交版本'
WORK = Path(__file__).resolve().parent / 'submission_build'
COMPILER = Path(os.environ['LOCALAPPDATA']) / 'LaTeXPortable' / 'compile.ps1'


def compile_tex(source, outdir, cached=False):
    outdir.mkdir(parents=True, exist_ok=True)
    pdf = outdir / source.with_suffix('.pdf').name
    if not (cached and pdf.exists() and pdf.with_suffix('.log').exists()):
        with (outdir / (source.stem + '_compile.txt')).open('w', encoding='utf-8') as log:
            result = subprocess.run(['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass',
                                     '-File', str(COMPILER), '-Source', str(source),
                                     '-OutDir', str(outdir), '-Offline'],
                                    cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        assert result.returncode == 0, str(source)
    raw = pdf.with_suffix('.log').read_text(encoding='utf-8', errors='replace')
    counts = {key: len(re.findall(pattern, raw)) for key, pattern in {
        'overfull': r'Overfull', 'missing': r'Missing character', 'errors': r'(?m)^! ',
        'undefined': r'(?:Reference .* undefined|There were undefined references|Citation .* undefined)',
    }.items()}
    assert not any(counts.values()), (source, counts)
    return pdf, counts


def group(text, pos):
    while text[pos].isspace():
        pos += 1
    assert text[pos] == '{', text[pos:pos+50]
    start = pos + 1
    depth = 1
    pos += 1
    while depth:
        if text[pos] == '{' and text[pos-1] != '\\':
            depth += 1
        elif text[pos] == '}' and text[pos-1] != '\\':
            depth -= 1
        pos += 1
    return text[start:pos-1], pos


def uncomment(text):
    return re.sub(r'(?m)(?<!\\)%[^\n]*', lambda m: ' ' * len(m[0]), text)


def extract_blocks(body, midterm):
    scan = uncomment(body)
    pattern = re.compile(r'\\begin\{(figure\*?|table\*?|longtable)\}|\\reportfigure(?=\{)')
    blocks = []
    cursor = 0
    counters = {}
    while match := pattern.search(scan, cursor):
        if match[1]:
            env = match[1]
            end = scan.index('\\end{' + env + '}', match.end()) + len('\\end{' + env + '}')
            kind = 'figure' if env.startswith('figure') else 'table'
        else:
            end = match.end()
            args = []
            for _ in range(4):
                arg, end = group(body, end)
                args.append(arg)
            kind = 'figure'
        section = len(re.findall(r'\\section\s*\{', scan[:match.start()]))
        key = (section if midterm else 0, kind)
        counters[key] = counters.get(key, 0) + 1
        number = (f'{section}-' if midterm else '') + str(counters[key])
        raw = body[match.start():end]
        labels = re.findall(r'\\label\{([^}]+)\}', uncomment(raw))
        if not match[1]:
            labels.append(args[0])
        blocks.append(dict(start=match.start(), end=end, raw=raw, kind=kind,
                           number=number, section=section, index=counters[key], labels=labels))
        cursor = end
    return blocks


def main():
    summary = []
    mapping = []
    sources = sorted(ROOT.glob('逻辑月*.tex')) + [ROOT / '中期报告.tex']
    for source in sources:
        midterm = source.stem == '中期报告'
        original_aux = (WORK / 'original' if midterm else ROOT / 'build-latex') / source.with_suffix('.aux').name
        if not original_aux.exists():
            compile_tex(source, original_aux.parent)
        aux = original_aux.read_text(encoding='utf-8')
        label_numbers = dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}', aux))
        original = source.read_text(encoding='utf-8')
        preamble, body = original.split('\\begin{document}', 1)
        body = body.rsplit('\\end{document}', 1)[0]
        blocks = extract_blocks(body, midterm)
        imported = []
        cursor = 0
        chunks = []
        attachments = []
        for block in blocks:
            kind = '图' if block['kind'] == 'figure' else '表'
            number = block['number']
            for label in block['labels']:
                assert label in label_numbers, (source.name, label)
                value = label_numbers[label]
                assert value == number or re.fullmatch(re.escape(number) + r'[a-z]', value), (label, value, number)
                imported.append('\\begingroup\\submissionnumber{' + value + '}\\phantomsection\\label{' + label + '}\\endgroup ')
            chunks.append(body[cursor:block['start']])
            labels = ''.join(imported[-len(block['labels']):]) if block['labels'] else ''
            chunks.append('\n\\par\\noindent ' + labels + f'{kind}~{number} 请参见附件{kind}~{number}。\\par\n')
            cursor = block['end']
            reset = f'\\setcounter{{section}}{{{block["section"]}}}\n' if midterm else ''
            reset += f'\\setcounter{{{block["kind"]}}}{{{block["index"]-1}}}\n'
            attachments.append(reset + block['raw'] + '\n\\clearpage\n')
            mapping.append({'report': source.stem, 'type': kind, 'number': number,
                            'labels': {key: label_numbers[key] for key in block['labels']}})
        chunks.append(body[cursor:])
        helper = '\n\\makeatletter\n\\newcommand{\\submissionnumber}[1]{\\def\\@currentlabel{#1}}\n\\makeatother\n'
        text_body = re.sub(r'\\[Nn]eedspace\{[^}]*\}|\\FloatBarrier', '', ''.join(chunks))
        text_source = preamble + helper + '\\begin{document}\n' + text_body + '\\end{document}\n'
        assert not re.search(r'\\(?:includegraphics|reportfigure)|\\begin\{(?:figure|table|longtable|tabular)', uncomment(''.join(chunks)))
        # Attachment cross-references to the full report retain their original values.
        attachment_labels = {label for b in blocks for label in b['labels']}
        snapshots = []
        for line in aux.splitlines():
            if match := re.match(r'\\newlabel\{([^}]+)\}', line):
                if match[1] not in attachment_labels:
                    snapshots.append(line)
        bib = re.search(r'\\begin\{thebibliography\}.*?\\end\{thebibliography\}', body, re.S)
        appendix_source = (preamble + '\n' + '\n'.join(snapshots) + '\n\\begin{document}\n'
                           + '\\section*{' + source.stem.replace('_', '\\_') + '：图表附件}\n'
                           + '本附件图表编号与对应提交正文及完整报告一致。\\par\\clearpage\n'
                           + ''.join(attachments) + (bib[0] if bib else '') + '\n\\end{document}\n')
        for folder, content in [('正文', text_source), ('图表附件', appendix_source)]:
            target = OUTPUT / folder / source.name
            target.parent.mkdir(parents=True, exist_ok=True)
            # Paths remain explicit for independent recompilation from either subfolder.
            content = content.replace('{figs/', '{../../figs/')
            content = re.sub(r'(?m)[ \t]+$', '', content)
            unchanged = target.exists() and target.read_text(encoding='utf-8') == content
            target.write_text(content, encoding='utf-8', newline='\n')
            built, counts = compile_tex(target, WORK / folder, cached=unchanged)
            shutil.copyfile(built, target.with_suffix('.pdf'))
            pdf = fitz.open(built)
            text = ''.join(page.get_text() for page in pdf)
            if folder == '正文':
                assert not any(page.get_images() for page in pdf), target.name
                for block in blocks:
                    kind = '图' if block['kind'] == 'figure' else '表'
                    needle = f'{kind}{block["number"]}请参见附件{kind}{block["number"]}。'
                    assert needle in re.sub(r'\s+', '', text), (source.name, needle)
                new_aux = built.with_suffix('.aux').read_text(encoding='utf-8')
                new_numbers = dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}', new_aux))
                assert all(new_numbers[k] == label_numbers[k] for k in attachment_labels)
            preview = WORK / 'preview' / folder
            preview.mkdir(parents=True, exist_ok=True)
            for old_preview in preview.glob(source.stem + '_*.png'):
                old_preview.unlink()
            # Render all pages for a contact-sheet review.
            for index, page in enumerate(pdf):
                page.get_pixmap(matrix=fitz.Matrix(.55, .55)).save(preview / f'{source.stem}_{index+1:03}.png')
            summary.append({'report': source.stem, 'version': folder, 'pages': len(pdf),
                            'figures': sum(b['kind'] == 'figure' for b in blocks),
                            'tables': sum(b['kind'] == 'table' for b in blocks), **counts})
            print(source.stem, folder, 'PASS', len(pdf), flush=True)
    (WORK / 'validation.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (OUTPUT / '图表对应清单.json').write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
