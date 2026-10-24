"""发布前静态检查与 Tectonic 离线编译；通过后同步正式报告 PDF。"""
from pathlib import Path
import importlib.util
import json
import re
import shutil
import subprocess

import fitz

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('report_check', ROOT / 'check.py')
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)
results = {}
changed_sources = subprocess.check_output(
    ['git', 'diff', '--name-only', '-z', '--', '*.tex'], cwd=ROOT
).decode('utf-8').split('\0')
for folder in ('reports', 'template'):
    for source in sorted((ROOT / folder).glob('*.tex')):
        problems = check.check_braces(str(source)) + check.check_refs(str(source))[0]
        assert not problems, (source, problems)
        run = subprocess.run([
            'powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass',
            '-File', str(HERE / 'latex_environment' / 'compile.ps1'),
            '-Source', str(source), '-Offline',
        ], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if run.returncode:
            raise RuntimeError(run.stdout.decode('utf-8', errors='replace'))
        output = source.parent / 'build-latex' / source.name
        log = output.with_suffix('.log').read_text(encoding='utf-8', errors='replace')
        counts = {
            'overfull': len(re.findall(r'Overfull \\[hv]box', log)),
            'missing_characters': log.count('Missing character'),
            'tex_errors': len(re.findall(r'^! ', log, re.M)),
            'undefined_references': len(re.findall(r'(?:Reference|Citation).*undefined|There were undefined', log)),
        }
        assert not any(counts.values()), (source, counts)
        with fitz.open(output.with_suffix('.pdf')) as doc:
            counts['pages'] = len(doc)
        if folder == 'reports' and source.relative_to(ROOT).as_posix() in changed_sources:
            shutil.copy2(output.with_suffix('.pdf'), source.with_suffix('.pdf'))
        results[source.relative_to(ROOT).as_posix()] = counts
        print(source.name, counts, flush=True)
(HERE / 'upload_validation.json').write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
