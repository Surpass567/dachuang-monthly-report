from pathlib import Path
import re,json,csv,hashlib

SRC=Path(__file__).resolve().parent
REPORT=SRC.parents[2]
E=SRC/'evidence'
s=(SRC/'midterm_original.tex').read_text(encoding='utf8')
months={int(re.search(r'月(\d)',p.name)[1]):p.read_text(encoding='utf8') for p in (SRC/'monthly_sources').glob('*.tex')}

def fig(label,caption,path,width=r'\linewidth',height=None):
    sizing=f'width={width}'
    if height:sizing+=f',height={height},keepaspectratio'
    return '\n'+r'\begin{figure}[htbp]\centering'+'\n'+rf'\includegraphics[{sizing}]{{figs/{path}}}'+'\n'+rf'\caption{{{caption}}}\label{{{label}}}'+'\n'+r'\end{figure}'+'\n'

def table_from(month,label,prefix):
    blocks=re.findall(r'\\begin\{table\}.*?\\end\{table\}',months[month],re.S)
    b=next(b for b in blocks if r'\label{'+label+'}' in b)
    b=b.replace('[H]','[htbp]')
    return re.sub(r'\\(label|ref|eqref)\{([^}]+)\}',lambda m:'\\'+m[1]+'{'+prefix+m[2]+'}',b)+'\n'

def replace_placeholder(label,new):
    global s
    lines=s.splitlines(keepends=True)
    found=0
    for i,line in enumerate(lines):
        if line.startswith(('\\placeholderfigure{'+label+'}','\\placeholderpair{'+label+'}')):
            lines[i]=new+'\n';found+=1
    assert found==1,(label,found)
    s=''.join(lines)

def replace_table(label,new):
    global s
    pattern=r'\\begin\{table\}.*?\\end\{table\}'
    blocks=list(re.finditer(pattern,s,re.S))
    b=next(b for b in blocks if r'\label{'+label+'}' in b[0])
    s=s[:b.start()]+new+s[b.end():]

def replace_subsub(title,new):
    global s
    pattern=r'\\subsubsection\{'+re.escape(title)+r'\}.*?(?=\\subsubsection\{|\\subsection\{|\\section\{)'
    s,n=re.subn(pattern,lambda _:r'\subsubsection{'+title+'}\n'+new+'\n',s,flags=re.S)
    assert n==1,title

# Make the source self-contained with report-native figure paths.
s=re.sub(r'figures/diagrams/(fig_\d+\.pdf)',r'figs/midterm_diagram_\1',s)
s=s.replace(r'\begin{thebibliography}{9}',r'\begin{thebibliography}{99}')
s=s.replace('已形成局部结构验证与最小闭环基础，正在完善动态模型、数据集和系统级证据。','已整理结构复现、小模型、物性对照及网格诊断证据，完成简化 PID 仿真；连接与整板性能仍需独立验证。')

