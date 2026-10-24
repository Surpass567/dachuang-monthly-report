# -*- coding: utf-8 -*-
"""把中期报告重排为“干了什么 / 怎么干的 / 得到了什么 / 未来计划”四块。

一次性迁移脚本：按标记切分现有正文，原样搬运数值表格与图件，只改章节框架、
过渡语句、方向编号和月份表述。重复运行会被保护挡住，避免覆盖人工修改。
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "reports" / "中期报告.tex"
s = SRC.read_text(encoding="utf-8")

if "\\section{干了什么" in s:
    raise SystemExit("报告已是四块结构，脚本不再执行（避免覆盖人工修改）。")


def part(a, b):
    i = s.index(a)
    j = s.index(b, i)
    assert i < j, (a, b)
    return s[i:j]


def body(block):
    return block.split("\n", 1)[1]


def remap(t):
    """旧编号：方向一=代理、方向二=结构、方向三=控制 → 新编号：结构/控制/代理。"""
    t = t.replace("方向一", "@1@").replace("方向二", "@2@").replace("方向三", "@3@")
    return t.replace("@1@", "方向三").replace("@2@", "方向一").replace("@3@", "方向二")


# ---------- 原文块 ----------
pre = s[: s.index("\\section{本月计划}")]
intro = part("\\subsection{项目概述}", "\\subsection{任务目标}")
task = body(part("\\subsection{任务目标}", "\\subsection{研究背景与项目目标}"))
bg1 = part("\\subsubsection{时空非均匀热负荷下的散热需求}", "\\subsubsection{微通道热管理面临的问题}")
bg2 = part("\\subsubsection{微通道热管理面临的问题}", "\\subsubsection{项目的原始研究思路}")
bg3 = part("\\subsubsection{项目的原始研究思路}", "\\subsubsection{项目总体研究目标}")
goal = part("\\subsubsection{项目总体研究目标}", "\\subsection{项目总体技术路线与研究演化}")
evo = part("\\subsection{项目总体技术路线与研究演化}", "\\section{研究过程}")
lit = part("\\subsection{文献与理论准备}", "\\subsection{研究步骤与分析框架}")
geom = part("\\subsubsection{几何建模与计算域}", "\\subsubsection{三类流道复现与后处理基础}")
repro = part("\\subsubsection{三类流道复现与后处理基础}", "\\subsubsection{CFD数值模型与基本控制方程}")
eqs = part("\\subsubsection{CFD数值模型与基本控制方程}", "\\subsubsection{网格划分及网格无关性验证}")
mesh_method = part("\\subsubsection{网格划分及网格无关性验证}", "本报告提取了 NACA2416")
mesh_results = part("本报告提取了 NACA2416", "\\subsubsection{温度相关物性UDF与非均匀热源设置}")
udf_method = part("\\subsubsection{温度相关物性UDF与非均匀热源设置}", "\\paragraph{已有拟合精度和同一时刻求解对照}")
udf_results = part("\\paragraph{已有拟合精度和同一时刻求解对照}", "\\subsubsection{数值仿真自动化流程}")
auto = part("\\subsubsection{数值仿真自动化流程}", "\\subsubsection{流动与传热性能评价指标}")
metric = part("\\subsubsection{流动与传热性能评价指标}", "\\subsection{区域化冷板连接结构设计与阶段性成果（方向二）}")
conn = part("\\subsection{区域化冷板连接结构设计与阶段性成果（方向二）}", "\\subsubsection{局部结构筛选与小模型结果}")
small = part("\\subsubsection{局部结构筛选与小模型结果}", "\\textbf{（一）四种流道在共同热流密度下的比较}")
flows = part("\\textbf{（一）四种流道在共同热流密度下的比较}", "\\textbf{流道形态与网格的补充整理。}")
other = part("\\textbf{流道形态与网格的补充整理。}", "\\textbf{（二）六种翼型在基准工况下的比较}")
airfoil = part("\\textbf{（二）六种翼型在基准工况下的比较}", "\\textbf{NACA 小模型的补充结果。}")
naca = part("\\textbf{NACA 小模型的补充结果。}", "\\textbf{450 W/cm$^2$ 下三种 v2 翼型的初步比较。}")
nacav2 = part(
    "\\textbf{450 W/cm$^2$ 下三种 v2 翼型的初步比较。}",
    "\\textbf{NACA2420 的回流设置、物性与时间步检查。}",
)
naca2420 = part(
    "\\textbf{NACA2420 的回流设置、物性与时间步检查。}",
    "\\subsubsection{基本单元与连接结构}",
)
unit = part("\\subsubsection{基本单元与连接结构}", "\\subsubsection{三类代表性热负荷工况}")
load = part("\\subsubsection{三类代表性热负荷工况}", "\\subsubsection{连接结构的数值验证}")
cval = part("\\subsubsection{连接结构的数值验证}", "\\subsubsection{性能对照与优势分析}")
ccmp = part("\\subsubsection{性能对照与优势分析}", "\\subsubsection{流动传热机理讨论}")
mech = part("\\subsubsection{流动传热机理讨论}", "\\subsubsection{当前完成情况与成果总结}")
csum = part("\\subsubsection{当前完成情况与成果总结}", "\\subsection{非均匀动态热负荷下的协同调控研究（方向三）}")
cdef = part("\\subsubsection{动态热负荷问题定义}", "\\subsubsection{双泵与行级阀门控制架构}")
carch = part("\\subsubsection{双泵与行级阀门控制架构}", "\\subsubsection{动态非均匀热源建模}")
cheat = part("\\subsubsection{动态非均匀热源建模}", "\\subsubsection{初步数学模型与最小闭环验证}")
cpid = part("\\subsubsection{初步数学模型与最小闭环验证}", "\\subsubsection{向物理机理融合模型的发展}")
cgrey = part("\\subsubsection{向物理机理融合模型的发展}", "\\subsubsection{当前研究进展与下一阶段任务}")
cend = part("\\subsubsection{当前研究进展与下一阶段任务}", "\\subsection{物理机理融合的代理模型与计算加速研究（方向一）}")
sreq = part("\\subsubsection{代理模型研究需求的提出}", "\\subsubsection{代表性翼型结构与几何参数化}")
spar = part("\\subsubsection{代表性翼型结构与几何参数化}", "\\subsubsection{CFD数据集构建方法}")
sdata = part("\\subsubsection{CFD数据集构建方法}", "\\subsubsection{物理机理分析与理论推导路线}")
stheo = part("\\subsubsection{物理机理分析与理论推导路线}", "\\subsubsection{物理与机器学习融合的模型框架}")
sfuse = part("\\subsubsection{物理与机器学习融合的模型框架}", "\\subsubsection{代理模型精度、泛化及计算效率评价}")
seval = part("\\subsubsection{代理模型精度、泛化及计算效率评价}", "\\subsubsection{当前研究进展与后续计划}")
send = part("\\subsubsection{当前研究进展与后续计划}", "\\section{完成情况}")
dkey = part("\\subsection{关键结果与完成边界}", "\\subsection{可以确定的}")
dcert = part("\\subsection{可以确定的}", "\\subsection{尚不能确定的}")
dunc = part("\\subsection{尚不能确定的}", "\\section{问题与初步对策}")
pdiff = part("\\subsection{与预期的差异}", "\\subsection{遇到的主要问题}")
pmain = part("\\subsection{遇到的主要问题}", "\\subsection{已尝试的方案}")
ptried = part("\\subsection{已尝试的方案}", "\\subsection{下一步对策}")
pnext = part("\\subsection{下一步对策}", "\\section{下个月计划}")
pp1 = part("\\subsection{下一阶段研究任务与里程碑}", "\\subsection{承接月4理论迭代与月5整板尝试}")
pp2 = part("\\subsection{承接月4理论迭代与月5整板尝试}", "\\subsection{三个方向的协同与系统级验证路线}")
pp3 = part("\\subsection{三个方向的协同与系统级验证路线}", "\\FloatBarrier\n\n\\FloatBarrier")

# ---------- 局部改写 ----------
intro_lines = intro.split("\n")
name_line = [x for x in intro_lines if x.startswith("\\textbf{项目名称")][0]
p1 = [x for x in intro_lines if x.startswith("时空非均匀热负荷")][0]

goal = goal.replace("\\subsubsection{项目总体研究目标}", "\\subsubsection{总体目标与方向对应}")
goal = goal.replace(
    "中期考核的重点是说明这一链条已推进到何种程度，而非提前宣布系统最优或所有任务完成。表\\ref{tab:01}给出目标与三个方向之间的对应关系。",
    "链条分为三个方向：方向一解决区域结构适配与连接性能，方向二解决动态运行下的流量分配与协同控制，"
    "方向三为前两者提供快速预测方法。表\\ref{tab:01}给出目标、方向与本阶段交付要求的对应关系；实际完成状态见第三部分。",
)
goal = goal.replace("研究目标、对应方向与中期状态", "研究目标、对应方向与阶段交付要求")
goal = goal.replace("阶段依据与交付边界", "本阶段交付要求")
goal = goal.replace(
    "方向二 & 区域结构适配与连接性能验证 & 已有候选方案与装配几何；尚缺连接段独立成对性能结果。 \\\\\n"
    "方向三 & 动态温度响应与泵阀协同 & 已有简化 PID 仿真与时序；设备辨识及多行控制验证待开展。 \\\\\n"
    "方向一 & 物理融合预测与计算加速 & 已有数值与自动化基础；数据集与算法研究正在推进。 \\\\\n"
    "系统协同 & 统一对象下评价温度、均匀性和代价 & 整板几何与热源映射已有记录；系统流热与控制验证拟开展。 \\\\",
    "方向一 & 区域结构适配与连接性能验证 & 同主体、同工况的连接成对对照及机理说明。 \\\\\n"
    "方向二 & 动态温度响应与泵阀协同 & 可追溯的闭环时序、物理模型与执行器边界。 \\\\\n"
    "方向三 & 物理融合预测与计算加速 & 统一口径的数据集、独立测试与成本评价。 \\\\\n"
    "系统协同 & 统一对象下评价温度、均匀性和代价 & 整板参考流热解与多行协同验证。 \\\\",
)

evo = evo.replace("\\subsection{项目总体技术路线与研究演化}", "\\subsection{总体工作与三个方向}")
evo = evo.replace(
    "表\\ref{tab:15}概括对应数据、参数和验证需求的流向，区分当前已有支撑与后续拟建立的联动。",
    "三者的数据、参数与验证需求在后文按方向分别展开，并在第四部分汇总为同一对象上的系统级验证。",
)
evo = evo.replace("\\enlargethispage{\\baselineskip}", "")
evo = remap(evo)

lit = lit.replace("本节沿用原报告已核实的三项文献", "本节沿用已核实的三项文献")

mesh_method = mesh_method.replace("\\subsubsection{网格划分及网格无关性验证}", "\\subsubsection{网格划分与检验方法}")

udf_method = udf_method.replace(
    "\\subsubsection{温度相关物性UDF与非均匀热源设置}", "\\subsubsection{温度相关物性 UDF 与热源设置}"
)
udf_method = udf_method.rstrip("\n") + "\n\n物性拟合精度与同一时刻的求解对照属于平台校验结果，见第三部分。\n\n"
udf_results = udf_results.replace("\\paragraph{已有拟合精度和同一时刻求解对照}", "\\subsubsection{物性实现对照}")

conn = remap(conn).replace(
    "\\subsection{区域化冷板连接结构设计与阶段性成果（方向二）}",
    "\\subsection{方向一：连接结构的设计与验证方法}",
)
small = remap(small).replace("\\subsubsection{局部结构筛选与小模型结果}", "\\subsubsection{局部结构对照的设计}")
small = small.rstrip("\n") + "\n\n各分支的保存条件与实测指标见第三部分，本节只说明对照是如何组织的。\n\n"
unit = remap(unit)
cval = remap(cval)
ccmp = remap(ccmp)
mech = remap(mech)
csum = remap(csum).replace("\\subsubsection{当前完成情况与成果总结}", "\\subsubsection{阶段小结}")
cdef = remap(cdef)
carch = remap(carch)
cheat = remap(cheat)
cpid = remap(cpid)
cgrey = remap(cgrey)
cend = remap(cend).replace("\\subsubsection{当前研究进展与下一阶段任务}", "\\subsubsection{阶段小结}")
send = remap(send).replace("\\subsubsection{当前研究进展与后续计划}", "\\subsubsection{阶段小结}")
sreq = remap(sreq)
spar = remap(spar)
sdata = remap(sdata)
stheo = remap(stheo)
sfuse = remap(sfuse)
seval = remap(seval)
pp1 = remap(pp1)
pp3 = remap(pp3)

merged_val = "\\subsubsection{连接结构的验证方案}\n" + body(cval) + "\n" + body(ccmp)

pid_head = "\\subsubsection{初步数学模型与最小闭环验证}"
m_fig = "图~\\ref{fig:20}直接由已有数组重绘"
m_find = "原程序先更新并限幅累计误差变量"
m_eq = "基础 PID 可写为"
pid_setup = cpid[cpid.index(pid_head) : cpid.index(m_fig)].replace(pid_head, "\\subsubsection{最小闭环对象与 PID 控制}")
pid_fig = cpid[cpid.index(m_fig) : cpid.index(m_find)]
pid_find = cpid[cpid.index(m_find) : cpid.index(m_eq)]
pid_eq = cpid[cpid.index(m_eq) :]

# 结果块：把加粗引导句改为四级标题（规范要求不以加粗段代替标题）
flows = flows.replace("\\textbf{（一）四种流道在共同热流密度下的比较}", "\\subsubsection{四种流道在共同热流密度下的比较}", 1)
other = other.replace("\\textbf{流道形态与网格的补充整理。}", "\\subsubsection{流道形态与网格的补充}", 1)
airfoil = airfoil.replace("\\textbf{（二）六种翼型在基准工况下的比较}", "\\subsubsection{六种翼型在基准工况下的比较}", 1)
naca = naca.replace("\\textbf{NACA 小模型的补充结果。}\n", "")
naca = naca.replace(
    "\\textbf{350 W/cm$^2$ 下的几何、网格与物性分支。}", "\\paragraph{350 W/cm$^2$ 下的几何、网格与物性分支}"
)
nacav2 = nacav2.replace(
    "\\textbf{450 W/cm$^2$ 下三种 v2 翼型的初步比较。}", "\\paragraph{450 W/cm$^2$ 下三种 v2 翼型的初步比较}"
)
naca2420 = naca2420.replace(
    "\\textbf{NACA2420 的回流设置、物性与时间步检查。}", "\\paragraph{NACA2420 的回流设置、物性与时间步检查}"
)

dkey = dkey.replace("\\subsection{关键结果与完成边界}", "\\subsubsection{关键量化结果}")
dcert = dcert.replace("\\subsection{可以确定的}", "\\subsubsection{可以确定的}")
dunc = dunc.replace("\\subsection{尚不能确定的}", "\\subsubsection{尚不能确定的}")
pmain = pmain.replace("\\subsection{遇到的主要问题}", "\\subsection{主要问题与初步对策}")
ptried = ptried.replace("\\subsection{已尝试的方案}", "\\subsubsection{已尝试的方案}")

pnext_body = body(pnext)
pnext_body = pnext_body.replace("\\begin{enumerate}", "\\subsubsection{下一步对策}\n\\begin{enumerate}", 1)
pnext_body = pnext_body.replace("\\item 固定几何、物性", "\\item 连接方向（M1）：固定几何、物性")
pnext_body = pnext_body.replace("\\item 补齐最小闭环", "\\item 控制方向（M1--M2）：补齐最小闭环")
pnext_body = pnext_body.replace("\\item 统一数据划分", "\\item 代理方向（M3）：统一数据划分")
pnext_body = pnext_body.replace(
    "\\end{enumerate}",
    "\\item 系统评价（M4）：以同一整板对象建立参考解，统一控制约束、监测位置、统计时段与成本口径，再比较各方案。\n\\end{enumerate}",
)

pp1 = pp1.replace(
    "此处承接原中期报告的下一阶段安排。月度起止日期尚未确认，故保留 M1--M4 的依赖顺序和日期待补项，不将全部里程碑承诺为一个月内完成。",
    "本节按依赖关系组织下一阶段任务。具体日期在团队确认结题节点后填写，M1--M4 只表示依赖顺序，不代表固定周期。",
)
pp1 = pp1.replace("\\subsection{下一阶段研究任务与里程碑}", "\\subsection{任务与里程碑}")
pp2 = pp2.replace("\\subsection{承接月4理论迭代与月5整板尝试}", "\\subsection{整板与系统验证检查项}")
pp2 = pp2.replace(
    "月4研究不同热流密度下的小块选择分界线，并拟通过 Bi 与扰流柱数量分析迭代小块理论；XGBoost 尚未开展。",
    "前期研究了不同热流密度下的小块选择分界线，并拟通过 Bi 与扰流柱数量分析迭代小块理论；XGBoost 尚未开展。",
)
pp2 = pp2.replace("月5承接连接、供液及整板尝试，后续验证分解为五项内容。", "连接、供液及整板尝试的后续验证分解为五项内容。")
pp3 = pp3.replace("\\subsection{三个方向的协同与系统级验证路线}", "\\subsection{三方向的协同路线}")

# ---------- 新写段落 ----------
ch1_13 = r"""
\subsection{各方向完成的工作}

