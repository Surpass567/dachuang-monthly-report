"""Compile monthly reports and verify that only the closing note was removed."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

import fitz
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / 'monthly_closing_note_validation'
OUT.mkdir(exist_ok=True)
compiler = Path(os.environ['LOCALAPPDATA']) / 'LaTeXPortable' / 'compile.ps1'
results = []
previews = []
for source in sorted(ROOT.glob('逻辑月*.tex')):
    with (OUT / (source.stem + '_compile.txt')).open('w', encoding='utf-8') as log:
        run = subprocess.run(['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass',
                              '-File', str(compiler), '-Source', str(source), '-Offline'],
                             cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
    assert run.returncode == 0, source.name
    built = ROOT / 'build-latex' / source.with_suffix('.pdf').name
    raw = built.with_suffix('.log').read_text(encoding='utf-8', errors='replace')
    counts = {name: len(re.findall(pattern, raw)) for name, pattern in {
        'overfull': r'Overfull', 'missing': r'Missing character',
        'errors': r'(?m)^! ', 'undefined_references': r'(?:Reference .* undefined|There were undefined references)',
    }.items()}
    assert not any(counts.values()), (source.name, counts)
    original = subprocess.run(['git', 'show', 'HEAD:reports/' + built.name], cwd=ROOT,
                              capture_output=True, check=True).stdout
    old = fitz.open(stream=original, filetype='pdf')
    new = fitz.open(built)
    assert len(old) == len(new), source.name
    old_pages = [p.get_text() for p in old]
    new_pages = [p.get_text() for p in new]
    removed = re.sub(r'——\s*本报告由.*?——\s*', '', old_pages[-1], flags=re.S)
    normalize = lambda s: re.sub(r'\s+', '', s)
    assert normalize(removed) == normalize(new_pages[-1]), source.name
    assert normalize(''.join(old_pages[:-1]) + removed) == normalize(''.join(new_pages)), source.name
    assert '本报告由' not in ''.join(new_pages), source.name
    image_path = OUT / (source.stem + '_last_page.png')
    new[-1].get_pixmap(matrix=fitz.Matrix(1.2, 1.2)).save(image_path)
    panel = Image.open(image_path).convert('RGB')
    panel.thumbnail((420, 610))
    card = Image.new('RGB', (440, 650), 'white')
    card.paste(panel, ((440-panel.width)//2, 25))
    ImageDraw.Draw(card).text((10, 8), f'Month {len(results)+1} / {len(new)} pages', fill='black')
    previews.append(card)
    shutil.copyfile(built, source.with_suffix('.pdf'))
    results.append({'source': source.name, 'pages': len(new), **counts,
                    'body_text_unchanged': True, 'closing_note_removed': True})
    print(source.name, 'PASS', flush=True)
sheet = Image.new('RGB', (440 * len(previews), 650), '#cccccc')
for i, panel in enumerate(previews):
    sheet.paste(panel, (440*i, 0))
sheet.save(OUT / 'last_pages.png')
(OUT / 'validation.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