# Resolve status inconsistencies against the monthly artifacts, without claiming new CFD.
paragraphs={
'在区域化连接结构方面，已确定连接方案，依据团队阶段进展说明，已有数值仿真对照验证其性能优势，相关研究接近阶段性完成，当前重点为对照数据归档、最终性能评价与机理解释。':'在区域化连接结构方面，已有方案库和40 mm条带装配，已完成几何检查；月4尚无连接段成对性能结果，当前不能报告其换热或压降改善幅度。',
'动态调控方面，已形成十行单向流路、双泵和行级出口阀门的基本架构，开展随机变化热源模拟并完成最小闭环的初步可行性验证。':'动态调控方面，已形成十行单向流路、双泵和行级出口阀门的基本架构，并保存了一阶温控对象上的增量式 PID 仿真数据；其抽象执行量尚未标定为实际泵阀流量。',
'本报告依照项目真实演化过程梳理问题、方法与阶段证据，并区分局部连接验证、装配几何准备及整板系统验证的不同层级。':'本报告按五个逻辑月的图表和保存记录梳理阶段证据，区分局部单元计算、连接装配准备与整板系统验证。',
'下一阶段将完成连接结构成果整理，':'下一阶段将完成连接结构成对计算与成果整理，',
'总体任务是完成区域化连接结构的阶段性验证、建立动态反馈研究基础，并为高保真数据驱动的快速预测方法建立可靠数值平台。':'总体任务是整理局部结构及数值可信度证据、建立动态反馈研究基础，并为连接结构验证和高保真数据驱动预测建立可靠数值平台。',
'方案确定；已有局部对照支持优势；最终量化与机理待归档。':'已有候选方案与装配几何；尚缺连接段独立成对性能结果。',
'最小闭环初步可行；物理模型与多算法比较正在推进。':'已有简化 PID 仿真与时序；设备辨识及多行控制验证待开展。',
'方向二已有确定方案与局部仿真验证，是目前最接近阶段收尾的方向；方向三已实现基本反馈可行性，正在深化物理模型；':'方向二已积累局部单元性能和连接装配资料，连接本身的优势仍需成对计算；方向三已保存简化反馈仿真，正在明确物理模型和设备接口；',
'分区、连接方案确定、局部数值对照支持优势':'局部结构筛选、连接候选与条带装配',
'最终量化归档、关键参数与机制；接近阶段完成。':'连接基准、统一工况及成对流热结果待补。',
'动态框架、双泵行阀方案、热源模拟、最小闭环初步验证':'动态框架、双泵行阀方案、简化对象 PID 仿真',
'连接优势和最小闭环阶段事实来自团队说明，原始成对数据与闭环日志待补；不以文件数量计算完成率。':'结构、网格及控制时序按月报和保存文件核对；简化 PID 结果不代表十行泵阀系统已经验证。',
'第二，完成区域化基本单元、连接方案及局部验证，取得了团队已确认的性能优势，下一步是将其转化为数据与机理完整的阶段结果。':'第二，整理了四种流道的39个既有工况、六种翼型基准结果和17条小模型代表分支，形成结构筛选的资料基础；连接装配已有几何，但性能优势尚待独立计算。',
'第四，建立动态热源与反馈控制的初步研究基础，验证最小闭环的可行性，为后续物理灰箱与算法比较提供起点。':'第四，读取1800个采样点的简化 PID 温控时序并核查程序，为后续灰箱建模和设备辨识提供起点；保存数据同时暴露了积分限幅未进入控制更新的实现问题。',
'已有量化记录见表~\\ref{tab:key_results}；具体统计口径、原始数值和适用边界见后续数值平台与结构部分。以下数据均来自原报告，不表示新增求解结果。':'已有量化记录见表~\\ref{tab:key_results}；后文补入五个月报的主要图表、保存数组的只读复核及现有物性验证资料。本次整理没有推进 Fluent 求解。',
'最细档时间步历史有差异，全序列未通过联合判据。':'统一以323万档为比较参考；294万档压降差0.3201%，461万档4.2751%。',
'局部连接方案已有团队确认的定性优势，当前整板则仅完成几何准备；两者成熟度不同。后续必须分别完成局部成对结果归档和整板流热求解，不能将局部优势直接推广为系统收益。':'局部小模型已有温度与水力结果，连接段和当前整板则主要具备几何准备。后续必须分别完成连接成对对照和整板流热求解，不能将局部单元表现直接推广为连接或系统收益。',
'项目已完成整体分区与单元设计思路，形成不同负荷类别的结构配置路径；已确定连接方案，并根据团队阶段说明取得仿真对照支持的性能优势。现阶段研究已由概念方案进入性能验证与结果整理，接近阶段性完成。本章重点展示这一实质进展，同时保留尚未归档的对照数据和适用边界。':'项目已有整体分区与单元设计思路、代表性小模型计算和连接方案库。月4记录连接方向及评价方法已明确，但尚无连接段成对仿真结果；几何装配资料进一步说明可采用六片梭形导叶连接，未提供相同主体、相同工况下的连接收益。以下先整理已具备的单元结果，再说明连接验证的输入与缺口。',
'当前可以确认的是方案已确定、已有局部仿真支持优势；尚不能确认优势体现为哪些指标同时改善、其幅度多大、是否覆盖全部负荷与流量。':'当前可以确认的是已有连接候选和可追溯装配；尚不能确认连接本身能否改善指定指标、其幅度及适用负荷范围。',
'已有局部仿真支持优势为团队提供的阶段事实；本表具体量化尚待原始对照归档。':'局部单元性能已在前文给出；本表专用于连接段成对验证，不能用不同主体或不同工况的小模型数据代填。',
'当前已形成基本架构并完成最小闭环初步验证，尚未形成完整的多场景控制性能数据。':'当前已有基本架构和简化对象上的 PID 闭环时序，尚未形成实物泵阀或多行耦合系统的完整性能数据。',
'积分抗饱和、微分滤波和离散实现是后续配置，不表示当前最小闭环一定采用此完整形式。':'该式用于说明连续形式；已有程序采用增量更新，累计误差限幅没有实际进入控制更新，需先修正并复核后再评价抗饱和效果。',
'已完成工作包括基本动态研究框架、双泵与行级阀门方案、动态热源模拟、最小闭环初步可行性验证及数学模型路线。':'已开展基本动态研究框架、双泵与行级阀门方案、简化对象的周期扰动 PID 仿真及数学模型路线；当前控制数据不能证明实际泵阀链条已打通。',
'当前正在明确输入参数、建立合格样本集、推进理论尺度分析和 XGBoost 等基础方法研究。':'目前17条小模型代表分支及37条原始提取记录可用于来源整理，但工况、时刻与物性尚未统一，不能直接宣布形成37个合格训练样本；仍需明确输入、筛选样本并开展基础方法研究。',
}
for old,new in paragraphs.items():
    if old in s:s=s.replace(old,new)

replace_table('tab:monthly_status',r'''
\begin{table}[htbp]\centering\small
\caption{按现有月报及保存记录核对的中期任务状态}\label{tab:monthly_status}
\begin{tabularx}{\linewidth}{@{}Y c Y@{}}\toprule
\rowcolor{ydzjlight} 任务 & 状态 & 已有证据及下一步 \\\midrule
局部结构复现与筛选 & 已有结果 & 三类复现云图；四种流道39工况；六翼型及17条小模型分支。\\
物性实现与数值诊断 & 阶段完成 & 1601点拟合核对、共同0.137 s实现对照、七档网格与出口诊断；非全工况验证。\\
连接段及流路集成 & 部分完成 & 有候选、40 mm条带与整板几何；连接段成对性能仍待计算。\\
动态温控原型 & 部分完成 & 1800点简化 PID 时序；物理对象、泵阀标定与抗饱和实现待完善。\\
物理融合代理模型 & 部分完成 & 路线与数值资料已有；尚无独立训练测试精度。\\
整板与多行协同验证 & 未完成 & 已有几何和热源映射；流体域、网格、求解及系统对照待开展。\\
\bottomrule\end{tabularx}\end{table}
''')

