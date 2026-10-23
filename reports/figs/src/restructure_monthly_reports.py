"""按 2026-10-23 确认的逻辑月重组既有素材；只改文稿，不运行数值仿真。

输入固定为 Git 基线，保留数据、图像和引用。重跑会覆盖目标文稿，
后续人工修订后请勿直接重跑。月报文件名变化见结构调整说明。
"""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
REPORTS = ROOT / 'reports'
if any('unified-five-part-outline' in p.read_text(encoding='utf-8') for p in REPORTS.glob('*.tex')):
    raise SystemExit('当前稿已按五部分再次修订，禁止用旧基线脚本覆盖。')
BASE = '0ad6126276f092d677e95bfb4f5fc1f8848df0f5'

def source(name):
    return subprocess.check_output(['git', 'show', f'{BASE}:reports/{name}.tex'], cwd=ROOT).decode('utf-8').replace('\r\n', '\n')

def between(s, start, end):
    return s[s.index(start):s.index(end, s.index(start))].strip() + '\n\n'

def table(s, label):
    return next(m[0] for m in re.finditer(r'\\begin\{table\}.*?\\end\{table\}', s, re.S) if '\\label{'+label+'}' in m[0]) + '\n\n'

def heading(title, body, sub=False):
    return ('\\subsection{' if sub else '\\section{') + title + '}\n\n' + body.strip() + '\n\n'

def tasks(rows, label='tab:tasks', caption='本月工作与材料状态'):
    return r'\begin{table}[H]\centering'+'\n'+f'\\caption{{{caption}}}\\label{{{label}}}\n'+r'''\begin{tabularx}{\textwidth}{@{}Y Y Y@{}}
\toprule\rowcolor{ydzjlight} 工作 & 状态 & 依据或缺口 \\
\midrule
'''+ '\n'.join(' & '.join(row)+r' \\' for row in rows)+r'''
\bottomrule\end{tabularx}\end{table}

'''

def plan(rows):
    return tasks(rows, 'tab:plan', '后续工作及所需产出')

def preamble(stage, n, title, keywords, summary, extra=''):
    setup = 'stageone' if stage == 1 else 'stagetwo'
    return f'''% 2026-10-23：按学习复现、探索尝试、优化验证、迭代调试、整板尝试重组。
\\documentclass[stage{stage},fontset=fandol]{{ydzjreport}}
\\usepackage{{subcaption,longtable}}
{extra}
\\{setup}setup
{{第 {n} 个逻辑月 · {title}}}
{{冯旭东、陈思文、张昊洋}}
{{复合微通道分区冷却}}
{{【待确认】逻辑月 {n} 对应的自然月}}
{{{keywords}}}
{{{summary}}}
\\begin{{document}}
\\make{setup}head

'''

def bibliography(s):
    return between(s, r'\begin{thebibliography}', r'\end{document}')

def save(name, text):
    (REPORTS / (name+'.tex')).write_text(text.rstrip()+'\n', encoding='utf-8')

m1=source('逻辑月1_基础建立')
m2=source('逻辑月2_指标与形态')
m3=source('逻辑月3_形态与物理')
m4=source('逻辑月4_连接成网络')
m5=source('逻辑月5_整板验证')
mid=source('中期报告')

# 月一：保留文献摘录与十二幅复现图；控制框架、具体 PID 和正式物性修正后移。
concept=between(m1, r'\subsection{概念一', r'\subsection{概念二')
concept=re.sub(r'\\subsection\{[^}]*\}', r'\\subsection{从非均匀热负荷提出小块思路}', concept, count=1)
literature=between(m1, r'\subsection{关键摘录}', r'\section{阶段二')
literature=literature.replace('本阶段的应用', '对小块思路及后续工作的启示').replace('文献要点与本阶段工作','文献要点与研究思路')
repro=between(m1, r'\subsection{复现环境与步骤}', r'\subsection{水物性 UDF')
repro=repro.replace('核查原水物性 UDF：在 298.15 K 校验点比对参考物性值；','学习已有物性函数的温度输入、量纲和参考数据来源；').replace('记录误差量级，判断是否需要重新拟合。','记录尚待核查的问题，为后续正式修改物性函数准备材料。')
repro=repro.replace('核查采用 Python 后处理','学习采用 Python 后处理')
repro_result=between(m1, r'\subsection{复现结果}', r'\textbf{物性核查}')
ctrl_basic=between(m1, r'\subsection{一阶与二阶', r'\subsection{PID 三个')
ctrl_basic=ctrl_basic.replace('减少超调的正确手段是提高阻尼（引入微分作用）或降低增益，\n\t\t而不是简单地把比例项调小——后者只会让响应变慢，超调未必改善。','具体控制器的作用和整定方法在下一逻辑月继续学习。')
# 原文换行与缩进不同，基础知识段落直接避免无条件整定判断。
ctrl_basic=re.sub('这条式子给出一个容易被忽略的结论：.*?超调未必改善。', '该式说明二阶标准模型中阻尼比与超调的关系；实际热控对象还需结合时延和闭环模型分析。', ctrl_basic, flags=re.S)
out=preamble(1,1,'学习与复现','软件学习；文献复现；初步小块理论；UDF 入门；自控基础','通过软件学习与文献复现建立研究基础，从非均匀热负荷提出初步小块思路；学习变物性和自控基础，开展 UDF 初步编写尝试。')
out+=heading('本月研究任务',heading('任务目标','本月以学习和复现为主。先学习几何建模、网格、边界设置与后处理，再结合文献和课题组经验理解流动传热及变物性条件。在此基础上提出初步小块理论，并学习自动控制的基本概念。正式 UDF 修改归入逻辑月三，具体 PID 学习和控制流程归入逻辑月二。',True)+heading('完成情况',tasks([
('仿真软件学习与复现','已有材料','方形、圆形、六边形结构及后处理图'),('初步小块理论','概念形成','来自文献与非均匀热负荷思考，适用分界线尚未建立'),('物理与 UDF 学习','初步尝试','理解变物性、经验公式及接口，正式修改后移至月三'),('自控基础学习','已有整理','一阶、二阶、惯性、滞后及反馈基础')]),True))
out+=heading('阶段一：通读与摘录',heading('学习路径','从结构类文献和学长资料学习流道组织，再理解水物性随温度变化的条件，同时补充自动控制基础。文献中的性能数值仅作为设计启发，不作为本项目已取得的结果。',True)+literature)
out+=heading('阶段二：导出与复现',heading('复现目标','通过方形、六边形和圆形微通道复现，学习流固域构建、边界条件设置、求解监测和后处理。现有材料支持流程与趋势记录，尚缺完整的文献数值误差对照。',True)+repro+repro_result)
out+=heading('基础物理与 UDF 初步学习',heading('从常物性假设到变物性条件',r'''水的密度、黏度、导热系数和比热随温度变化。学习文献与课题组学长经验公式时，需要同时记录公式来源、温度单位和适用范围，不能只因程序可编译就认为物性正确。本月主要识别这些条件并初步尝试编写 UDF；公式排查、正式修改及其数值验证统一在逻辑月三报告。''',True)+heading('接口与初步编写',r'''密度、黏度和导热系数可通过 \texttt{DEFINE\_PROPERTY} 返回，并用 \texttt{C\_T(c,t)} 读取温度；比热通过 \texttt{DEFINE\_SPECIFIC\_HEAT} 定义，还需设置与比热积分一致的显焓。本月记录学习方法和初步代码尝试，不把后续拟合、自检及共同时间段对照提前归入本月。

【待补：本月初步 UDF 代码及学习记录的具体版本。】''',True))
out+=heading('初步小块理论的形成',concept+heading('本阶段的提出范围','由文献复现与热负荷差异得到初步设想：将冷板划分为可分别研究的局部单元，为不同需求配置不同结构。此时只提出研究对象和思路，尚未确定不同热流密度下的小块选择分界线；该问题在逻辑月四继续探究。',True))
out+=heading('控制方向：自控基础学习',heading('反馈与热控对象','本月学习设定值、被控温度、控制输入、扰动与反馈的关系，并认识到热容导致惯性、流体输运导致时延。学习目标是理解对象与反馈为何有关；PID 具体知识及控制流程图在逻辑月二展开。',True)+ctrl_basic)
out+=heading('阶段性收获',heading('认知上的变化','本月由软件操作进入问题思考：能够复现代表结构并整理结果；认识到物性公式必须有适用条件；形成以非均匀热负荷为起点的初步小块理论；建立控制对象、惯性和滞后的基本认识。小块是否有效仍需后续结构探索与验证。',True))
out+=heading('下月计划',plan([('多种小块结构尝试','代表性温度与水力结果','逻辑月二'),('传统 PID 专题学习','作用、限幅与整定的学习整理','逻辑月二'),('控制流程设计','输入输出接口与流程图','逻辑月二')]))
out+=bibliography(m1)+r'\end{document}'
save('逻辑月1_基础建立',out)

