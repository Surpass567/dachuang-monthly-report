from pathlib import Path
import csv,shutil,json

ROOT=Path(__file__).resolve().parents[3]
SIM=ROOT.parent
REPORT=ROOT/'reports'
source=REPORT/'逻辑月2_指标与形态.tex'
s=source.read_text(encoding='utf8')
if 'tab:other-small' in s:
    raise SystemExit('逻辑月2已包含小模型补充内容，无需重复插入。')
rows=list(csv.DictReader((REPORT/'figs/src/small_model_results.csv').open(encoding='utf-8-sig')))
byid={r['编号']:r for r in rows}
def table(ids,names,caption,label):
    head=r'''\begin{table}[H]
\centering
\small
\caption{CAPTION}
\label{LABEL}
\begin{tabularx}{\textwidth}{@{}Y r r r r r@{}}
\toprule
\rowcolor{ydzjlight} 模型或分支 & 热流密度 & 最高温度 & 平均温度 & 压差 & 水力功率 \\
 & / (W/cm$^2$) & / $^\circ$C & / $^\circ$C & / kPa & / W \\
\midrule
'''.replace('CAPTION',caption).replace('LABEL',label)
    for ident,name in zip(ids,names):
        r=byid[ident]
        nums=[float(r[c]) for c in ['热流密度 (W/cm²)','最高温度 (°C)','平均温度 (°C)','压差 (kPa)','水力功率 (W)']]
        head+=name+' & '+ ' & '.join(format(v,fmt) for v,fmt in zip(nums,['.2f','.2f','.2f','.3f','.5f']))+r' \\'+'\n'
    return head+r'\bottomrule'+'\n'+r'\end{tabularx}'+'\n'+r'\end{table}'+'\n'

others=r'''
\textbf{流道形态与网格的补充整理。}
在既有四种流道数据之外，我补充整理了六边形 v4、六边形 v4.2、
gao2.1 和叶脉 A\_leaf 的保存结果。表~\ref{tab:other-small} 记录了各自工况下的
温度和水力指标，表~\ref{tab:other-conditions} 列出网格与计算条件。
其中叶脉模型已经完成建模并保存了稳态结果，可作为后续仿生结构筛选的基础。

本次新增表格的平均温度统一采用\textbf{固体单元温度算术平均}，
与前表既有数据中的体积平均温度、后续翼型表中的底板平均温度分别保留；
最高温度取固体单元最大值，压差取入口与出口的面积加权平均静压之差，
水力功率按 $P_{\mathrm{hyd}}=\Delta p\,\dot V$ 计算。
对于 gao2.1 的多个入口和出口，分别按总面积加权，入口体积流量取各入口之和。
'''
others+=table(['M01','M02','M09','M17'],['六边形 v4','六边形 v4.2','gao2.1',r'叶脉 A\_leaf'],'非 NACA 小模型在各自保存工况下的性能','tab:other-small')
others+=r'''
\begin{table}[H]
\centering
\small
\caption{非 NACA 小模型的网格与计算条件}
\label{tab:other-conditions}
\begin{tabularx}{\textwidth}{@{}Y r r r r@{}}
\toprule
\rowcolor{ydzjlight} 模型 & 网格单元数 & 保存时刻 / s & 时间步 / s & 流量 / (mL/s) \\
\midrule
六边形 v4 & 1,443,844 & 15.00 & 0.5 & 77.043 \\
六边形 v4.2 & 1,320,229 & 6.05 & 0.01 & 15.000 \\
gao2.1 & 2,347,198 & 0.20 & 0.01 & 9.000 \\
叶脉 A\_leaf & 5,031,324 & 稳态 & --- & 16.000 \\
\bottomrule
\end{tabularx}
\end{table}

六边形 v4 与 v4.2 的热负荷和流量同时发生变化，因此不能把两者的温度差
解释为结构优化的净收益。gao2.1 与叶脉模型虽然都采用 600 W/cm$^2$，
但流量分别为 9 和 16 mL/s，且一个是瞬态保存结果、一个是稳态结果；
当前只能记录各自的散热表现与水力代价，尚不能据此给出结构优劣排序。

图~\ref{fig:other-small} 对照展示了三种代表模型的流固界面网格和加热面温度。
图中网格来自实际 Case 文件的平面界面面元，温度直接读取配套 Data 文件的加热面数据，
没有额外推进求解。各温度子图采用独立色标，颜色仅反映各自工况的温度分布。
现有单元数可说明离散规模，\textbf{不能仅据此认定网格无关性已经通过}；
仍需对同一几何在统一工况和收敛标准下比较不同网格的结果。

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{figs/month2_other_models.png}
\caption{六边形 v4.2、gao2.1 与叶脉模型的实际界面网格及加热面温度。上排为平面流固界面网格，下排为各自保存工况的加热面温度；各列工况不同，色标独立。}
\label{fig:other-small}
\end{figure}

'''