# Remove two old status diagrams that imply completed connection verification.
s=re.sub(r'^\\reportfigure\{fig:(?:04|29)\}.*\n','',s,flags=re.M)
s=s.replace(r'图\ref{fig:04}',r'表\ref{tab:15}').replace(r'图\ref{fig:29}',r'表\ref{tab:monthly_status}')

# Add a month-to-evidence map, including months that contain plans only.
mapping=r'''
\subsubsection{五个逻辑月的成果承接}
五份月报按研究推进顺序组织，并不对应已确认的自然月。表~\ref{tab:mid_month_map}
将已有成果接入中期报告：月1提供复现与方法基础，月2提供结构筛选数据，月3提供
数值可信度与流场诊断，月4和月5主要限定连接及整板的后续验证要求。
\begin{table}[htbp]\centering\small
\caption{月报图表在中期报告中的承接}\label{tab:mid_month_map}
\begin{tabularx}{\linewidth}{@{}c Y Y@{}}\toprule
\rowcolor{ydzjlight} 逻辑月 & 可纳入的图表与资料 & 本报告中的作用 \\\midrule
1 & 方形、六边形、圆形的12幅复现云图；UDF接口图；分层控制框架 & 几何及后处理能力、物性检查流程和控制思路。\\
2 & 四流道与六翼型表；17条代表分支；两组网格与温度图；PID工况表 & 温度与水力代价权衡、工况标识和初步温控量级。\\
3 & 七档网格原值、323万参考误差、换热流阻、内部流场与出口回流图 & 参考网格的适用边界及统计口径核查。\\
4 & 连接设计目标、前置条件和控制接口表 & 构建连接段压降、供液均匀性与模型辨识任务。\\
5 & 整板验证五项内容、前置条件及计划表 & 统一温度、流量、能效和控制的系统验收路线。\\
\bottomrule\end{tabularx}\end{table}
上述资料按研究对象分组，不将重复网格、不同保存时刻或同一文件的归档副本算作独立结构；
月4、月5的任务表也不转写成已完成性能结果\cite{monthly1,monthly2,monthly3,monthly4,monthly5}。
'''
s=s.replace(r'\subsection{关键结果}',mapping+'\n'+r'\subsection{关键结果}',1)

# Existing geometry and actual CAD assembly replace empty figure slots.
replace_placeholder('fig:05',fig('fig:05','当前40 mm整板在 z=1.5 mm 的实际 CAD 截面：70个低负荷、27个中负荷、3个高负荷模块。此图为几何与映射核对，不是整板温度场。','midterm_whole_plate.png',r'.88\linewidth','145mm'))
s=s.replace('图\\ref{fig:05}和图\\ref{fig:06}分别预留整体布局和局部结构图。','图\\ref{fig:05}展示实际整板截面，图\\ref{fig:06}展示可追溯连接装配局部。')
replace_placeholder('fig:06',fig('fig:06','40 mm条带装配的接缝放大：主体、六片梭形导叶及内部0.5 mm、端部0.25 mm连接。图注热流为后续主体工况配置，未表示条带已经完成求解。','midterm_joint_detail.png',r'.86\linewidth','155mm'))
s=s.replace('图\\ref{fig:07}用于明确边界位置，不能仅以方程替代实际边界设置。','实际边界配置见表\\ref{tab:03}；代表算例与整板规划分别记录，不能仅以控制方程替代实际边界。')
replace_placeholder('fig:07','')

# Month 1 reproduction: reuse all twelve original panels, grouped for readability.
reproduction=r'''
\subsubsection{三类流道复现与后处理基础}
月1已整理方形、六边形和圆形微通道的复现结果，形成水侧中截面温度、静压、速度及铜基板温度
共12幅云图。表~\ref{m1:tab:repro}列出复现关注点；
图~\ref{fig:repro-square}至图~\ref{fig:repro-round}保留原图的坐标、色标和遮罩。
这些图用于说明已完成建模、求解与后处理流程，不将不同几何和历史工况的色标直接用于结构排序。
部分历史温度图的高温区超出当前280--360 K拟合温区，因此也不作为当前变物性单相算例的准入证据。
'''+table_from(1,'tab:repro','m1:')
names=['temperature_midplane','pressure_midplane','speed_midplane','copper_base_temperature']
for j,(label,cn) in enumerate([('square','方形'),('hex','六边形'),('round','圆形')]):
    reproduction+=r'\begin{figure}[p]\centering'+'\n'
    for k,(name,cap) in enumerate(zip(names,['水侧温度','水侧表压','水侧速度大小','铜基板温度'])):
        fn=f'{4*j+k+1:02}_{name}.png'
        reproduction+=r'\begin{subfigure}[t]{.48\linewidth}\centering'+'\n'+rf'\includegraphics[width=\linewidth]{{figs/{fn}}}\caption{{{cap}}}'+r'\end{subfigure}'
        reproduction+=r'\hfill'+'\n' if k%2==0 else '\n'+r'\vspace{2mm}'+'\n'
    reproduction+=rf'\caption{{{cn}微通道的月1历史复现云图。水侧取 $Y=0.150$ mm，铜基板取 $Y=0.025$ mm；保留各图原色标，不能由颜色直接比较不同工况。}}\label{{fig:repro-{label}}}'+'\n'+r'\end{figure}'+'\n'