# 月二：常规与仿生结构探索；只保留九条代表结构记录，十三条翼型分支移月三。
struct=between(m2,r'\textbf{（一）流道',r'\textbf{（二）六种翼型')
struct=struct.replace(r'\textbf{（一）流道与小模型性能汇总}',r'\subsubsection{代表性流道与仿生小块的探索}')
struct=struct.replace('四种流道在共同热流密度下的后处理云图','四种流道在各自保存热流密度下的后处理云图')
struct=struct.replace('表~\\ref{tab:results} 将既有的 5 条流道记录与新增的 17 条小模型记录合并列示。','表~\\ref{tab:results} 选取 5 条既有流道记录与 4 条非 NACA 小模型记录。翼型的详细参数与验证分支放在逻辑月三。')
longtable=between(m2,r'\begingroup',r'\endgroup')+r'\endgroup'+'\n\n'
start=struct.index(r'\multicolumn{6}{@{}l@{}}{\textbf{NACA 小模型')
stop=struct.index(r'\end{longtable}',start)
struct=struct[:start]+struct[stop:]
struct=struct.replace('表中新增小模型记录','表中非 NACA 小模型记录').replace('、后续翼型表中的底板平均温度分别保留','分别保留')
ctrl_physics=between(m1,r'\subsection{概念二',r'\section{控制方向')
ctrl_physics=re.sub(r'\\subsection\{概念二[^}]*\}', r'\\subsubsection{热控对象对控制设计的要求}', ctrl_physics, count=1)
ctrl_physics=ctrl_physics.replace(r'\subsection{初步控制框架}',r'\subsubsection{控制流程图与接口}')
ctrl_physics=ctrl_physics.replace('（1）冷却工质水的物性随温度变化。因此\\textbf{物性核查必须放在结构比较之前}。','结构探索和控制设计均需注明所用物性；物性正式修改与核查在逻辑月三进行。')
ctrl_physics=ctrl_physics.replace('这决定了「加流量有效，但边际收益递减」','该简化模型用于说明「加流量有效，但边际收益递减」')
ctrl_physics=ctrl_physics.replace('它不改变闭环的稳定性判据，只负责提供「提前量」。\n\t\t这样即使预测失效，闭环仍由 PID 兜底，不会因为预测出错而失稳。','预测用于提供提前量；其接入方式、误差和回退策略仍需单独验证，不能仅凭分层架构保证闭环稳定。')
ctrl_physics=ctrl_physics.replace('泵功近似与流量的三次方成正比','在阻力近似随流量平方变化的简化条件下，水力功近似与流量的三次方成正比')
pid_theory=between(m1,r'\subsection{PID 三个',r'\subsection{数据驱动')
pid_theory=pid_theory.replace(r'\subsection{',r'\subsubsection{')
out=preamble(2,2,'探索与尝试','多种小块；代表结构比较；传统 PID；控制流程','探索不同小块结构的温度与水力表现，形成翼型专题研究的动机；学习传统 PID 的具体知识并提出控制流程。')
out+=heading('本月研究任务',heading('任务目标','本月承接初步小块理论，尝试常规流道、仿生结构与翼型扰流小块，关注结构变化带来的温度收益和水力代价。控制方向从基础理论进入传统 PID 的作用、工程约束与流程设计，数学模拟留到逻辑月三。',True)+heading('完成情况',tasks([('多种结构探索','已有结果','四种流道 39 个既有工况及非 NACA 小模型保存结果'),('评价口径','部分统一','热负荷、流量、时刻及温度统计仍需分别标识'),('翼型专题方向','提出','本月只说明研究动机，详细结果在月三'),('传统 PID 与控制流程','已整理','具体知识、控制层次和接口；本月不报告闭环模拟结果')]),True))
lit=between(m2,r'\subsection{本阶段文献与资料}',r'\section{研究进展}')
lit=lit.replace('明确相对厚度、相对弯度、攻角对液冷性能的影响','识别可用于后续分组的厚度、弯度与攻角参数')
out+=heading('进阶阅读与理论支撑',lit)
out+=heading('研究进展',heading('已完成的工作','已汇总多种小块的保存结果，并整理控制流程。下面先说明结构探索，再说明传统 PID 学习和控制方案；各数据组保留各自条件，不以跨组温度差直接判定优劣。',True)+heading('关键结果',struct+heading('从多结构探索转向翼型专题','翼型扰流小块兼有可参数化的剖面和可调整的排列形式，为后续分析厚度、弯度、攻角等因素提供了研究对象。本月据此提出翼型专题方向；详细翼型表、参数分组和流场分析统一放在逻辑月三。不同热流密度下应选择哪类小块的分界线属于逻辑月四。',True)+pid_theory+ctrl_physics,True)+heading('与预期的差异','原先可能期待结构越复杂、散热越强，但已有结果提示温度改善和压降代价需要共同评价；不同组的流量和保存时刻也会改变比较结果。这是探索阶段发现的问题，尚不能据此给出小块适用分界线。控制方面，流程图目前是方案，不代表已经完成实物泵阀标定或闭环验证。',True))
out+=heading('问题与对策',heading('遇到的主要问题','各组物性、工况和温度统计口径未完全一致；翼型参数与多柱相互干扰尚未分离；控制对象的执行量和实际流量映射未知。',True)+heading('已尝试的方案','分别保留各组条件及结果，避免无条件合并排序；将翼型作为下一阶段专题；控制流程先定义输入、输出及安全约束。',True)+heading('下一步对策','逻辑月三设计翼型参数分组、修改 UDF 并检查网格，以纯数学对象开展 PID 模拟。参数组未取得结果前，保留研究方案和数据缺口。',True))
out+=heading('阶段性结论',heading('可以确定的','已有结构记录支持继续研究温度与水力代价之间的权衡；翼型可作为进一步参数化研究对象；传统 PID 学习已落实为控制流程和接口。',True)+heading('尚不能确定的','不同热流密度下的小块选择分界线、翼型参数的独立影响、实物控制性能及节能收益均未得到本月证据支持。',True))
out+=heading('下月计划',plan([('翼型参数分组研究','明确变量、固定条件与缺失数据','逻辑月三'),('正式修改 UDF 与网格检验','适用范围、校验和敏感性记录','逻辑月三'),('PID 纯数学模拟','保存时序、统计窗口及实现检查','逻辑月三')]))
out+=bibliography(m2)+r'\end{document}'
save('逻辑月2_指标与形态',out)

