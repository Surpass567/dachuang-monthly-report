"""对六份当前报告编译、核对引用并生成本地版面联系页。"""
from pathlib import Path
import importlib.util
import json
import re
import shutil
import subprocess
import sys

import fitz
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[3]
REPORTS=ROOT/'reports'
HERE=Path(__file__).resolve().parent
QA=HERE/'structure_qa'
QA.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('report_check',ROOT/'check.py')
check=importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)
names=['逻辑月1_基础建立','逻辑月2_指标与形态','逻辑月3_形态与物理','逻辑月4_迭代与调试','逻辑月5_整板尝试','中期报告']
results={}
compile_filter=next((v.split('=',1)[1].split(',') for v in sys.argv if v.startswith('--compile-only=')),None)
cls=REPORTS/'ydzjreport.cls'
copied=not cls.exists()
if copied: shutil.copy2(ROOT/'template'/'ydzjreport.cls',cls)
try:
    for name in names:
        path=REPORTS/(name+'.tex')
        s=path.read_text(encoding='utf-8')
        # 与 check.py 相同检查；中期宏的 #3 是占位参数，需跳过并检查实际调用。
        braces=check.check_braces(str(path))
        refs,unused=check.check_refs(str(path))
        refs=[p for p in refs if '图片不存在: #3' not in p]
        command=['cmd','/c','tectonic','--only-cached','--keep-logs','--keep-intermediates',path.name]
        if '--no-compile' not in sys.argv and (compile_filter is None or name in compile_filter):
            run=subprocess.run(command,cwd=REPORTS,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            (QA/(name+'_compiler.txt')).write_bytes(run.stdout)
            if run.returncode:
                print(run.stdout.decode('utf-8',errors='replace')[-4000:])
                raise RuntimeError(f'{name}: compiler exit {run.returncode}')
        log=path.with_suffix('.log').read_text(encoding='utf-8',errors='replace')
        labels=re.findall(r'\\label\{([^}]+)\}',s)
        labels=[v for v in labels if '#' not in v]
        labels+=re.findall(r'^\\reportfigure\{([^}]+)\}',s,re.M)
        used=re.findall(r'\\(?:ref|eqref|autoref)\{([^}]+)\}',s)
        cites=[k.strip() for v in re.findall(r'\\cite\{([^}]+)\}',s) for k in v.split(',')]
        bibs=re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',s)
        imgs=re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}',s)
        imgs+=re.findall(r'^\\reportfigure\{[^}]*\}\{[^}]*\}\{([^}]+)\}',s,re.M)
        imgs=[v for v in imgs if '#' not in v]
        pdf=fitz.open(path.with_suffix('.pdf'))
        info={
            'pages':len(pdf),'braces':braces,'static_references':refs,
            'overfull':len(re.findall(r'Overfull \\[hv]box',log)),
            'missing_characters':log.count('Missing character'),
            'tex_errors':len(re.findall(r'^! ',log,re.M)),
            'undefined_log':len(re.findall(r'(?:Reference|Citation).*undefined|There were undefined',log)),
            'missing_references':sorted(set(used)-set(labels)),
            'duplicate_labels':sorted({x for x in labels if labels.count(x)>1}),
            'missing_citations':sorted(set(cites)-set(bibs)),
            'missing_images':[v for v in imgs if not (REPORTS/v).exists()],
            'thin_pages':[],
        }
        # 每页含页码的完整渲染缩略图，用于检查断页、表格与图题。
        thumbs=[]
        for i,page in enumerate(pdf):
            if len(page.get_text().strip())<90:info['thin_pages'].append(i+1)
            pix=page.get_pixmap(matrix=fitz.Matrix(.55,.55),alpha=False)
            thumb=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
            canvas=Image.new('RGB',(thumb.width,thumb.height+23),'#e0e0e0')
            canvas.paste(thumb,(0,23))
            ImageDraw.Draw(canvas).text((7,4),str(i+1),fill='black')
            thumbs.append(canvas)
        for offset in range(0,len(thumbs),12):
            group=thumbs[offset:offset+12]
            w,h=group[0].size
            sheet=Image.new('RGB',(w*3,h*((len(group)+2)//3)),'#b0b0b0')
            for i,thumb in enumerate(group):sheet.paste(thumb,((i%3)*w,(i//3)*h))
            sheet.save(QA/(name+f'_pages_{offset+1}.png'))
        # check.py 不展开 reportfigure 宏，实际宏标签已在 labels 中核对。
        info['static_references']=[v for v in info['static_references'] if not any('\\ref{'+k+'}' in v for k in re.findall(r'^\\reportfigure\{([^}]+)\}',s,re.M))]
        first_text=pdf[0].get_text()
        info['direct_section_start']='报告阶段' not in first_text and '一句话摘要' not in first_text and '月度阅读总结' not in first_text
        results[name]=info
        print(name,json.dumps(info,ensure_ascii=False),flush=True)
finally:
    if copied and cls.exists():cls.unlink()
(HERE/'structure_validation.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
keys=['braces','static_references','overfull','missing_characters','tex_errors','undefined_log','missing_references','duplicate_labels','missing_citations','missing_images']
assert all(not v[k] for v in results.values() for k in keys), '存在未通过检查项'
print('六份报告检查通过。')
