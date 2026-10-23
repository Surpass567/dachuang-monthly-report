"""Merge the 17 small-model results into the existing performance table."""
from pathlib import Path
import re

report = Path(__file__).resolve().parents[2] / '逻辑月2_指标与形态.tex'
text = report.read_text(encoding='utf-8')
marker = '% month2-merged-performance'
if marker in text:
    raise SystemExit('性能表已合并，无需重复处理。')

labels = ['results', 'other-small', 'naca350', 'nacav2', 'naca2420']
groups = [
    '既有流道结果（平均温度为体积平均）',
    '非 NACA 小模型（平均温度为固体单元算术平均）',
    'NACA 小模型：350 W/cm$^2$',
    'NACA v2 小模型：450 W/cm$^2$',
    'NACA2420：1 s 时刻的瞬时热流密度',
]
blocks = {}
rows = {}
for label in labels:
    matches = [m for m in re.finditer(r'\\begin\{table\}\[H\].*?\\end\{table\}', text, re.S)
               if rf'\label{{tab:{label}}}' in m.group()]
    assert len(matches) == 1, label
    blocks[label] = matches[0].group()
    body = blocks[label].split(r'\midrule', 1)[1].split(r'\bottomrule', 1)[0]
    rows[label] = []
    for line in body.strip().splitlines():
        cells = [c.strip() for c in line.removesuffix('\\\\').split('&')]
        assert len(cells) == 6, (label, line)
        if label != 'results':
            cells[0], cells[1] = cells[1], cells[0]
        rows[label].append(' & '.join(cells) + r' \\')
assert [len(rows[k]) for k in labels] == [5, 4, 6, 3, 4]

header = r'''\rowcolor{ydzjlight} 热流密度 & 模型或分支 & 最高温度 & 平均温度 & 压差 & 水力功率 \\
/ (W/cm$^2$) & & / $^\circ$C & / $^\circ$C & / kPa & / W \\
\midrule
'''
merged = marker + '\n' + r'''\begingroup
\small
\renewcommand{\arraystretch}{1.05}
\setlength{\tabcolsep}{4pt}
\setlength{\LTleft}{0pt}
\setlength{\LTright}{0pt plus 1fill}
\begin{longtable}{@{}r p{0.30\textwidth} r r r r@{}}
\caption{流道与小模型的温度及水力性能汇总（按数据来源与工况分组）}
\label{tab:results}\\
\toprule
''' + header + r'\endfirsthead' + '\n' + r'''\caption[]{流道与小模型的温度及水力性能汇总（续）}\\
\toprule
''' + header + r'''\endhead
\midrule
\multicolumn{6}{r}{\small 接下页}\\
\endfoot
\bottomrule
\endlastfoot
'''
for label, group in zip(labels, groups):
    merged += r'\multicolumn{6}{@{}l@{}}{\textbf{' + group + '}}\\\\\n'
    merged += '\n'.join(rows[label]) + '\n'
    if label != labels[-1]:
        merged += r'\midrule' + '\n'
merged += '\\end{longtable}\n\\endgroup'
text = text.replace(blocks['results'], merged)
for label in labels[1:]:
    text = text.replace(blocks[label], '')
    text = text.replace(rf'\ref{{tab:{label}}}', r'\ref{tab:results}')
text = text.replace(r'\documentclass[stage2,fontset=fandol]{ydzjreport}',
                    r'\documentclass[stage2,fontset=fandol]{ydzjreport}'+'\n'+r'\usepackage{longtable}')
text = text.replace('（一）四种流道在共同热流密度下的比较', '（一）流道与小模型性能汇总')
text = text.replace('本次新增表格的平均温度统一采用', '表中新增小模型记录的平均温度统一采用')
text = text.replace('与前表既有数据中的体积平均温度、后续翼型表中的底板平均温度分别保留；',
                    '与同表既有流道记录的体积平均温度、后续翼型表中的底板平均温度分别保留；')
text = text.replace('新增表格沿用前述固体单元算术平均温度和水力功率口径，不将其平均温度\n直接并入',
                    '这 13 条记录已并入表~\\ref{tab:results}，沿用前述固体单元算术平均温度和水力功率口径。其平均温度与')
text = text.replace(' 的底板平均温度，也不据此补算缺少统一基准的 PEC。',
                    ' 的底板平均温度口径不同，不据此补算缺少统一基准的 PEC。')
intro = ('表~\\ref{tab:results} 将既有的 5 条流道记录与新增的 17 条小模型记录合并列示。'
         '分组标题区分数据来源与热负荷；不同分组的流量、保存时刻及平均温度口径见后文说明，'
         '合并列示不代表各组具备相同的比较条件。\n\n')
text = text.replace(marker, intro + marker)
text = text.replace(r'\needspace{17\baselineskip}', r'\needspace{6\baselineskip}')
text = text.replace('表~\\ref{tab:results} 中各分支的入口体积流量', '表~\\ref{tab:results} 中 350 W/cm$^2$ 的 NACA 分支入口体积流量')
text = text.replace('表~\\ref{tab:results} 的四个分支', '表~\\ref{tab:results} 中 NACA2420 的四个分支')
report.write_text(text, encoding='utf-8')
print('已合并 22 条性能记录，保留全部原始表格数值。')