# 月三：专项翼型资料、参数分组方案、正式 UDF 修正、网格诊断、数学 PID。
airfoil=between(m2,r'\textbf{（二）六种翼型',r'\textbf{（三）控制回路')
airfoil=airfoil.replace(r'\textbf{（二）六种翼型在基准工况下的比较}',r'\subsubsection{既有六种翼型结果与专题研究动机}')
airfoil=airfoil.replace('本次新增的 17 条代表结果','包含月二结构探索和本月翼型资料的 17 条代表结果')
airfoil=airfoil.replace('努塞尔数提高约 5.7\\%','表列换热系数提高约 5.5\\%')
airfoil=airfoil.replace('已并入表~\\ref{tab:results}，沿用前述固体单元算术平均温度和水力功率口径','整理在表~\\ref{tab:results}，平均温度采用固体单元算术平均，水力功率为压差与体积流量之积')
# 长表只保留十三条翼型分支，所有原始数值不变。
lt_start=longtable.index(r'\multicolumn{6}{@{}l@{}}{\textbf{既有流道结果')
lt_end=longtable.index(r'\multicolumn{6}{@{}l@{}}{\textbf{NACA 小模型')
branch_table=longtable[:lt_start]+longtable[lt_end:]
branch_table=branch_table.replace('流道与小模型的温度及水力性能汇总','翼型小模型的温度及水力性能汇总')
airfoil=airfoil.replace(r'\textbf{350 W/cm$^2$ 下的几何、网格与物性分支。}',branch_table+r'\textbf{350 W/cm$^2$ 下的几何、网格与物性分支。}')
mesh=between(m3,r'\textbf{（二）网格',r'\textbf{（三）机理')
mesh=mesh.replace(r'\textbf{（二）网格无关性检验}',r'\subsubsection{七档网格分析与无关性检验}')
mesh=re.sub(r'\\textcolor\{red\}\{[^\n]*\}', '', mesh)
mechanism=between(m3,r'\textbf{（三）机理',r'\textbf{（四）参数')
mechanism=mechanism.replace(r'\textbf{（三）机理分析：高弯度翼型 PEC 回落的原因}',r'\subsubsection{翼型差异的定性机理解释}')
mechanism=mechanism.replace('这正是 NACA0024、NACA4424 的 PEC 高于基准、\n而 NACA6424、NACA6624 回落的原因。','这一解释与既有表中 PEC 的变化相容，但仍需分离点、回流区和局部换热数据验证，不能作为已完成的因果证明。')
udf=between(mid,r'\paragraph{已有拟合精度',r'\subsubsection{数值仿真自动化')
udf=udf.replace(r'\paragraph{已有拟合精度和同一时刻求解对照}',r'\subsubsection{拟合精度与代表算例对照}')
udf=udf.replace('月1、月3所述298.15 K密度偏低60.8\\%与现有逐点公式核查表不一致：','历史月报曾记载298.15 K密度偏低60.8\\%，但该说法与现有逐点公式核查表不一致：')
udf_intro=r'''\subsubsection{从初步编写到正式修正}
月一学习接口和经验公式后，本月正式核对温度相关水物性并修改 UDF。现有拟合版采用101325 Pa下 REFPROP WATER.FLD v9.1 液态水数据，适用材料温度为280--360 K；密度、黏度、导热系数和比热随温度返回。该压力是拟合条件，不表示流动压力场处处固定。

比热与显焓须采用同一多项式及其积分：
\begin{equation}
h(T)-h(T_{\mathrm{ref}})=\int_{T_{\mathrm{ref}}}^{T}c_p(\theta)\,\mathrm d\theta,
\qquad \frac{\mathrm dh}{\mathrm dT}=c_p(T).
\end{equation}
编译通过只说明接口可用；校验还需覆盖适用范围、数值趋势和实际调用。以下采用仓库已有拟合与共同时间段对照记录，不重新运行 Fluent 求解，也不把代表算例推广到全部结构。
'''
pid=between(mid,r'\subsubsection{初步数学模型与最小闭环验证}',r'\subsubsection{向物理机理融合')
pid=pid.replace('月2采用','本月采用').replace(r'\cite{monthly2}',r'\cite{control}')
out=preamble(2,3,'优化与验证','翼型专题；参数分组；UDF 修改；网格检验；PID 数学模拟','细化翼型参数研究，整理既有翼型结果与待补分组方案；修改并核验 UDF，分析网格敏感性，并开展纯数学温控模拟。',r'\usepackage{bm}')
out+=heading('本月研究任务',heading('任务目标','翼型研究从代表结构比较推进到参数分组。这里的分组指厚度、弯度、攻角等翼型参数的分组，不是不同热流密度下的小块选择分界线。与此同时，正式修改 UDF、复核已有网格结果，并在纯数学对象上初试 PID。',True)+heading('完成情况',tasks([('翼型专题研究','已有历史结果','六种翼型基准及13条小模型分支，不等于完整参数矩阵'),('翼型参数分组','方案待落实','本稿列出建议设计；完整数据尚未提供'),('UDF 修改及对照','已有代表记录','1601点拟合与共同0.137 s实现对照'),('网格检验','阶段分析','323万档作参考，联合收敛仍待复核'),('PID 数学模拟','已有时序','1800点保存数据；抗饱和实现存在待修问题')]),True))
out+=heading('研究进展',heading('已完成的工作',heading('翼型参数分组设计与数据缺口',tasks([('相对厚度组','拟固定弯度、攻角与排列','改变厚度；范围和组内数据待补'),('相对弯度组','拟固定厚度、攻角及其余几何','改变弯度；弯度位置需单独记录'),('攻角组','拟固定剖面和排列','改变攻角；角度范围及结果待补'),('单柱与阵列','需分别声明','不能把阵列差异直接当作单参数效应')],'tab:groups','翼型参数分组方案（建议设计，完整结果待补）')+'分组目标是分离变量影响。各组需固定热流密度、入口条件、物性版本、网格策略及结果时刻；若无法固定，应记录混杂因素。已有六翼型和保存分支可用于提出问题，不能据其数量宣布完成单因素扫描。\n\n【待补：实际分组表、参数上下界、各组统一工况结果和独立变量影响曲线。】',True)+airfoil+mechanism+udf_intro+udf+mesh+pid,True)+heading('关键结果','现有证据包括翼型历史对照、UDF 拟合及实现对照、七档网格和纯数学 PID 时序。参数分组研究尚无完整结果，不能宣布最优参数或影响权重；具体量化值及适用边界分别见上文。',True)+heading('与预期的差异','翼型弯度增大并未在已有记录中始终提高综合性能，定性解释仍需局部场验证；网格加密未使所有指标共同单调收敛；PID 程序中的累计误差限幅未实际进入增量更新，不能把两组相同输出解释为抗饱和有效。',True))
out+=heading('问题与对策',heading('遇到的主要问题','翼型分组的完整数据未提供；历史分支存在物性、网格及保存时刻差异；网格检验尚未充分统一推进历史；纯数学控制对象尚未与真实泵阀标定。',True)+heading('已尝试的方案','保留原始分支条件，采用共同时间段核对两种物性实现，统一以323万档比较网格，并按保存数组复核 PID 实现。',True)+heading('下一步对策','补充翼型分组数据；统一数值条件后复核网格；修正并独立检验抗饱和更新。随后在逻辑月四研究小块选择分界线、Bi 与扰流柱数量影响，准备翼型代理模型的数据。',True))
out+=heading('阶段性结论',heading('可以确定的','已有资料支持翼型专题研究；UDF 修改已有拟合与代表算例一致性证据；网格结论具有条件限制；PID 目前只验证数学对象下的反馈逻辑。',True)+heading('尚不能确定的','各参数的独立影响、最优翼型及泛化范围尚不能确定。局部物性实现一致性不等于实验精度；数学闭环不代表整板控制性能。',True))
out+=heading('下月计划',plan([('小块适用分界线','热流密度与小块选择的条件化关系','逻辑月四'),('Bi 与扰流柱数量','统一定义和对照数据','逻辑月四'),('翼型 XGBoost 尝试','先补分组数据再训练和独立测试','逻辑月四')]))
out+=bibliography(m2)+r'\end{document}'
save('逻辑月3_形态与物理',out)