reproduction+=r'\FloatBarrier'+'\n'
s=s.replace(r'\subsubsection{CFD数值模型与基本控制方程}',reproduction+r'\subsubsection{CFD数值模型与基本控制方程}')

# Update mesh reference consistently with the latest month 3.
replace_placeholder('fig:08',fig('fig:08','NACA2416 v3三档实际流固界面面网格，统一取 z=0.25 mm。下排采用相同局部范围；此图不等同于三维边界层截面，单元总数增大也不保证每一局部区域同步加密。','midterm_naca_mesh_actual.png'))
replace_placeholder('fig:09',fig('fig:09','NACA2416在0.2 s的七档网格温度与静压差，沿用月3原始数据。','month3_mesh_temperature_pressure.png'))
start='记录显示，2943269 与 3235081 单元之间的静压差相对变化较小，'
a=s.index(start);b=s.index(r'\subsubsection{温度相关物性UDF与非均匀热源设置}',a)
mesh=r'''
本阶段统一以 $N_{\mathrm{ref}}=3\,235\,081$ 为比较参考，按
$e_{\phi,i}=|\phi_i-\phi_{\mathrm{ref}}|/|\phi_{\mathrm{ref}}|\times100\%$ 计算差异；
参考档并非精确解，参考档自身差异为零也不能证明网格无关。
表~\ref{m3:tab:mesh_ref323}和图~\ref{fig:mesh-errors}均采用同一分母。
'''+table_from(3,'tab:mesh_ref323','m3:')+r'''
294万档相对323万档的平均温度、最高温度和压降差异分别为0.0239\%、0.0057\%和0.3201\%，
对应绝对差约0.0726 K、0.0198 K和7.518 Pa；该局部区间较接近。
152万档压降差异仍为1.7722\%，461万档为4.2751\%，所以不沿用月4、月5前置条件中
“约150万网格已验证”的旧表述。当前323万档用于诊断与成本折中，尚未成为全部新构型的通用生产网格。
流体侧 $D_h=2.8070$ mm、$L=3.5$ mm时，323万档 $Nu=175.818$、
$h_c\approx38210.0$ W/(m$^2$·K)；294万档二者差异约0.11\%，461万档约1.54\%，
$f_D$差异约4.28\%。$Re\approx6603$只用于记录该特征尺度下的流动量级，
并不单独证明层流模型在全部参数范围有效，后续还需结合扰流结构和流动形态复核。
'''+fig('fig:mesh-errors','温度、压降及换热流阻指标统一以323万档为参考的相对差异，虚线为1%比较线。','month3_mesh_errors_ref323.png')+fig('fig:mesh-dimensionless','七档网格的换热与流阻指标；特征尺度、物性参考温度及热流统计沿用月3记录。','month3_mesh_dimensionless.png')+r'''
图~\ref{fig:mesh-flow}与图~\ref{fig:mesh-outlet}按月3相同色标比较323万与461万档。
前者显示 $z=1.50$ mm平面的主流向速度、投影流线、温度与静压；投影流线并非完整三维轨迹。
后者显示出口法向速度和温度。两档出口回流面积比例分别为5.1720\%和5.3886\%，
回流质量流量占入口流量分别为0.4754\%和0.2777\%；回流面积扩大而回流质量减少，
不能概括为461万档的回流整体更严重。两档回流面质量加权温度均为305 K。
'''+fig('fig:mesh-flow','323万档（上排）与461万档（下排）的中高平面速度、投影流线、温度和静压。','month3_mesh_flowfield.png')+fig('fig:mesh-outlet','323万档（上排）与461万档（下排）的出口速度和温度。出口局部回流与内部尾迹分开识别。','month3_mesh_outlet.png')+r'''
同区域体积加权温度为305.7793 K与305.8673 K，相对323万档差约0.0288\%，
远小于单元算术平均的0.5537\%；这说明平均方式和网格统计权重会显著影响结论。
尚未进行统一时间推进历史、出口延长或回流温度敏感性重算，因此不能将压降差异直接归因于单一出口因素。
GCI外推与两档相对差异也需区分：以323万为细档的107万／152万／323万组合压降形式GCI为0.7275\%，
表观阶约5.57；这不证明所有输出均已进入可信渐近区间\cite{monthly3}。
'''
s=s[:a]+mesh+s[b:]
s=s.replace('图\\ref{fig:08}和图\\ref{fig:09}用于补入局部网格与响应曲线。','图\\ref{fig:08}给出统一平面的实际面网格，图\\ref{fig:09}给出已有响应曲线。')
s=s.replace('来源：evidence/mesh\\_results\\_02s.csv。','来源：配套源码目录内 evidence/mesh\\_results\\_02s.csv。')

