"""核查五部分标题、不跳级、月二22条数值与六翼型基准保留情况。"""
from pathlib import Path
import csv
import json
import re

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
expected=['本月计划','研究过程','完成情况','问题与初步对策','下个月计划']
report={}
for p in sorted((ROOT/'reports').glob('*.tex')):
    s=p.read_text(encoding='utf-8').split(r'\begin{document}',1)[1]
    headings=re.findall(r'\\(section|subsection|subsubsection|paragraph)\{([^}]+)\}',s)
    depths={'section':1,'subsection':2,'subsubsection':3,'paragraph':4}
    jumps=[];prev=0
    for kind,title in headings:
        depth=depths[kind]
        if depth>prev+1:jumps.append(title)
        prev=depth
    top=[title for kind,title in headings if kind=='section']
    assert top==expected,(p.name,top)
    assert not jumps,(p.name,jumps)
    report[p.stem]={'sections':top,'heading_counts':{k:sum(h[0]==k for h in headings) for k in depths},'skipped_levels':jumps}
m2=(ROOT/'reports/逻辑月2_指标与形态.tex').read_text(encoding='utf-8')
table=next(m[0] for m in re.finditer(r'\\begin\{longtable\}.*?\\end\{longtable\}',m2,re.S) if r'\label{tab:results}' in m[0])
actual=[]
for line in table.splitlines():
    cells=[v.strip().removesuffix('\\\\').strip() for v in line.split('&')]
    if len(cells)==6 and re.fullmatch(r'\d+(?:\.\d+)?',cells[0]):actual.append(cells)
rows=list(csv.DictReader((HERE/'small_model_results.csv').open(encoding='utf-8-sig')))
assert len(actual)==22,len(actual)
for row,cells in zip(rows,actual[5:]):
    values=[float(row[k]) for k in ['热流密度 (W/cm²)','最高温度 (°C)','平均温度 (°C)','压差 (kPa)','水力功率 (W)']]
    expectedcells=[format(v,fmt) for v,fmt in zip(values,['.2f','.2f','.2f','.3f','.5f'])]
    assert [cells[0]]+cells[2:]==expectedcells,(row['编号'],cells,expectedcells)
legacy=[['300','直线','52.50','38.43','3.074','0.04919'],['300','正弦','62.27','44.84','4.914','0.05897'],['300','NACA2416','72.48','45.99','0.979','0.01566'],['500','gao2.1','68.50','42.55','12.457','0.11211'],['500','NACA2416','99.60','56.82','0.926','0.01482']]
assert actual[:5]==legacy
for wing in ['0015','0021','0024','4424','6424','6624']:assert 'NACA'+wing in m2
report['month2_data']={'legacy_rows':5,'csv_rows':17,'combined_rows':22,'csv_rounded_values_match':True,'six_airfoil_baselines_retained':True}
(HERE/'outline_data_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('六份报告五部分及标题层级通过；月二22条记录与源数值一致，六翼型基准保留。')