# 月四整体改为理论迭代；不把研究问题写成已得到量化结果。
out=preamble(2,4,'迭代与调试','小块分界线；结构复杂性；Bi；扰流柱数量；XGBoost 待开展','探究不同热流密度下小块选择的适用边界，围绕 Bi 与扰流柱数量迭代理论，并准备基于翼型参数分组的 XGBoost 尝试。')
out+=heading('本月研究任务',heading('任务目标','本月从多种结构的探索结果回到小块理论，研究不同热流密度下应该选哪一种小块，以及选择何时发生变化。此处的分界线是小块适用范围，不是逻辑月三的翼型参数分组。代理模型拟承接月三分组，但 XGBoost 尚未开展。',True)+heading('完成情况',tasks([('小块适用分界线','研究问题已明确','尚缺统一约束下的扫描数据和交界热流密度'),('复杂性与性能关系','已有探索依据','现有记录可提示问题，尚不能给出通用排序'),('Bi 验证','待补依据','需给出特征尺度、物性、换热系数及计算结果'),('扰流柱数量影响','研究重点已明确','需数量对照和换热、水力指标支持定量判断'),('翼型 XGBoost','尚未开展','待月三分组数据补齐后训练和测试')]),True))
out+=heading('进阶阅读与理论支撑',heading('本阶段文献与资料','本月承接月二的结构探索、月三的翼型参数方案和数值核验，以及已有代理模型方法资料。Bi 与扰流柱数量部分目前缺少归档的专门计算记录，以下仅给出分析框架和需补证据。',True)+heading('对本方向的启示','结构形状、换热面积、扰流柱数量和水力阻力会共同改变温度表现。因此不能把“结构复杂”直接当作性能优势，也不能只按热流密度给出脱离流量、温度上限及泵功约束的固定选择。',True))
out+=heading('研究进展',heading('已完成的工作',r'''\subsubsection{由探索结果提出小块选择分界线问题}
已有常规、仿生和翼型结构结果显示温度收益与水力代价需要联合评价。例如月二保存记录中，300 W/cm$^2$下直线、正弦和 NACA2416 的最高温度分别为52.50、62.27和72.48 $^\circ$C，水力功率分别为0.04919、0.05897和0.01566 W。三者运行条件并非等泵功对照，不能据这些值直接确定适用分界线；这些记录的作用是提出“在什么约束下选哪一种小块”的问题。

\subsubsection{分界线的研究设计}
拟在统一几何尺度、入口条件和物性下扫描热流密度，先排除超出温度或压降限制的结构，再在满足限制的候选中比较泵送代价或统一综合指标。相同流量与相同泵功属于不同的比较方式，应分别报告。分界线可能随约束改变，也可能出现重叠可选区或没有可行结构的区间，不预先假设唯一阈值。

【待补：候选小块清单、扫描范围、约束值、性能曲线及分界线不确定性。】

\subsubsection{Bi 验证思路与小块理论边界}
本稿将 Bi 作为待验证的尺度分析工具。若采用常见固体导热与对流比较形式，需明确
\begin{equation}
Bi=\frac{hL_c}{k_s},\qquad L_c=\frac{V_s}{A_{\mathrm{conv}}}.
\label{eq:bi}
\end{equation}
式~\eqref{eq:bi} 中 $k_s$ 为固体导热系数，$V_s$ 为声明的固体体积，$A_{\mathrm{conv}}$ 为相应对流面积，$h$ 应注明提取位置与平均方式。这是建议采用的定义，实际尺度与统计区域仍需结合小块模型确认。Bi 可辅助讨论内部导热与表面对流的相对影响；相邻小块的横向导热耦合还需温度场或热量分配对照，不能由一个 Bi 值直接证明独立小块假设成立。

【待补：实际 Bi 定义、各结构计算表、与温度场的一致性验证。】

\subsubsection{扰流柱数量影响的迭代分析}
用户确定的研究重点是扰流柱数量在换热中的作用。数量改变会同时影响固液面积、流通截面、阻塞及柱间干扰，因此需要与翼型形状效应区分。拟固定外形尺寸、单柱几何和边界条件，改变柱数并记录排列、间距和总面积，联合比较最高温度、换热量、压降与水力功率；必要时再用等面积对照辨识数量与面积的影响。

目前尚未归档支持数量效应大小的完整对照数据，不给出“增加多少柱即提高多少换热”的结论。
【待补：柱数、排列、换热面积和对应性能数据。】

\subsubsection{基于翼型参数分组的 XGBoost 准备}
XGBoost 尚未开展。拟先核对月三参数组，将厚度、弯度、攻角及可用工况作为候选输入，选择定义统一的温度或压降指标作为输出，再建立基础回归和 XGBoost 对照。参数组没有数据时不能直接开始训练；已有13条分支混含物性、网格和时刻变化，也不能未经筛选当作13个独立合格训练样本。

后续需按几何或工况组合划分训练与测试，避免同一算例的近邻或重复记录跨集合，并报告误差、范围和训练成本。当前不填模型精度、泛化或加速收益。
''',True)+heading('关键结果','本月已明确小块适用分界线、Bi 验证、数量效应和代理模型四项研究任务。当前材料不足以给出量化分界线、Bi 验证结论或 XGBoost 预测结果，保留为待补项。',True)+heading('与预期的差异','由结构探索转向适用边界研究后，不能再沿用“更复杂即更优”的直观判断。实际需要同时检查导热、对流、水力代价和数量变化。现有非统一工况结果不足以把上述因素分离，理论解释需与后续数据共同修正。',True))
out+=heading('问题与对策',heading('遇到的主要问题','热流密度分界数据、Bi 定义及数量对照尚未齐备；翼型参数组数据不足，XGBoost 暂不具备训练依据。',True)+heading('已尝试的方案','从已有温度与水力记录中提出复杂性问题，并将形状、数量、面积及工况分别记录，形成后续对照要求。',True)+heading('下一步对策','补齐统一工况扫描，验证 Bi 与数量效应；按分组整理数据后开展基础回归与 XGBoost。将得到的小块候选及其条件限制交给逻辑月五整板尝试。',True))
out+=heading('阶段性结论',heading('可以确定的','小块分界线研究应由约束条件和性能对照支撑；复杂结构不能凭形态获得优先级；数量与面积需与翼型形状效应区分。',True)+heading('尚不能确定的','各小块交界热流密度、Bi 适用性、扰流柱数量的定量贡献及 XGBoost 性能均待补证据。',True))
out+=heading('下月计划',plan([('补充理论迭代证据','分界线、Bi 与数量对照','持续补充'),('补齐分组并尝试代理模型','训练记录及独立测试','具备数据后'),('将局部研究接入整板','候选布局、连接和供液条件','逻辑月五')]))
out+=bibliography(m4)+r'\end{document}'
save('逻辑月4_迭代与调试',out)