# UDF learning and independent implementation evidence.
udf=r'''
\paragraph{从接口学习到数值自检}
月1整理了温度读取、物性返回、编译加载、材料挂接与按需自检的流程。
密度、黏度、导热系数采用 \texttt{DEFINE\_PROPERTY} 和 \texttt{C\_T(c,t)}；
比热采用 \texttt{DEFINE\_SPECIFIC\_HEAT}，同时返回 $c_p(T)$ 和其积分显焓，满足
$\mathrm dh/\mathrm dT=c_p$。编译通过只说明接口可用，仍需检查适用温区、数值与变化趋势。
图~\ref{fig:udf-interface}承接这一学习过程。
'''+fig('fig:udf-interface','水物性 UDF 的温度输入、函数接口、材料挂接与自检流程，采用月1已有图。','udf_learning_interfaces.png')+r'''
\paragraph{已有拟合精度和同一时刻求解对照}
补充资料在280--360 K、101325 Pa下核对1601个温度点。
密度、动力黏度、导热系数和比热的最大相对拟合误差分别为
0.0000151\%、0.0005164\%、0.0001216\%和0.0002054\%。
图~\ref{fig:udf-curves}保留原公式、REFPROP参考与最终拟合曲线；
图~\ref{fig:udf-fit-error}给出逐项最大误差。这是对同一参考物性的拟合检验，不等于物理模型的实验精度。
月1、月3所述298.15 K密度偏低60.8\%与现有逐点公式核查表不一致：
该表中原公式密度为999.999985 kg/m$^3$，参考为997.047637 kg/m$^3$，偏高约0.2961\%。
现阶段保留来源差异，不继续沿用60.8\%作为当前已核实误差；后续需核对历史源码版本。
'''+fig('fig:udf-curves','四项水物性随温度的变化：参考、原公式与最终REFPROP拟合版。排查候选公式与最终拟合版分别保留，不混用。','midterm_udf_01_四项物性温度曲线.png')+fig('fig:udf-fit-error','1601温度点核对记录中的四项最大相对拟合误差。','midterm_udf_03_1601点拟合误差.png')+r'''
在共同0.137 s时刻，拟合与实时REFPROP实现的固体最高温度分别为332.6852693 K和332.6852725 K，
加热面最高温度分别为332.8039186 K和332.8039218 K；
进出口面积平均静压差分别为4290.169554 Pa和4290.159872 Pa。
共同前37步的求解及残差读取耗时分别为5.653 min和64.986 min，实时接口约为拟合版的11.50倍。
拟合分支最终到0.2 s，实时分支到0.137 s，因此末态文件不能直接逐点对比。
图~\ref{fig:udf-common}和图~\ref{fig:udf-time}分别保留共同时间段和共同步数口径。
'''+fig('fig:udf-common','相同初场和时间步下两种物性实现的共同时间段对照。','midterm_udf_04_同一时段求解结果.png')+fig('fig:udf-time','共同前37步的求解及残差读取耗时；不是不同总步数或代理模型的加速比较。','midterm_udf_05_共同37步计算耗时.png',r'.8\linewidth')
s=s.replace(r'\subsubsection{数值仿真自动化流程}',udf+r'\subsubsection{数值仿真自动化流程}')
replace_placeholder('fig:10',r'\noindent 空间热源对应图~\ref{fig:05}中的实际模块分类；实际区域动态热源序列尚待补入，不能由静态热流等级代替时间变化。')
s=s.replace('图\\ref{fig:10}预留空间和时间热源说明。','空间映射见图\\ref{fig:05}；实际区域动态轨迹仍待归档。')

# Reuse all quantitative month 2 model branches, preserving their condition notes.
m2=months[2]
a=m2.index(r'\textbf{（一）四种流道在共同热流密度下的比较}')
b=m2.index(r'\textbf{（三）控制回路仿真}')
small=m2[a:b]
small=re.sub(r'\\(label|ref|eqref)\{([^}]+)\}',lambda m:'\\'+m[1]+'{m2:'+m[2]+'}',small)
small=small.replace(r'\cite{smallmodels}',r'\cite{monthly2}')
small=small.replace('我补充整理了','团队补充整理了').replace('我进一步整理了','团队进一步整理了')
small=small.replace('[H]','[htbp]').replace(r'\par\needspace{17\baselineskip}','')
small=small.replace('努塞尔数提高约 5.7\\%。','表列换热系数由756.6增至798.5 W/(m$^2$·K)，提高约5.54\\%。')
small=small.replace('本次新增的 17 条代表结果与源文件对应关系已整理到小模型汇总数据中','17条代表结果与源文件对应关系已保留在配套数据中')
small=r'''\subsubsection{局部结构筛选与小模型结果}
月2首先建立温度和水力代价的比较口径，再从常规流道推进到翼型与仿生结构。
下面保留历史共同热流工况、六翼型基准以及17条已保存代表分支，
分别注明平均温度定义和时间、流量、物性条件；这些结果用于筛选后续同工况对照对象\cite{monthly2}。
'''+small+r'''
上述结果不能转写为连接导叶的性能收益。后续先固定热负荷、入口流量或泵功、物性和统计时刻，
再比较温度与压降；同一模型的网格、物性和时间步分支保留为验证记录，不重复计为新几何样本。
\FloatBarrier
'''
s=s.replace(r'\subsubsection{基本单元与连接结构}',small+r'\subsubsection{基本单元与连接结构}')
replace_placeholder('fig:13',fig('fig:13','四条40 mm装配的实际内部截面，包含gao2.1、翼型、直线及混合排列；用于几何准备和接口检查。','midterm_strip_overview.png',r'\linewidth','125mm'))

replace_subsub('连接结构的数值验证',r'''
月4尚未形成连接段仿真结果，当前可核对的是设计目标、候选方案与装配几何。
局部小模型温度和水力性能不能代替连接段“有／无整流”的成对验证。
下一步需在相同主体、相同热负荷和相同入口约束下，比较连接前后截面的流量、速度均匀性与压降，
并输出下游受热面温度。若采用固定泵功，应由各自水力特性确定运行点，不能只固定入口流量后宣称等泵功改善。
现有条带几何可作为计算输入，但仍需流体域、共享拓扑、网格和守恒检查\cite{monthly4}。
''')
for label in ['fig:15','fig:16','fig:19','fig:27','fig:28','fig:22','fig:23']:
    replace_placeholder(label,'')