naca=r'''
\textbf{NACA 小模型的补充结果。}
在上述六种翼型基准对比之外，我进一步整理了 NACA0016、1416、2416、3416
及 2420 的已有小模型结果，共 13 条代表性分支。
这些分支包含几何变化、网格组织、物性验证及时间步验证，不能全部视为独立翼型。
新增表格沿用前述固体单元算术平均温度和水力功率口径，不将其平均温度
直接并入表~\ref{tab:airfoil} 的底板平均温度，也不据此补算缺少统一基准的 PEC。

\textbf{350 W/cm$^2$ 下的几何、网格与物性分支。}
表~\ref{tab:naca350} 中各分支的入口体积流量均约为 16 mL/s。
L450 表示弦长 450 $\mu$m，A06 与 A00 分别对应 $6^\circ$ 和 $0^\circ$ 攻角，
原模型目录中的 98989 阵列标识保留在数据来源中。
NACA0016 A06 基础分支为 3,048,985 单元，保存时刻 0.10 s；
其拟合物性和 REFPROP 物性分支采用相同网格，时间步均为 0.001 s，
但分别保存于 0.200 s 和 0.137 s。
NACA2416 A00 core 与尾部 BOI 分支分别为 4,371,445 和 3,079,413 单元，
保存时刻分别为 0.15 s 和 0.20 s，时间步均为 0.01 s；
NACA2416 v3 列出 3,235,081 单元、时间步 0.001 s、0.20 s 时刻的结果。
基础 NACA0016 A06 的时间步为 0.01 s。
'''
naca+=table(['M03','M04','M05','M06','M07','M08'],['0016 A06 基础','2416 A00 core','2416 A00 尾部 BOI','0016 A06 拟合物性','0016 A06 REFPROP','2416 v3'],'350 W/cm$^2$ 下 NACA 小模型的保存结果','tab:naca350')
naca+=r'''
这些记录说明了不同分支的温度与水力量级，但保存时刻、攻角及网格并未全部一致。
尤其是物性分支的最终保存时刻不同，不能用本表的末态温差代替同一时刻的物性误差；
core 与 BOI 分支也不能仅凭本表认定网格无关。

\textbf{450 W/cm$^2$ 下三种 v2 翼型的初步比较。}
三组结果的热流密度均为 450 W/cm$^2$，入口流量约为 16 mL/s，
时间步均为 0.0002 s，保存时刻均为 0.10 s。
NACA0016、1416、3416 的网格分别为 821,987、792,259、783,184 单元。
表~\ref{tab:nacav2} 显示，三者最高温度相差不足 0.23 $^\circ$C；
与 NACA0016 相比，NACA3416 最高温度降低约 0.230 $^\circ$C，
压差和水力功率均提高约 5.25\%。
这提示弯度变化带来的温度收益需要与流动代价一起衡量，
但当前数据只支持该保存时刻的初步比较，仍需检查收敛状态和网格敏感性。
'''
naca+=table(['M14','M15','M16'],['NACA0016 v2','NACA1416 v2','NACA3416 v2'],'同热负荷、同流量与同保存时刻的 v2 翼型结果','tab:nacav2')
naca+=r'''
图~\ref{fig:naca-small} 给出了三种 v2 翼型的实际界面网格和加热面温度。
各子图分别标注色标；加热面温度是表面局部值，
与表中固体全域最高温度和固体单元算术平均温度含义不同。

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{figs/month2_naca_models.png}
\caption{NACA0016、1416、3416 v2 小模型的界面网格与 0.10 s 加热面温度。上排为实际平面流固界面网格，下排温度来自各自配套 Data 文件，色标独立。}
\label{fig:naca-small}
\end{figure}

\textbf{NACA2420 的回流设置、物性与时间步检查。}
表~\ref{tab:naca2420} 的四个分支均为 771,225 单元，保存时刻均为 1 s。
加热边界采用随时间变化的热流，表中 126.82 W/cm$^2$ 为 1 s 的瞬时值，
不是整个计算过程的恒定热负荷。原始分支流量约为 12.000 mL/s，
其余三个分支约为 12.041 mL/s；原始与回流温度 300 K 分支的时间步均为 0.01 s。
'''
naca+=table(['M10','M11','M13','M12'],['2420 v4 原始','2420 回流 300 K',r'2420 IAPWS $\Delta t=0.01$ s',r'2420 IAPWS $\Delta t=0.005$ s'],'NACA2420 在 1 s 时刻的设置与时间步验证结果','tab:naca2420')
naca+=r'''
采用 IAPWS 物性后，将时间步从 0.01 s 减小到 0.005 s，
1 s 时刻的最高温度差约为 $3.68\times10^{-6}$ K，压差相对差约为
$2.75\times10^{-5}\%$，各项指标在表中精度下相同。
因此，这组结果在该时刻对本次时间步减半不敏感；
这一检查不等同于验证整个瞬态过程，也不能替代网格无关性检验。
本次新增的 17 条代表结果与源文件对应关系已整理到小模型汇总数据中\cite{smallmodels}。

'''