# 月五吸收旧月四的网络、连接与分流准备，保留原整板验证指标。
out=preamble(2,5,'整板尝试','整板布局；网络连接；供液；集成尝试；验证准备','承接小块探索与适用边界研究，尝试整板布局、单元连接及供液组织，区分已有几何准备与尚待求解的整板性能。')
out+=heading('本月研究任务',heading('任务目标','本月将局部小块研究推进到整板尝试，先组织布局、连接与供液，再检查是否具备流热计算和控制验证条件。整板几何准备不等于整板性能已验证；月四分界线未补齐时，已有布局只作为候选方案。',True)+heading('完成情况',tasks([('整板几何与热源布局','已有记录','中期资料保存40 mm整板及热源映射，不代表流热求解完成'),('网络与连接设计','有方向及候选','沿用已有连接、条带装配和供液方案'),('整板流体域与网格','待完成','需按整体几何独立检查'),('整板性能对照','尚缺结果','需支路流量、温度场和压差'),('系统控制验证','尚缺结果','月三数学 PID 不替代泵阀与多行验证')]),True)+heading('前置条件',tasks([('小块选择依据','月四研究内容','候选可先试装，分界线尚待数据支持'),('数值条件','月三核验','323万档仅局部参考，整板需独立网格检查'),('物性实现','已有代表对照','280--360 K拟合，整板实际温区与挂接仍需确认'),('执行器特性','缺数据','供液方式、泵阀曲线、流量计和采样条件')],'tab:pre','整板尝试的输入条件'),True))
network=between(m4,r'\subsection{对本方向的启示}',r'\section{研究进展}')
network=network.replace(r'\subsection{对本方向的启示}',r'\subsection{连接与供液的基本约束}').replace('这是本月最重要的认识。','').replace('上逻辑月得到的单元排序','已有单元级结果')
connection=between(m4,r'\textbf{（一）明确了连接段',r'\textbf{（二）UDF')
connection=connection.replace(r'\textbf{（一）明确了连接段的设计方向与评价方法}',r'\subsection{连接段设计目标与评价方法}')
out+=heading('整板布局与连接尝试',r'''\subsection{已有几何准备及其边界}
中期资料记录了 $40\,\mathrm{mm}\times40\,\mathrm{mm}$ 整板、$10\times10$ 单元及40 mm条带装配；其中低、中、高负荷分别为70、27、3格。此处沿用已有几何与热源映射，不把候选配置写成小块分界线已经验证的产物。各版本的主体、节距和连接尺寸需对应实际文件核查。

当前整板尚缺完整的流体域提取、共享拓扑、网格及求解证据。尝试顺序是核对几何和热源，再明确拓扑与供回液边界，随后建立流体域与网格，检查守恒与收敛，最后进行性能对照。

'''+network+connection)
verification=between(m5,r'\subsection{验证一',r'\section{问题与对策}')
verification=verification.replace('上逻辑月已确认','前述分析说明').replace('→',r'$\rightarrow$')
verification=verification.replace('在相同泵功下温度均匀性应明显改善','在相同泵功下比较温度均匀性，改善幅度及合格阈值待明确')
out+=heading('后续验证方案',verification)
out+=heading('问题与对策',heading('遇到的主要问题','局部排序无法直接用于整板；热源覆盖面积与总功率需要一致；连接阻力、支路分流和下游入口升温需要整板或条带计算；控制执行器尚缺实测辨识。',True)+heading('下一步对策','先以候选几何跑通整体流程；记录连接压降与支路流量，作为结构和控制共用输入；整板采用独立网格检验，并对物性适用温区、质量和能量平衡进行核查。',True))
out+=heading('阶段性结论',heading('可以确定的','已具备开展整板尝试的局部资料、部分几何与连接方向；整板性能应以独立求解和同条件对照判断。',True)+heading('尚不能确定的','现有布局是否最优、整板温度均匀性、实际泵送代价和多行协同控制收益均尚缺系统级数据。',True))
out+=heading('下月计划',plan([('整板模型准备','流体域、连接与边界核对','下一阶段'),('整板试算与独立检验','守恒、网格和求解记录','具备模型后'),('统一基准性能对照','温度、流量与泵功比较','试算可靠后'),('控制接口辨识','泵阀特性及动态响应','具备条件后')]))
out+=bibliography(m5)+r'\end{document}'
save('逻辑月5_整板尝试',out)