s=s.replace('图\\ref{fig:15}和图\\ref{fig:16}对应压力代价与热响应两个维度。','表\\ref{tab:09}同时保留压力代价与热响应两个维度。')
s=s.replace('图\\ref{fig:19}将以同一时间轴对应真实负荷与温度。','后续应以同一时间轴保存真实区域负荷与温度；已有简化 PID 的温度信号不等同于区域热流时序。')
s=s.replace('图\\ref{fig:22}与图\\ref{fig:23}对应几何定义和数值解析能力。','代表翼型排布见图\\ref{m2:fig:naca-small}，NACA2416统一平面的实际网格见图\\ref{fig:08}；这些图没有提供全部弦长、柱高和边界层参数，后续仍需对应几何文件核对。')
s=s.replace('图\\ref{fig:27}预留独立预测和泛化结果，目前尚无可填入的训练精度。','目前尚无可填入的独立预测与泛化结果，不以空白结果图替代模型验证。')
s=s.replace('表\\ref{tab:14}和图\\ref{fig:28}用于记录后续实测成本，当前保持占位。','表\\ref{tab:14}记录后续实测成本，当前尚无代理模型计时，保留为任务表。')
s=re.sub(r'^\\reportfigure\{fig:17\}.*\n','',s,flags=re.M)
s=s.replace('图\\ref{fig:17}概括几何、流动、热响应与能耗之间的分析链条，图中的因果箭头应由对照结果支持。','几何、流动、热响应与能耗之间的关联需由成对结果支持，当前不以示意箭头替代连接机理证据。')
replace_subsub('当前完成情况与成果总结',r'''
方向二已有三类复现、四流道与六翼型基准、17条小模型分支以及连接装配准备。
温度和水力代价的权衡已有局部数据支持，但连接段本身的改善尚未形成成对结果。
下一步应优先固定基准连接、主体、入口条件和物性版本，再完成流场、压降及受热面指标，
将局部筛选与连接验证分别归档。40 mm条带和40 mm整板装配提供几何对象，不能代替系统计算。
''')

# Replace empty minimal-loop placeholders with the real stored PID records and code audit.
pid=r'''
月2采用一阶集总温控对象与增量式 PID，保存1800个采样点，采样周期0.05 s，时间坐标0--89.95 s。
热源输入是 $82\pm12$ $^\circ$C、周期15 s的\textbf{温度信号}，不是 W/cm$^2$ 表示的区域热流；
程序以经验加热系数0.45和随执行量变化的冷却系数0.03--0.20推进温度。
因此，该算例验证抽象冷却动作下的闭环逻辑，不是耦合 Fluent、实物双泵或十行阀门的系统验证。
图~\ref{fig:20}直接由已有数组重绘，表~\ref{tab:11}按明确统计窗口复核\cite{monthly2}。
'''+fig('fig:20','已有简化 PID 温控数组的只读复核。上图为温度扰动与被控温度，中图为限幅执行量，下图为开关累计误差限幅时的累计值；不表示实物流量。','midterm_pid_verified.png',r'.9\linewidth','150mm')+r'''
\begin{table}[htbp]\centering\small
\caption{保存 PID 时序的工况与复核指标}\label{tab:11}
\begin{tabularx}{\linewidth}{@{}Y Y Y@{}}\toprule
\rowcolor{ydzjlight} 项目 & 数值或状态 & 统计与适用范围 \\\midrule
设定值／初始温度 & 68／50 $^\circ$C & 首个保存温度为更新后50.67625 $^\circ$C。\\
离散增益／采样周期 & $K_p=8.0,K_i=0.5,K_d=2.0$；0.05 s & 增量更新的已有参数，不直接等同连续增益。\\
全时段温度范围 & 50.6763--72.0657 $^\circ$C & 相对68 $^\circ$C全时段最大偏高4.0657 K。\\
后半时段峰值偏高 & 3.8865 K & 月报3.9 K对应后半段45--89.95 s，不是全程峰值。\\
执行量范围与均值 & 0--100\%；均值54.3705\% & 为经验模型抽象动作，未标定为泵速或流量。\\
上限采样占比 & 28.9444\% & 以保存数组 $U\ge100-10^{-10}$ 逐点统计；月报29.3\%未由当前数组复现。\\
累计误差峰值 & 限幅100；不限幅1052.6016 & 仅记录累计量变化，不能单独证明抗饱和有效。\\
开关限幅后的温度／执行量差 & 两者最大绝对差均为0 & 当前程序没有将该累计量用于增量更新。\\
\bottomrule\end{tabularx}\end{table}
原程序先更新并限幅累计误差变量，随后用当前和前两步误差直接计算增量，未使用被限幅的累计值。
因此两组保存的温度和执行量完全相同，现有结果不能支持“积分限幅已改善超调”的结论。
后续需将抗饱和反馈或条件积分接入实际控制更新，再与相同扰动、初态和模型下的基准比较。
当前峰值仍受经验冷却能力上限影响，但不能据此量化真实泵阀系统的结构性超调或节能收益。
'''
a=s.index(r'\subsubsection{初步数学模型与最小闭环验证}')
b=s.index('基础 PID 可写为',a)
s=s[:a]+r'\subsubsection{初步数学模型与最小闭环验证}'+'\n'+pid+'\n'+s[b:]