三个方向各自完成的工作可概括如下。方向一从整板分区与单元划分出发，建立了连接方案库和 40 mm 条带装配，完成了四种流道、六种翼型及多条小模型分支的数值对照，并准备了连接段的成对计算。方向二从动态负荷问题定义出发，形成了十行单向流路、双泵与行级出口阀门的控制架构，建立了非均匀热源模型，并在一阶集总对象上完成了增量式 PID 闭环仿真。方向三从高保真计算成本出发，确定了参数化建模、自动化批量计算、数据集构建与物理信息融合的技术路线，并完成了网格、物性和评价口径的前置整理。

表\ref{tab:work}把三项工作与产出形态对应起来。表中“产出形态”只说明已有材料的类型，不代表性能已经验证；具体数值与边界见第三部分。
\begin{table}[htbp]
\centering\small
\caption{三个方向的工作内容与产出形态}\label{tab:work}
\begin{tabularx}{\linewidth}{@{}lYY@{}}
\toprule
\rowcolor{ydzjlight} 方向 & 已开展的工作 & 产出形态 \\
\midrule
方向一 & 单元划分、连接方案库、40 mm 条带装配、四流道与六翼型对照、多条小模型分支 & 几何装配、工况表、温度与水力数据 \\
方向二 & 十行流路、双泵与行级阀门架构、非均匀热源模型、一阶对象 PID 闭环 & 架构方案、模型方程、闭环时序 \\
方向三 & 参数化建模、批量计算流程、数据集设计、物理信息融合路线 & 技术路线、流程图、数据字典 \\
\bottomrule
\end{tabularx}
\end{table}
"""

ch2_lead = r"""
\section{怎么干的：研究方法}