# 中期只同步月份归属和状态，不重建全部数值材料。
s=mid
mapping_start=s.index(r'\subsubsection{五个逻辑月的成果承接}')
mapping_end=s.index(r'\subsection{关键结果}',mapping_start)
mapping=r'''\subsubsection{五个逻辑月的成果承接}
五个逻辑月按研究推进组织，不等同已确认的自然月。月一学习与复现，月二探索小块并学习传统 PID、提出控制流程，月三专题研究翼型参数并修改 UDF、检查网格和开展数学 PID，月四迭代小块适用边界并准备代理模型，月五尝试整板。表~\ref{tab:mid_month_map}给出本文材料的归属。
\begin{table}[htbp]\centering\small
\caption{逻辑月主线、材料及证据状态}\label{tab:mid_month_map}
\begin{tabularx}{\linewidth}{@{}c Y Y@{}}\toprule
\rowcolor{ydzjlight} 月份 & 研究内容 & 证据状态 \\
\midrule
1 & 软件与文献复现、变物性及 UDF 入门、自控基础、初步小块理论 & 已有复现与学习材料；正式 UDF 修改后移至月三。\\
2 & 多种小块探索、代表结果比较、传统 PID 与控制流程 & 保留结构探索；不集中展开翼型数据，不放数学闭环结果。\\
3 & 翼型参数分组、UDF 修改、网格检验、PID 数学模拟 & 历史翼型和数值记录已有；完整参数分组数据待补。\\
4 & 不同热流密度下的小块分界线、Bi、扰流柱数量及 XGBoost & 分界线与 Bi、数量对照需补证据；XGBoost 尚未开展。\\
5 & 整板布局、连接供液和整体计算尝试 & 有几何准备；整板性能与控制收益待验证。\\
\bottomrule\end{tabularx}\end{table}
已有保存分支不自动等同于参数分组已完成；小块适用分界线与翼型参数分组属于不同研究问题。月四待开展的代理模型和月五待验证的整板不能转写成已有量化成果\cite{monthly1,monthly2,monthly3,monthly4,monthly5}。

'''
s=s[:mapping_start]+mapping+s[mapping_end:]
s=s.replace('月2采用一阶集总温控对象','月3采用一阶集总温控对象').replace('月报3.9 K对应','原月报3.9 K对应')
s=s.replace('月1由热容惯性','月2由热容惯性').replace('月1提出的感知','月2提出的感知')
s=s.replace('月1、月3所述298.15 K密度偏低60.8\\%与现有逐点公式核查表不一致：','历史稿所述298.15 K密度偏低60.8\\%与现有逐点公式核查表不一致：')
s=s.replace('月4尚无连接段成对性能结果','月5尚无连接段成对性能结果').replace('月4尚无连接段成对流热结果','月5尚无连接段成对流热结果').replace('月4尚未形成连接段仿真结果','月5尚未形成连接段仿真结果').replace('月4记录连接方向','月5记录连接方向')
s=s.replace('月2的39个既有工况、六翼型基准与17条代表分支','月2的结构探索、月3的六翼型基准与13条翼型分支')
s=s.replace('月1的12幅历史云图说明已具备三类结构复现和后处理基础；月2的39个既有工况、六翼型基准与17条代表分支','月1的12幅历史云图说明已具备三类结构复现和后处理基础；月2结构探索及月3翼型专题资料')
s=s.replace('月2首先建立温度和水力代价的比较口径，再从常规流道推进到翼型与仿生结构。','月2探索常规、仿生及翼型小块；月3集中整理翼型专题与参数分组方案。完整分组数据尚未提供，以下历史分支只按实际保存条件使用。')
s=s.replace(r'\subsection{承接月4和月5的连接与整板验证要求}',r'\subsection{承接月4理论迭代与月5整板尝试}')
s=s.replace('月4强调连接段引入的新阻力、并联供液不足与串联入口升温；月5把整板验证分解为五项内容。','月4研究不同热流密度下的小块选择分界线，并拟通过 Bi 与扰流柱数量分析迭代小块理论；XGBoost 尚未开展。分界线、Bi 及数量效应仍需数据支持，不能将候选布局解释为已经验证的最优配置。月5承接连接、供液及整板尝试，后续验证分解为五项内容。')
s=s.replace('网格前置条件采用本报告323万参考档的有限适用结论；月4、月5的“约150万网格”不作为新工况验收依据。','局部网格前置条件采用323万参考档的有限适用结论；整板仍需独立检验，不存在可直接迁移的统一单元数门槛。')
s=s.replace('逻辑月4 连接成网络','逻辑月4 迭代与调试').replace('逻辑月5 整板验证','逻辑月5 整板尝试')
s=s.replace('月1整理了温度读取、物性返回、编译加载、材料挂接与按需自检的流程。','月1学习温度读取与物性接口并初步编写；正式 UDF 修改、编译及代表算例验证归入月3。以下流程图用于说明实现方法，不代表月1已经完成全部校验。')
# 增补新主线中的任务缺口，避免中期继续宣称已完成代理模型。
needle=r'\subsubsection{当前研究进展与后续计划}'
s=s.replace(needle,needle+'\n逻辑月四拟承接月三翼型参数分组尝试 XGBoost，目前尚未开展。参数分组完整数据、训练测试划分及独立结果均待补；以下为方法准备。\n',1)
save('中期报告',s)