# Carry month 1's control design insight without assuming every claimed relationship is universal.
control_intro=r'''
月1由热容惯性、输运滞后及执行器限幅提出分层递阶与独立约束的控制框架，
见图~\ref{fig:control-month1}。感知、预测、决策和执行是功能划分，
其中预测和增益调度仍属方案；当前量化证据来自后文简化 PID，而非全部层级已经实现。
流量相关换热与泵送成本需由实际通道和设备特性辨识，不能把幂律指数或泵功立方关系视为所有流况的既定结论。
'''+fig('fig:control-month1','月1提出的感知、预测、决策、执行与独立安全约束框架，作为后续系统架构方案。','13_控制框架框图.png')
s=s.replace(r'\subsubsection{双泵与行级阀门控制架构}',control_intro+r'\subsubsection{双泵与行级阀门控制架构}')

# The later monthly reports define the verification scope rather than completed results.
system=r'''
\subsection{承接月4和月5的连接与整板验证要求}
月4强调连接段引入的新阻力、并联供液不足与串联入口升温；月5把整板验证分解为五项内容。
结合已保存的40 mm几何，表~\ref{tab:system_checks}将这些计划整理为可检查的后续证据。
当前整板尚未完成流体域提取、共享拓扑、网格及求解，不能报告温度均匀性或泵功改善。
\begin{table}[htbp]\centering\small
\caption{连接与整板的验证项目、指标及缺口}\label{tab:system_checks}
\begin{tabularx}{\linewidth}{@{}Y Y Y@{}}\toprule
\rowcolor{ydzjlight} 验证内容 & 统一评价方式 & 当前输入与待补证据 \\\midrule
分区是否有效 & 同受热面最高温、极差、面积标准差 & 已有70/27/3几何映射；需整板温度场及均匀布置基准。\\
流动分配是否合理 & 支路流量偏差、入口均匀性、连接压降占比 & 已有连接几何；需各行流量和连接前后截面数据。\\
能效是否可接受 & 相同热源与约束下的水力功、必要时电功 & 需系统压差、体积流量与设备效率；不由局部压降直接推电耗。\\
是否优于单一流道 & 同整板尺寸、负荷与泵功下比较 & 单元数据已有，整板独立基准与复合方案均需计算。\\
控制是否可落地 & 执行器至流量、流量／水温至反馈温度的独立辨识 & 简化 PID 时序已有；实际泵阀特性、采样与多行响应待补。\\
\bottomrule\end{tabularx}\end{table}
网格前置条件采用本报告323万参考档的有限适用结论；月4、月5的“约150万网格”不作为新工况验收依据。
物性对照已有代表算例记录，但不能据此认定40 mm条带与整板已经挂接并完成计算\cite{monthly4,monthly5}。
'''
s=s.replace(r'\subsection{三个方向的协同与系统级验证路线}',system+r'\subsection{三个方向的协同与系统级验证路线}')

# Rewrite the cumulative conclusion so it agrees with the new evidence throughout.
start=s.index(r'\subsection{可以确定的}',s.index(r'\section{阶段性结论}'))
end=s.index(r'\subsection{尚不能确定的}',start)
s=s[:start]+r'''
\subsection{可以确定的}
已有成果可以沿“复现与物性学习—局部结构比较—数值诊断—连接装配—系统验证计划”串联。
月1的12幅历史云图说明已具备三类结构复现和后处理基础；月2的39个既有工况、六翼型基准与17条代表分支
呈现温度与水力代价的权衡。不同物性、流量、保存时刻和平均温度定义分别保留，不据此给出跨工况统一排序。

数值可信度已有可追溯记录：REFPROP拟合1601点最大误差低于0.00052\%，共同0.137 s的实现差异很小，
共同37步的接口计时比约11.50；它们支持限定条件下的拟合和实现一致性。
七档网格统一以323万为参考后，294万档三项温度压降差异均低于1\%，461万档压降仍相差4.2751\%；
不能将局部接近解释为全部网格或全部构型无关。

简化 PID 已保存1800点时序，全程温度为50.6763--72.0657 $^\circ$C，后半程峰值偏高3.8865 K。
代码复核显示累计误差限幅未接入控制增量，两组温度和执行量完全一致；
后续首先修正并核验抗饱和实现，再进行设备辨识与多行控制比较。

连接和整板已有候选、条带与40 mm装配几何，热源映射的数量和覆盖功率已有核对。
当前月报尚未形成连接段成对流热结果或整板性能，因此相关改善幅度仍属于待验证内容。
代理模型已有研究路线和数值资料，尚无独立测试精度、泛化与累计加速收益。
下一阶段以连接对照、合格样本准入、动态对象辨识与整板独立求解为可检查里程碑。
''' +s[end:]
s=s.replace('局部连接优势的最终幅度及其整板适用性：缺少已归档的最终成对指标与统一对象上的系统求解。','连接结构是否改善指定指标及其整板适用性：缺少同主体、同工况成对结果与系统求解。')
s=s.replace('动态控制的温度改善与泵送代价：缺少完整控制日志、可辨识参数及相同扰动下的对照评价。','实际动态控制的温度改善与泵送代价：已有简化时序，但抗饱和、设备标定及多行对照仍需验证。')
s=s.replace('动态建模方面，已开展随机热源模拟并实现最小闭环的初步验证；','动态建模方面，已保存周期温度信号下的简化 PID 时序；')
s=s.replace('连接成果证据闭合','连接成对计算与归档')
s=s.replace('首先完成方向二的最终几何版本与成对结果归档','首先确认方向二的对照几何并完成成对计算与结果归档')
s=s.replace('同步归档最小闭环的热源、控制和温度序列。','同步修正简化 PID 抗饱和实现，并完善热源、控制和温度序列。')