s=s.replace(r'\textcolor{red}{汇总补充模型核对应云图，大树哥哥统一后处理}', '')
s=s.replace(r'\section{进阶阅读与理论支撑}',r'\par\needspace{10\baselineskip}'+'\n'+r'\section{进阶阅读与理论支撑}')
s=s.replace(r'\textbf{（二）六种翼型在基准工况下的比较}',others+r'\par\needspace{17\baselineskip}'+'\n'+r'\textbf{（二）六种翼型在基准工况下的比较}')
s=s.replace(r'\textbf{（三）控制回路仿真}',naca+r'\textbf{（三）控制回路仿真}')
s=s.replace('已提取设计灵感并列入候选，尚未形成独立方案','已保存叶脉稳态结果，并补入六边形分支；统一工况对比待完成')
s=s.replace('四种流道 39 个有效工况','既有四种流道 39 个有效工况；补充六边形、gao2.1 与叶脉结果')
s=s.replace('六种 NACA 翼型流热耦合仿真 \\', '六种翼型基准仿真；补充 13 条 NACA 小模型结果分支 \\')
s=s.replace('完成四种流道与六种翼型的对比，','保留四种流道与六种翼型的既有对比，补充 17 条小模型结果及网格、温度配图，')
s=s.replace(r'  \item 建立控制回路的一阶热平衡模型',r'  \item 补充整理六边形、gao2.1、叶脉及 NACA 小模型的 17 条代表性结果分支，核对热负荷、网格、流量与保存时刻，提取界面网格和加热面温度配图；'+'\n'+r'  \item 建立控制回路的一阶热平衡模型')
s=s.replace('单元层面的结果资料较为完整，结构工作由多方案探索推进到重点形态筛选。','新增 17 条小模型分支及其来源记录，结构工作由多方案探索推进到重点形态筛选；新增分支尚需统一工况复核。')
s=s.replace('仿生形态（叶脉／沙丘）建模与同工况对比','复核已有叶脉模型并开展叶脉／沙丘同工况对比')
s=s.replace(r'\bibitem{airfoil}',r'\bibitem{smallmodels} 小模型保存结果与性能汇总. 项目仿真资料, 2026. 见配套数据文件 small\_model\_results.csv 及 model\_sources.json；数值由 Case／Data 提取，图像由实际面元及表面温度生成。'+'\n'+r'\bibitem{airfoil}')
out=REPORT/source.name
out.write_text(s,encoding='utf8')
(REPORT/'figs/src/model_sources.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
(REPORT/'figs/src/month2_small_models.md').write_text('''# 逻辑月2补充说明

报告位于 reports/逻辑月2_指标与形态.tex，保留了控制文献内容，并补入小模型结果。

新增 17 条代表分支：前面的流道形态与网格部分 4 条，NACA 部分 13 条。37 条原始提取记录中的网格变化、归档副本未重复视为独立模型。

small_model_results.csv 与 model_sources.json 保留所有原值和源文件路径。新增表格平均温度为固体单元算术平均，历史表格沿用原来的体积平均或底板平均口径。

配图直接读取 Fluent HDF5 Case 面节点及 Data 表面温度，不推进求解，也不进行几何重建。每个界面提取面元最多的坐标平面，六边形为 x-z 视图，其他模型为 x-y 视图；这些是界面平面面元，不宣称为内部体网格截面。温度图为加热面局部值，采用各自色标，不能把图上最大值当作固体全域最大值。

复现：从仓库根目录运行 python reports/figs/src/build_small_model_figures.py，然后在 reports 内编译同名 tex。输入汇总位于本目录，源 Case/Data 文件须可读。update_month2.py 是一次性正文插入脚本，当前报告已完成插入，无需再次执行。
''',encoding='utf8')
print(out)