# 最终层级与证据措辞校正。
p=REPORTS/'逻辑月1_基础建立.tex'
s=p.read_text(encoding='utf-8').replace('由此得到一条判据：\\textbf{若被控对象近似一阶，那么出现超调就说明还存在二阶环节或纯滞后}。','该单调性针对正增益标准一阶模型；实际闭环超调需结合控制器、时延及其他动态分析。')
s=s.replace('本月通过文献和复现形成初步小块思路。','本月通过文献和复现形成初步小块思路。')
s=s.replace(r'\subsection{关键摘录}',r'\subsection{关键摘录}'+'\n文献要点见表~\\ref{tab:notes}及续表~\\ref{tab:notes-cont-2}、\\ref{tab:notes-cont-5}。')
s=s.replace(r'\subsection{复现结果}',r'\subsection{复现结果}'+'\n图~\\ref{fig:repro}保存复现后处理图，表~\\ref{tab:repro}汇总关注内容。')
p.write_text(s,encoding='utf-8')

# 数学控制图表采用就地排版，避免 FloatBarrier 产生居中的孤立浮动页。
p=REPORTS/'逻辑月3_形态与物理.tex'
s=p.read_text(encoding='utf-8')
for kind,label in [('figure','fig:20'),('table','tab:11')]:
    pattern=r'\\begin\{'+kind+r'\}.*?\\end\{'+kind+r'\}'
    for block in re.findall(pattern,s,re.S):
        if r'\label{'+label+'}' in block:
            revised=re.sub(r'\\begin\{'+kind+r'\}\[[^]]*\]',lambda _:r'\begin{'+kind+'}[H]',block,count=1)
            s=s.replace(block,revised)
