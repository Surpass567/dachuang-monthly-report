"""Merge month-two figures 2/3 and their discussion without changing result data."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
path = ROOT / 'reports/逻辑月2_指标与形态.tex'
text = path.read_text(encoding='utf-8')
if '% month2-unified-figure' in text:
    raise SystemExit('Already merged; edit the current TeX directly.')

start = text.index('四种既有流道的后处理结果如图')
end = text.index('表~\\ref{tab:results} 选取', start)
block = text[start:end]
figure_start = block.index('\\begin{figure}[H]')
caption_start = block.index('\\caption{四种流道在各自保存热流密度下')
panels = block[figure_start:caption_start]
panels = panels.replace('\\begin{figure}[H]\n\t\\centering',
    '\\begin{figure}[H]\n\\centering\n% month2-unified-figure\n'
    '\\resizebox*{!}{0.82\\textheight}{%\n\\begin{minipage}{\\textwidth}\n\\centering')
combined = (
    '图~\\ref{fig:contours} 将既有流道的场分布与代表小模型的网格、加热面温度合并展示。'
    '各组工况、色标和温度统计口径分别保留，定量指标及保存条件统一列于后续两表，随后作联合分析。\n\n'
    + panels + '\n\\par\\vspace{5pt}\n'
    '\\includegraphics[width=0.84\\linewidth]{figs/month2_other_models.png}\n'
    '\\end{minipage}%\n}\n'
    '\\caption{流道与代表小模型的场分布及网格汇总。上部 (a)--(p) 按行依次为直线、正弦、NACA2416（均为 300 W/cm$^2$）及 gao2.1（500 W/cm$^2$），按列依次为近壁流体温度、静压、速度和铜板温度；下部三列依次为六边形 v4.2、gao2.1 与叶脉，上排为流固界面网格，下排为各自保存工况的加热面温度。各温度图色标独立，灰白区域为截面外或固体遮罩。}\n'
    '\\label{fig:contours}\n\\end{figure}\n\n'
)
text = text[:start] + combined + text[end:]
text = text.replace(
    '表~\\ref{tab:results} 选取 5 条既有流道记录与 4 条非 NACA 小模型记录。翼型的详细参数与验证分支放在逻辑月三。分组标题区分数据来源与热负荷；不同分组的流量、保存时刻及平均温度口径见后文说明，合并列示不代表各组具备相同的比较条件。',
    '表~\\ref{tab:results} 汇总 5 条既有流道记录与 17 条小模型保存分支，共 22 条记录。不同记录的流量、保存时刻及平均温度口径分别说明，合并列示不代表各组具备相同的比较条件；翼型的详细参数与验证放在逻辑月三。')
start = text.index('在表列 300 W/cm$^2$ 的工况下')
end = text.index('\\begin{table}[H]\\centering\\small', start)
text = text[:start] + '表~\\ref{tab:other-conditions} 列出全部小模型的流量、保存时刻与时间步；各分支网格数保留在配套 CSV 中。\n\n' + text[end:]
start = text.index('六边形 v4 与 v4.2 的热负荷和流量同时发生变化')
end = text.index('\\subsubsection{六种翼型基准结果的统一补充展示}', start)
discussion = r'''\subsubsection{各类小块的联合分析}
\paragraph{场分布、网格与定量结果结合解读}
图~\ref{fig:contours} 的上部将四种流道的温度、静压、速度和铜板温度并列，便于结合流动路径观察温度分布与水力代价；下部补充六边形 v4.2、gao2.1 与叶脉的实际流固界面网格及加热面温度，展示不同拓扑的离散形态和局部温度分布。网格取自实际 Case 文件的平面界面面元，温度直接读取配套 Data 文件，没有额外推进求解。各温度图色标独立，不能仅凭颜色深浅给不同结构排序；网格单元数也只能说明离散规模，不能据此认定网格无关性已经通过。

\paragraph{温度收益与水力代价共同决定候选方向}
结合图~\ref{fig:contours} 与表~\ref{tab:results}，300 W/cm$^2$ 的保存记录中，最高温度和平均温度均为直线低于正弦、正弦低于 NACA2416；压差和水力功率则为 NACA2416 低于直线、直线低于正弦。直线最高温度比正弦低 9.77 $^\circ$C，比 NACA2416 低 19.98 $^\circ$C；相对正弦，其压差低约 37.4\%，水力功率低约 16.6\%。NACA2416 的压差和水力功率均比直线低约 68.2\%，但最高温度较高。这些记录提示温度收益与泵送代价需要共同评价；由于流量并非完全相同，当前仅用于识别候选方向。

\paragraph{仿生与分支结构须连同保存条件比较}
图~\ref{fig:contours} 下部与表~\ref{tab:other-conditions} 共同说明，六边形 v4 与 v4.2 的热负荷、流量同时变化，不能把温度差解释为结构优化的净收益。600 W/cm$^2$ 下，叶脉 A\_leaf 比 gao2.1 的最高温度低约 26.60 $^\circ$C，水力功率约为其 6.07 倍，但两者流量分别为 16 与 9 mL/s，且分别为稳态与 0.2 s 瞬态保存结果，不能将全部差异归因于形状。合并图中 gao2.1 上部采用 500 W/cm$^2$ 的既有流道结果，下部采用 600 W/cm$^2$ 的小模型记录，两者不能当作同一工况相互验证。叶脉已有建模与稳态保存结果，可作为后续筛选基础；结构优劣仍需在统一工况、收敛标准及网格检验下判断。

\paragraph{翼型内部差异为后续参数分组提供线索}
450 W/cm$^2$、约 16 mL/s 和 0.10 s 条件下，NACA3416 v2 比 0016 v2 的最高温度低约 0.230 $^\circ$C，压差高约 5.25\%。350 W/cm$^2$ 的基础、core、BOI 和物性分支仍混有时刻与网格差异；NACA2420 的四条记录属于同一几何的设置检查，126.82 W/cm$^2$ 是 1 s 瞬时热流。这些记录与合并图共同展示了候选结构和数值设置的覆盖范围，但同一几何的设置分支不重复计作新结构。

'''
text = text[:start] + discussion + text[end:]
assert 'fig:other-small' not in text
assert text.count('\\begin{figure}') == 2
path.write_text(text, encoding='utf-8')
print(path)
