"""统一六份报告的三线表、表头和表格外观，生成五部分空白模板。

不修改数据单元格；数字精度按指标保留。核心样式由共享 cls 控制。
"""
from pathlib import Path
import re
import shutil

ROOT=Path(__file__).resolve().parents[3]
REPORTS=ROOT/'reports'
for p in REPORTS.glob('*.tex'):
    s=p.read_text(encoding='utf-8')
    s=re.sub(r'\\pretocmd\{\\(?:section|subsection|subsubsection)\}\{\\Needspace\{\d+\\baselineskip\}\}\{\}\{\}\n?','',s)
    s=s.replace(r'\needspace{8\baselineskip}','')
    s=re.sub(r'\\clearpage\s*(?=\\begin\{thebibliography\})',lambda m:r'\FloatBarrier'+'\n'+r'\Needspace{6\baselineskip}'+'\n',s)
    count=len(re.findall(r'\\bibitem(?:\[[^]]*\])?\{',s))
    if count<=12:
        s=re.sub(r'\\Needspace\{\d+\\baselineskip\}\s*(?=\\begin\{thebibliography\})',lambda m:'\\Needspace{'+str(3*count+3)+'\\baselineskip}\n',s)
    s=re.sub(r'\\AtBeginEnvironment\{(?:tabularx|longtable)\}\{\\linespread\{1\.1\}\\selectfont\}\n?','',s)
    # 每个首表/续表表头统一着色，清除旧稿重复的 rowcolor。
    s=re.sub(r'\\toprule\s*(?:\\rowcolor\{ydzjlight\}\s*)*',lambda m:'\\toprule\n\\rowcolor{ydzjlight} ',s)
    # 纯 tabular 数值表展开到版心宽度，与 tabularx 和长表的外边界一致。
    s=re.sub(r'\\begin\{tabular\}\{([^{}]+)\}',lambda m:r'\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}'+m[1]+r'@{}}',s)
    s=s.replace(r'\end{tabular}',r'\end{tabular*}')
    p.write_bytes(('\n'.join(line.rstrip() for line in s.splitlines())+'\n').encode('utf-8'))

body=r'''
% 一级固定为五部分；二级分方向，三级分方法/步骤，四级仅在需要时使用。
% 标题不手写编号；表格样式由共享 cls 控制。
\section{本月计划}
\subsection{任务目标与范围}
% 写清本月要研究的问题、对象和预期产出。
\subsection{任务安排与前置条件}
% 只写计划与依赖条件，完成状态放第三节。

\section{研究过程}
\subsection{研究方向一：学习、复现或结构研究}
\subsubsection{资料与方法}
\paragraph{输入资料与适用条件}
% 记录来源、软件、几何、边界、物性和统计定义。
\paragraph{实施步骤}
% 按可复现的顺序说明做法；短步骤用 enumerate。
\subsubsection{分析过程}
% 说明如何由资料或计算结果识别问题。
\subsection{研究方向二：控制或其他并行任务}
\subsubsection{方法与步骤}
% 同一层级只放同一类主题；无此方向可删除。

\section{完成情况}
\subsection{任务状态与产出}
\begin{table}[H]\centering
\caption{本月任务完成情况}
\begin{tabularx}{\textwidth}{@{}Y Y Y@{}}
\toprule
\rowcolor{ydzjlight} 任务 & 完成状态 & 实际产出及证据 \\
\midrule
待填写 & 已完成／部分完成／未开始 & 待填写 \\
\bottomrule
\end{tabularx}
\end{table}
\subsection{结果与适用边界}
% 表格、图像和实际记录支持什么结论；缺失数据如实标注。

\section{问题与初步对策}
\subsection{问题一：待填写}
\subsubsection{问题及其证据}
% 说明发现什么、影响什么，避免泛泛列问题。
\subsubsection{初步解决方向}
% 区分已尝试与拟尝试，不要求提前给出最终解答。

\section{下个月计划}
\begin{table}[H]\centering
\caption{下个月任务与预期产出}
\begin{tabularx}{\textwidth}{@{}Y Y Y@{}}
\toprule
\rowcolor{ydzjlight} 任务 & 预期产出 & 前置条件或安排 \\
\midrule
待填写 & 待填写 & 待填写 \\
\bottomrule
\end{tabularx}
\end{table}

\begin{thebibliography}{9}
\bibitem{ref1} 待填写实际使用的参考资料。
\end{thebibliography}
\end{document}
'''
for p in (ROOT/'template').glob('*_空白骨架.tex'):
    s=p.read_text(encoding='utf-8')
    end=s.index(r'\begin{document}')
    head=s[:end].replace('2026-10_阶段一_你的名字_方向.tex','逻辑月N_主题.tex').replace('2026-10_阶段二_你的名字_方向.tex','逻辑月N_主题.tex')
    s=head+'\\begin{document}\n'+('\\makestageonehead' if 'stage1' in head else '\\makestagetwohead')+'\n'+body
    p.write_bytes(s.encode('utf-8'))
shutil.copyfile(REPORTS/'中期报告.tex',REPORTS/'figs/src/midterm_expanded/final_report.tex')
print('表格外观和两份五部分空白模板已统一。')