p.write_text(s,encoding='utf-8')
p=REPORTS/'逻辑月2_指标与形态.tex'
s=p.read_text(encoding='utf-8').replace('照搬「快响应」的整定必然振荡','忽略时延而直接提高带宽可能引起振荡').replace('需要微分作用或预测补偿','可考虑超前或预测方法，需检验时延影响').replace('判据已定','约束原则已提出，阈值待定')
s=s.replace('由上一节的三条物理性质出发','由上述对象性质出发')
s=s.replace(r'\subsection{本阶段文献与资料}',r'\subsection{本阶段文献与资料}'+'\n表~\\ref{tab:lit}说明探索与控制学习所用资料。')
s=s.replace(r'\subsubsection{PID 三个作用及其代价}',r'\subsubsection{PID 三个作用及其代价}'+'\n表~\\ref{tab:pid}整理三个作用与工程代价。')
s=s.replace(r'\textbf{各层职责与接口。}',r'\textbf{各层职责与接口。}'+'\n各层方案与待补接口见表~\\ref{tab:layers}。')
extra_bibs='\n'.join(re.search(r'\\bibitem\{'+key+r'\}[^\n]*',m1)[0] for key in ['wu','ji','laguna'])
s=s.replace(r'\end{thebibliography}',extra_bibs+'\n'+r'\end{thebibliography}')
p.write_text(s,encoding='utf-8')
p=REPORTS/'逻辑月3_形态与物理.tex'
s=p.read_text(encoding='utf-8').replace(r'\subsection{已完成的工作}',r'\subsection{翼型专题与数值验证}').replace(r'\subsection{翼型参数分组设计与数据缺口}',r'\subsubsection{翼型参数分组设计与数据缺口}')
s=s.replace('分组目标是分离变量影响。','表~\\ref{tab:groups}列出分组设计。分组目标是分离变量影响。')
s=s.replace(r'\subsubsection{从初步编写到正式修正}',r'''\subsubsection{从初步编写到正式修正}
接口实现流程如图~\ref{fig:udf-interfaces}所示，正式修改在本月集中核查。
\begin{figure}[H]\centering
\includegraphics[width=\linewidth]{figs/udf_learning_interfaces.png}
\caption{水物性 UDF 的接口与实现流程；作为本月修改和核验的方法说明。}\label{fig:udf-interfaces}
\end{figure}
''')
p.write_text(s,encoding='utf-8')
p=REPORTS/'逻辑月4_迭代与调试.tex'
s=p.read_text(encoding='utf-8').replace('用户确定的研究重点是','本月研究重点是')
p.write_text(s,encoding='utf-8')
p=REPORTS/'中期报告.tex'
s=p.read_text(encoding='utf-8').replace('152万档压降差异仍为1.7722\\%，461万档为4.2751\\%，所以不沿用月4、月5前置条件中\n“约150万网格已验证”的旧表述。','152万档压降差异仍为1.7722\\%，461万档为4.2751\\%，现有记录不支持“约150万网格已验证”的判断。')
s=s.replace(r'\cite{monthly2}。'+'\n\n基础 PID',r'\cite{monthly3}。'+'\n\n基础 PID')
# PID小节的引文随材料归属同步。
pa=s.index(r'\subsubsection{初步数学模型与最小闭环验证}')
pb=s.index(r'\subsubsection{向物理机理融合',pa)
s=s[:pa]+s[pa:pb].replace(r'\cite{monthly2}',r'\cite{monthly3}')+s[pb:]
p.write_text(s,encoding='utf-8')
# 新模板不输出开篇框；中期原有概述归入第一节，保留内容。
s=(REPORTS/'中期报告.tex').read_text(encoding='utf-8')
start=s.index(r'\begin{keybox}',s.index(r'\begin{document}'))
end=s.index(r'\section{本月研究任务}',start)
front=s[start:end]
front=re.sub(r'\\begin\{keybox\}\s*(.*?)\\end\{keybox\}',r'\1',front,flags=re.S)
front=front.replace(r'\par\medskip','').replace(r'\noindent\textbf{项目概述}\par','')
s=s[:start]+s[end:]
s=s.replace(r'\section{本月研究任务}',r'\section{本月研究任务}'+'\n'+heading('项目概述',front,True),1)
(REPORTS/'中期报告.tex').write_text(s,encoding='utf-8')
p=REPORTS/'逻辑月1_基础建立.tex'
s=p.read_text(encoding='utf-8').replace('{冯旭东、陈思文、张昊洋}','{冯旭东、陈思文}')
p.write_text(s,encoding='utf-8')
print('已重组五份月报并同步中期月份映射；未运行仿真，未提交或上传。')

# 迁移后的版面收尾，避免表头独占页尾、遗留个人批注和图表跨越结论。
p=REPORTS/'逻辑月2_指标与形态.tex'
s=p.read_text(encoding='utf-8').replace(r'\begingroup',r'\needspace{14\baselineskip}'+'\n'+r'\begingroup',1)
s=s.replace(r'\textcolor{red}{陈思文插入数据来源网址}','')
s=s.replace(r'\begin{thebibliography}',r'\clearpage'+'\n'+r'\begin{thebibliography}',1)
p.write_text(s,encoding='utf-8')
p=REPORTS/'逻辑月3_形态与物理.tex'
s=p.read_text(encoding='utf-8').replace(r'\textcolor{red}{陈思文插入数据来源网址}','')
s=s.replace(r'\subsection{关键结果}',r'\FloatBarrier'+'\n'+r'\subsection{关键结果}',1)
p.write_text(s,encoding='utf-8')
p=REPORTS/'逻辑月5_整板尝试.tex'
s=p.read_text(encoding='utf-8').replace(r'\section{整板布局与连接尝试}',r'\needspace{8\baselineskip}'+'\n'+r'\section{整板布局与连接尝试}')
p.write_text(s,encoding='utf-8')
p=REPORTS/'中期报告.tex'
s=p.read_text(encoding='utf-8').replace('水物性 UDF 的温度输入、函数接口、材料挂接与自检流程，采用月1已有图。','水物性 UDF 的温度输入、函数接口、材料挂接与自检流程；正式修改和核验归入月三。')
s=s.replace('这些结果用于筛选后续同工况对照对象\\cite{monthly2}','这些结果用于筛选后续同工况对照对象\\cite{monthly2,monthly3}')
s=s.replace('17条代表结果与源文件对应关系已保留在配套数据中\\cite{monthly2}','17条代表结果与源文件对应关系已保留在配套数据中\\cite{monthly2,monthly3}')
s=s.replace('仍需流体域、共享拓扑、网格和守恒检查\\cite{monthly4}','仍需流体域、共享拓扑、网格和守恒检查\\cite{monthly5}')
s=s.replace(r'\begin{thebibliography}',r'\clearpage'+'\n'+r'\begin{thebibliography}',1)
p.write_text(s,encoding='utf-8')

# Keep generated sources free of trailing spaces and platform-dependent CRLF.
for p in REPORTS.glob('*.tex'):
    p.write_bytes(('\n'.join(line.rstrip() for line in p.read_text(encoding='utf-8').splitlines())+'\n').encode('utf-8'))