"""

ch2_platform_lead = r"""
\subsection{共享数值平台与工况}
三个方向共用同一套几何、工况、方程、网格、物性、自动化流程和评价口径。本节按这一顺序说明做法，平台的可用性证据集中在第三部分，本节不重复数值结果。

"""

ch3_lead = r"""
\section{得到了什么：研究结果}

\subsection{数值平台的可用性}
平台的可用性由三组已有记录支持：三类流道复现、七档网格诊断和物性实现对照。三组结果分别说明建模与后处理流程可用、离散误差的量级和物性实现的一致性，不构成对全部构型或全部工况的验证。
"""

ch3_32_lead = r"""
\subsection{方向一：结构对照结果}
结构对照按对象分组：共同热流密度下的四种流道、其他小模型、六种翼型基准和 NACA 小模型分支。各表的平均温度定义、保存时刻与流量条件均在表内注明，不同口径之间不直接横向排序。
"""

ch3_33_lead = r"""
\subsection{方向二：闭环仿真结果}
方向二的量化结果来自简化闭环时序及其程序复核，尚不包括真实泵阀系统。下面先给出保存的时序，再说明程序核查发现的问题。
"""

ch3_35_lead = r"""
\subsection{成果清单与结论边界}
本节把前面的进展收拢为一张状态表、一张量化记录表和一组结论边界。状态按“已有结果—部分完成—未完成”三级描述，不使用完成百分比。
"""

status_table = r"""
\begin{table}[htbp]\centering\small
\caption{按现有保存记录核对的中期任务状态}\label{tab:monthly_status}
\begin{tabularx}{\linewidth}{@{}Y c Y Y@{}}
\toprule
\rowcolor{ydzjlight} 方向与任务 & 状态 & 已有证据 & 下一步 \\
\midrule
方向一：局部结构复现与筛选 & 已有结果 & 三类复现云图；四种流道39工况；六翼型及17条小模型分支。 & 统一工况后进入连接对照。 \\
方向一：连接段及流路集成 & 部分完成 & 连接方案库、40 mm 条带与整板装配几何。 & 连接段成对性能计算。 \\
共享平台：物性实现与数值诊断 & 阶段完成 & 1601点拟合核对、0.137 s实现对照、七档网格与出口诊断。 & 新构型网格与守恒准入。 \\
方向二：动态温控原型 & 部分完成 & 1800点简化 PID 时序及程序复核。 & 抗饱和修正与设备辨识。 \\
方向三：物理融合代理模型 & 部分完成 & 技术路线、数值与自动化资料。 & 样本集与独立测试精度。 \\
系统协同：整板与多行验证 & 未完成 & 已有几何和热源映射。 & 流体域、网格、求解及系统对照。 \\
\bottomrule\end{tabularx}
\par\smallskip\begin{minipage}{\linewidth}\footnotesize 不填完成百分比；简化 PID 结果不代表十行泵阀系统已经验证。\end{minipage}
\end{table}
"""

conclusion_list = r"""
\subsubsection{阶段性结论}
\begin{enumerate}
\item 形成了以空间适配与时间调控为起点的研究框架，并在仿真需求推动下拓展出计算加速方法方向。其价值在于明确了工程对象、动态需求与计算方法之间的关系，使后续研究能够共同服务于同一热管理问题。
\item 整理了四种流道的39个既有工况、六种翼型基准结果和17条小模型代表分支，形成结构筛选的资料基础；连接装配已有几何，但性能优势尚待独立计算。
\item 开展翼型模型、网格敏感性和压力统计核验，修正温度相关水物性并进行实现对照，使数值工作从几何生成逐步进入评价口径与可靠性控制。
\item 读取1800个采样点的简化 PID 温控时序并核查程序，为后续灰箱建模和设备辨识提供起点；保存数据同时暴露了积分限幅未进入控制更新的实现问题。
\item 已有当前整板装配与热源映射验证，支持结构与空间热源的统一配置，但整板流热性能仍须后续求解。
\end{enumerate}