# Report all added data in a concise summary table too.
summary_row=r'静态热源布局 & 低/中/高负荷为 70/27/3 格 & 整格加热 2640 W；仅主体加热 2021.25 W。\\'
s=s.replace(summary_row,summary_row+'\n'+r'局部模型整理 & 17条代表分支、37条原始提取记录 & 非17种独立结构；各分支工况、物性和时刻分别标识。\\'+'\n'+r'简化 PID 时序 & 1800点，0.05 s间隔；全程最高72.0657 $^\circ$C & 温度信号扰动；累计误差限幅未接入控制更新。\\')

refs='\n'.join(rf'\bibitem{{monthly{i}}} 项目组. 逻辑月{i} {title}. 项目月度报告及配套图表, 2026. 采用本次整理时保存的版本，逻辑月不等同自然月。' for i,title in [(1,'基础建立'),(2,'指标与形态'),(3,'形态与物理'),(4,'连接成网络'),(5,'整板验证')])
s=s.replace(r'\bibitem{tuckerman1981}',refs+'\n'+r'\bibitem{tuckerman1981}')
# Avoid legacy notes that still imply a completed physical minimal loop.
s=s.replace('最小闭环的初步验证','简化闭环的初步验证')
s=s.replace('最小闭环的初步可行性验证','简化闭环的初步可行性验证')
s=s.replace('已完成的自动化基础为流程初步贯通','已有自动化基础为流程初步贯通')
s=s.replace('现有阶段说明表明，连接方案已确定且性能优势获得仿真支持，研究重点由方案是否可行转向最终结果归档和机制解释。','现有月报支持连接设计目标与装配版本已明确，但连接段的成对流热结果尚待计算；当前重点是固定基准和工况，建立可复核的性能对照。')
s=s.replace('已有阶段说明表明连接方案已确定且性能优势获得仿真支持，研究重点由方案生成逐渐转向结果收敛、对照归档与机理解释。','已有连接装配几何可支持后续计算输入，但月4尚无连接段成对流热结果；当前研究重点是固定对照几何和工况，开展结果计算与机理核查。')
s=s.replace('连接结构接近阶段性完成，不代表整板热流性能已验证；最小闭环实现也不等于多区域系统已经完成全部控制比较。','连接几何准备不代表连接性能或整板流热已验证；简化闭环仿真也不等于多区域系统已经完成控制比较。')
s=s.replace('连接结构接近阶段性完成，不等于整板与控制系统均已验证；最小闭环实现也不等于多输入耦合系统已经完成全面控制比较。','连接几何准备不等于连接性能及整板系统已验证；简化闭环也不等于多输入耦合系统已经完成控制比较。')
s=s.replace('局部连接改善也不会自动推广为整板优势。','局部单元的性能差异也不会自动推广为整板优势。')
s=s.replace('局部验证与平台基础在同一框架下区分证据层级。','局部单元计算与平台基础在同一框架下区分证据层级。')
# Float protection at logical transitions, not every section.
s=s.replace(r'\section{问题与对策}',r'\FloatBarrier'+'\n'+r'\section{问题与对策}')
s=re.sub(r'(?<=[0-9])%',r'\\%',s)
out=REPORT/'中期报告.tex';out.write_text(s,encoding='utf8')

images=json.loads((SRC/'integration_summary.json').read_text(encoding='utf8'))['referenced_images']
for ref in images:
    name=Path(ref).name
    if name.startswith('midterm_diagram_fig_'): new=name.replace('midterm_diagram_fig_','midterm_concept_fig_',1)
    elif name.startswith('midterm_'): new='midterm_asset_'+name[len('midterm_'):]
    elif re.match(r'^\d{2}_',name): new='midterm_monthly1_'+name
    elif name.startswith(('month2_','month3_')): new='midterm_'+name
    elif name=='udf_learning_interfaces.png': new='midterm_'+name
    else: raise ValueError(name)
    s=s.replace(name,new)
out.write_text(s,encoding='utf8')
labels=[x for x in re.findall(r'\\label\{([^}]+)\}',s) if '#' not in x]
labels+=re.findall(r'^\\reportfigure\{([^}]+)\}',s,re.M)
assert len(labels)==len(set(labels)), 'duplicate labels'
refs_used=re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',s)
missing=sorted(set(refs_used)-set(labels));assert not missing,missing
graphics=[x for x in re.findall(r'\\includegraphics\[[^]]*\]\{([^}]+)\}',s)+re.findall(r'^\\reportfigure\{[^}]*\}\{[^}]*\}\{([^}]+)\}',s,re.M) if '#' not in x]
assert all((REPORT/p).exists() for p in graphics)
(SRC/'integration_summary.json').write_text(json.dumps({'source_months':5,'top_level_figures':len(re.findall(r'\\begin\{figure\}',s))-3+len(re.findall(r'^\\reportfigure\{',s,re.M)),'top_level_tables':len(re.findall(r'\\begin\{table\}',s))+len(re.findall(r'\\begin\{longtable\}',s)),'referenced_images':sorted(set(graphics)),'missing_references':missing,'pid_source':'pid_sim.npz','new_cfd_runs':0},ensure_ascii=False,indent=2),encoding='utf8')
print(out)