上述成果分别对应研究框架、局部结构、数值方法、控制原型和系统几何准备，证据层级不同。已有资料中的局部物性实现计时属于数值实现改进，网格检验属于可靠性评价，几何装配属于工程准备，均不能替代代理模型精度或系统控制收益。当前没有已提供的论文发表、专利或实测节能成果，本报告不填写此类状态。
"""

bib = r"""
\FloatBarrier
\Needspace{27\baselineskip}
\begin{thebibliography}{99}
\bibitem{stagereports} 项目组. 阶段研究报告汇编及配套图表（内部资料）[R]. 2026. 采用本次整理时保存的版本。
\bibitem{tuckerman1981} Tuckerman D B, Pease R F W. High-performance heat sinking for VLSI[J]. IEEE Electron Device Letters, 1981, 2(5): 126--129. DOI: 10.1109/EDL.1981.25367.
\bibitem{chen2016} Chen T, Guestrin C. XGBoost: A Scalable Tree Boosting System[EB/OL]. arXiv:1603.02754, 2016. DOI: 10.48550/arXiv.1603.02754. 预印本；用于基础算法来源。
\bibitem{raissi2017} Raissi M, Perdikaris P, Karniadakis G E. Physics Informed Deep Learning (Part I): Data-driven Solutions of Nonlinear Partial Differential Equations[EB/OL]. arXiv:1711.10561, 2017. DOI: 10.48550/arXiv.1711.10561. 预印本；用于物理约束学习的方法背景。
\end{thebibliography}
\end{document}
"""

# ---------- 组装 ----------
new = pre
new += "\\section{干了什么：研究内容}\n\n"
new += "\\subsection{项目要解决的问题与目标}\n\n"
new += name_line + "\n\n"
new += p1 + "\n\n"
new += task.strip() + "\n\n"
new += bg1 + bg2 + bg3 + goal
new += evo
new += ch1_13

new += ch2_lead
new += lit
new += ch2_platform_lead
new += geom
new += load
new += eqs
new += mesh_method + "\n具体诊断结果见第三部分。\n\n"
new += udf_method
new += auto
new += metric

new += "\\FloatBarrier\n\\subsection{方向一：连接结构的设计与验证方法}\n"
new += body(conn)
new += small
new += unit
new += merged_val
new += mech

new += "\\subsection{方向二：动态调控的方法与模型}\n"
new += cdef
new += carch
new += cheat
new += pid_setup
new += pid_eq
new += cgrey

new += "\\subsection{方向三：代理模型的构建与评价方法}\n"
new += sreq
new += spar
new += sdata
new += stheo
new += sfuse
new += seval

new += ch3_lead
new += repro
new += "\\subsubsection{网格诊断结果}\n"
new += mesh_results
new += udf_results
new += "\n\\FloatBarrier\n"

new += ch3_32_lead
new += flows
new += other
new += airfoil
new += "\\subsubsection{NACA 分支结果}\n"
new += naca
new += nacav2
new += naca2420
new += csum
new += "\n\\FloatBarrier\n"

new += ch3_33_lead
new += pid_fig
new += pid_find
new += cend

new += "\\subsection{方向三：方法与数据基础}\n"
new += send

new += ch3_35_lead
new += status_table
new += dkey
new += conclusion_list
new += dcert
new += dunc

new += "\n\\section{未来计划}\n\n"
new += body(pdiff)
new += pmain
new += ptried
new += pnext_body
new += pp1
new += pp2
new += pp3
new += bib

# ---------- 月份清理 ----------
replacements = [
    ("本报告按五个逻辑月的图表和保存记录梳理阶段证据", "本报告按已保存的图表和记录梳理阶段证据"),
    ("本报告覆盖截至中期的累计研究进展；具体月度起止日期尚待确认。", "本报告覆盖截至中期的累计研究进展；具体日期尚待确认。"),
    ("但月5尚无连接段成对流热结果", "但目前尚无连接段成对流热结果"),
    ("结构、网格及控制时序按月报和保存文件核对", "结构、网格及控制时序按保存记录核对"),
    ("月1已整理方形、六边形和圆形微通道的复现结果", "已整理方形、六边形和圆形微通道的复现结果"),
    ("的月1历史复现云图", "的历史复现云图"),
    ("沿用月3原始数据", "沿用原始保存数据"),
    ("沿用月3记录", "沿用原始保存记录"),
    ("按月3相同色标", "按相同色标"),
    (
        "月1学习温度读取与物性接口并初步编写；正式 UDF 修改、编译及代表算例验证归入月3。以下流程图用于说明实现方法，不代表月1已经完成全部校验。",
        "前期学习温度读取与物性接口并完成初步编写；正式的 UDF 修改、编译及代表算例验证属于本阶段工作。以下流程图用于说明实现方法，不代表接口学习阶段已经完成全部校验。",
    ),
    ("正式修改和核验归入月三", "正式修改和核验属于本阶段工作"),
    ("月5记录连接方向及评价方法已明确", "既有记录表明连接方向及评价方法已明确"),
    (
        "月2探索常规、仿生及翼型小块；月3集中整理翼型专题与参数分组方案。",
        "前期探索了常规、仿生及翼型小块，随后集中整理了翼型专题与参数分组方案。",
    ),
    ("月5尚未形成连接段仿真结果", "目前尚未形成连接段仿真结果"),
    ("月2由热容惯性、输运滞后及执行器限幅提出", "基于热容惯性、输运滞后及执行器限幅提出"),
    ("月2提出的感知、预测、决策、执行与独立安全约束框架", "感知、预测、决策、执行与独立安全约束框架"),
    ("月3采用一阶集总温控对象与增量式 PID", "采用一阶集总温控对象与增量式 PID"),
    ("原月报3.9 K对应后半段", "原记录3.9 K对应后半段"),
    ("月报29.3\\%未由当前数组复现", "原记录29.3\\%未由当前数组复现"),
    ("逻辑月四拟承接月三翼型参数分组尝试 XGBoost，目前尚未开展", "翼型参数分组后的 XGBoost 尝试目前尚未开展"),
    ("按现有月报及保存记录核对的中期任务状态", "按现有保存记录核对的中期任务状态"),
    ("后文补入五个月报的主要图表", "后文补入既有报告的主要图表"),
    ("月1的12幅历史云图", "12幅历史云图"),
    ("月2的结构探索、月3的六翼型基准与13条翼型分支", "结构探索、六翼型基准与13条翼型分支"),
    ("当前月报尚未形成连接段成对流热结果", "当前尚未形成连接段成对流热结果"),
    ("月度起止日期尚未确认", "具体日期尚未确认"),
    ("不将全部里程碑承诺为一个月内完成", "不将全部里程碑承诺在同一阶段内完成"),
    ("月5尚无连接段成对性能结果", "目前尚无连接段成对性能结果"),
    ("月4研究不同热流密度下的小块选择分界线", "前期研究了不同热流密度下的小块选择分界线"),
    ("月5承接连接、供液及整板尝试", "连接、供液及整板尝试"),
    ("报告起止日期待确认", "截至中期检查"),
    ("% unified-five-part-outline 2026-10-23", "% midterm-stage-outline 2026-10-24"),
]
for a, b in replacements:
    new = new.replace(a, b)

new = re.sub(r"\\cite\{monthly[0-9](?:,monthly[0-9])*\}", r"\\cite{stagereports}", new)

SRC.write_text(new, encoding="utf-8")
left = [ln for ln in new.split("\n") if "月" in ln]
print("written", len(new), "chars;", "lines with 月:", len(left))
for ln in left[:25]:
    print("  ", ln.strip()[:110])
