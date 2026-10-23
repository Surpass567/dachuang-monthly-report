"""2026-10-23 二次修订：统一五部分主线，月二合并全部小块资料。

基于上一轮本地稿执行一次；输入备份留在忽略的 structure_qa/outline_before/。
不运行仿真，不改写 CSV 原值。后续已带标记的稿件禁止重复迁移。
"""
from pathlib import Path
import csv
import re
import shutil

ROOT=Path(__file__).resolve().parents[3]
REPORTS=ROOT/'reports'
HERE=Path(__file__).resolve().parent
MARK='% unified-five-part-outline 2026-10-23'
paths=sorted(REPORTS.glob('*.tex'))
assert len(paths)==6
assert all(MARK not in p.read_text(encoding='utf-8') for p in paths), '已调整，勿重复执行。'
backup=HERE/'structure_qa/outline_before'
backup.mkdir(parents=True,exist_ok=True)
sources={p.stem:p.read_text(encoding='utf-8') for p in paths}
for p in paths: shutil.copyfile(p,backup/p.name)

def sec(title,body): return '\\section{'+title+'}\n\n'+body.strip()+'\n\n'
def sub(title,body): return '\\subsection{'+title+'}\n\n'+body.strip()+'\n\n'
def parts(s):
    ms=list(re.finditer(r'\\section\{([^}]+)\}',s))
    return s[:ms[0].start()],{m[1]:s[m.end():ms[i+1].start() if i+1<len(ms) else len(s)] for i,m in enumerate(ms)}
def demote(s):
    return re.sub(r'\\(subsubsection|subsection|section)\{',lambda m:'\\'+{'section':'subsection','subsection':'subsubsection','subsubsection':'paragraph'}[m[1]]+'{',s)
def split_status(s):
    a=s.index(r'\subsection{完成情况}')
    b=s.find(r'\subsection{',a+1)
    if b<0:b=len(s)
    return s[:a]+s[b:],s[a+len(r'\subsection{完成情况}'):b]
def cut_sub(s,title):
    pat=r'\subsection{'+title+'}'
    a=s.index(pat); b=s.find(r'\subsection{',a+len(pat))
    if b<0:b=len(s)
    return s[:a]+s[b:],s[a+len(pat):b]
def write(p,s): p.write_bytes(('\n'.join(v.rstrip() for v in s.splitlines())+'\n').encode('utf-8'))

m3=sources['逻辑月3_形态与物理']
airfoil=next(m[0] for m in re.finditer(r'\\begin\{table\}.*?\\end\{table\}',m3,re.S) if r'\label{tab:airfoil}' in m[0])
airfoil=airfoil.replace('tab:airfoil','tab:airfoil-overview')
csvrows=list(csv.DictReader((HERE/'small_model_results.csv').open(encoding='utf-8-sig')))
shortnames=['六边形 v4','六边形 v4.2','0016 A06 基础','2416 A00 core','2416 A00 BOI','0016 A06 拟合物性','0016 A06 REFPROP','2416 v3','gao2.1','2420 v4 原始','2420 回流 300 K','2420 IAPWS dt0.005','2420 IAPWS dt0.01','0016 v2','1416 v2','3416 v2',r'叶脉 A\_leaf']

for p in paths:
    name=p.stem
    pre,d=parts(sources[name])
    plan,status=split_status(d['本月研究任务'])
    # 文末参考文献独立保留，不参与章节迁移。
    tail=d['下月计划']; bibstart=tail.index(r'\begin{thebibliography}')
    nextplan=tail[:bibstart].replace(r'\clearpage','').strip()
    bibliography=tail[bibstart:]
    conclusion=d.get('阶段性结论','')
    issues=d.get('问题与对策','')
    if name.startswith('逻辑月1'):
        process=''
        for title in ['阶段一：通读与摘录','阶段二：导出与复现','基础物理与 UDF 初步学习','初步小块理论的形成','控制方向：自控基础学习']:
            body=d[title]
            if title=='阶段二：导出与复现':
                body,repro=cut_sub(body,'复现结果')
            process+=demote(sec({'阶段一：通读与摘录':'文献学习与研究启发','阶段二：导出与复现':'仿真软件学习与结构复现','控制方向：自控基础学习':'自动控制基础学习'}.get(title,title),body))
        process=process.replace(r'\textbf{环境}：',r'\paragraph{软件与计算环境}'+'\n')
        process=process.replace(r'\textbf{步骤}：',r'\paragraph{复现步骤}'+'\n')
        process=process.replace(r'\textbf{一阶系统}',r'\paragraph{一阶模型与时间常数}'+'\n'+r'\textbf{一阶系统}')
        process=process.replace(r'\textbf{二阶系统}',r'\paragraph{二阶模型与阻尼}'+'\n'+r'\textbf{二阶系统}')
        complete=sub('任务完成状态',status)+sub('三种流道的复现结果',repro)+d['阶段性收获']
        issues=sub('复现误差尚未量化','现有图像支持流程复现和趋势记录，但缺少逐项对应的文献数值与误差表。初步对策是固定几何、流量和热流密度，补齐原文值、复现值与偏差。')+sub('物性学习与代码版本尚需归档','初步 UDF 代码的具体版本及经验公式适用范围待补。先记录公式来源、温标和接口，正式排查与修改在逻辑月三展开。')+sub('小块设想与控制模型尚待验证','本月形成研究思路，未验证小块独立性或控制效果。下阶段先比较不同小块，再进行参数分组与数学控制验证。')
    elif name.startswith('逻辑月2'):
        research=d['研究进展']
        a=research.index(r'\subsubsection{代表性流道与仿生小块的探索}')
        b=research.index(r'\subsection{从多结构探索转向翼型专题}')
        structural=research[a:b]
        ctlstart=research.index(r'\subsubsection{PID 三个作用及其代价}')
        ctlend=research.index(r'\subsection{与预期的差异}')
        control=research[ctlstart:ctlend]
        control=control.replace('（2）'+r'\textbf{控制策略的物理起源：为什么必须控制，以及控制的物理基础。}','')
        # 明确控制知识与结构结果属于平行方向，消除其从属于翼型动机的错误层级。
        for old,new in [('一、缘由：静态结构回答不了「热源会移动」。','动态热源与控制需求'),('二、物理基础：三个可以被控制利用的对象性质。','可用于建模的对象性质'),('三、能量学基础：控制为什么能省功。','流量调节与水力代价'),('四、由上述物理性质确定的学习重点。','由对象性质确定控制学习重点')]:
            control=control.replace(r'\textbf{'+old+'}',r'\paragraph{'+new+'}')
        process=demote(sec('资料与评价指标的整理',d['进阶阅读与理论支撑']))+sub('小块数据整理方法','将常规流道、蜂窝、叶脉和翼型纳入同一候选集合。统一列出热负荷、温度、压差和水力功率；对保存时刻、流量及统计口径保留条件说明。同一几何的物性、网格与时间步分支单独标识，不重复计作新结构。')+sub('传统 PID 学习与控制流程设计',control)
        # 原表仅保留了非 NACA 四条，本次从原始 CSV 恢复全部十七条。
        start=structural.index(r'\multicolumn{6}{@{}l@{}}{\textbf{非 NACA')
        end=structural.index(r'\end{longtable}',start)
        rows=r'\multicolumn{6}{@{}l@{}}{\textbf{全部小模型保存分支（固体单元温度算术平均）}}\\'+'\n'
        for row,label in zip(csvrows,shortnames):
            nums=[float(row[k]) for k in ['热流密度 (W/cm²)','最高温度 (°C)','平均温度 (°C)','压差 (kPa)','水力功率 (W)']]
            rows+=' & '.join([f'{nums[0]:.2f}',label]+[format(v,fmt) for v,fmt in zip(nums[1:],['.2f','.2f','.3f','.5f'])])+r' \\'+'\n'
        structural=structural[:start]+rows+structural[end:]
        structural=structural.replace(r'\subsubsection{代表性流道与仿生小块的探索}',r'\subsection{全部小块的合并展示与分析}')
        structural=structural.replace('在 150 至 300 W/cm$^2$ 的共同工况下','在表列 300 W/cm$^2$ 的工况下')
        structural=structural.replace('非 NACA 小模型记录的平均温度','CSV 小模型记录的平均温度')
        structural=structural.replace(r'\caption{非 NACA 小模型的网格与计算条件}',r'\caption{全部小模型的流量与保存条件}')
        cstart=structural.index(r'\begin{table}[H]',structural.index(r'\label{tab:results}'))
        cend=structural.index(r'\end{table}',cstart)+len(r'\end{table}')
        condition=r'''\begin{table}[H]\centering\small
\caption{全部小模型的流量与保存条件}\label{tab:other-conditions}
\begin{tabularx}{\textwidth}{@{}Y r r r@{}}
\toprule\rowcolor{ydzjlight} 分支 & 流量 / (mL/s) & 保存时刻 / s & 时间步 / s \\
\midrule
'''
        for row,label in zip(csvrows,shortnames):
            condition+=' & '.join([label,f'{float(row["体积流量 (m³/s)"])*1e6:.3f}','稳态' if row['求解方式']=='稳态' else f'{float(row["保存时刻 (s)"]):g}','---' if row['求解方式']=='稳态' else f'{float(row["时间步 (s)"]):g}'])+r' \\'+'\n'
        condition+='\\bottomrule\n\\end{tabularx}\n\\end{table}'
        structural=structural[:cstart]+condition+structural[cend:]
        structural=structural.replace('列出网格与计算条件','列出全部小模型的流量与保存条件；各分支网格数保留在配套 CSV 中')
        structural=structural.replace('现有单元数可说明离散规模','配套 CSV 中的单元数可说明离散规模')
        analysis=r'''\subsubsection{各类小块的联合分析}
\paragraph{温度表现与水力代价共同决定候选方向}
表~\ref{tab:results}将五条既有流道记录和十七条小模型保存分支合并，覆盖直线、正弦、蜂窝、叶脉与翼型。300 W/cm$^2$ 的记录中，直线温度较低，NACA2416 的水力功率较低，说明温度收益与泵送代价需要同时权衡。原记录的流量并非完全相同，这一现象只用于发现候选方向。
\paragraph{仿生结构与翼型使用同一评价框架}
600 W/cm$^2$ 下，叶脉比 gao2.1 的最高温度低约 26.60 $^\circ$C，水力功率约为其 6.07 倍；同时两者流量为 16 与 9 mL/s，且分别为稳态和瞬态保存结果。这组记录展示了温度与水力代价的权衡，不能将全部差异归因于形状。六边形 v4 与 v4.2 也应连同各自流量和热负荷分析。
\paragraph{翼型内部差异为后续参数分组提供线索}
450 W/cm$^2$、约16 mL/s和0.10 s条件下，NACA3416 v2 比0016 v2的最高温度低约0.230 $^\circ$C，压差高约5.25\%。350 W/cm$^2$ 的基础、core、BOI和物性分支仍混有时刻与网格差异；NACA2420的四条记录属于同一几何的设置检查，126.82 W/cm$^2$是1 s瞬时热流。将这些记录纳入同一数据表，既可展示覆盖范围，也可区分结构探索和数值设置变化。
\subsubsection{六种翼型基准结果的统一补充展示}
表~\ref{tab:airfoil-overview}保留另一组已有基准结果。该组使用 K、底板平均温度、换热系数与 PEC，与前表的固体单元算术平均温度分别标注；不将两种平均方式混为同一指标。月二统一呈现候选结构，参数分组与机理细化在月三继续。
'''
        structural+=analysis+airfoil+'\n'+sub('结构探索形成的后续方向','在统一评价框架下保留各类小块，翼型的厚度、弯度和攻角可进一步参数化。下一阶段设计分组并检验数值条件；不同热流密度下的小块选择分界线仍归逻辑月四。')
        complete=sub('任务完成状态',status.replace('四种流道 39 个既有工况及非 NACA 小模型保存结果','五条流道代表记录、十七条小模型分支及六翼型基准结果').replace('本月只说明研究动机，详细结果在月三','本月合并展示已有结果，参数分组与机理研究在月三'))+structural+sub('阶段认识',demote(conclusion))
        issues=sub('探索结果与预期的差异',research[ctlend+len(r'\subsection{与预期的差异}'):])+issues
        issues=issues.replace('分别保留各组条件及结果，避免无条件合并排序','将所有小块纳入同一组表格和综合分析，保留各组条件，比较温度表现与水力代价')
    elif name.startswith('逻辑月5'):
        process=demote(sec('整板布局与连接尝试',d['整板布局与连接尝试']))+demote(sec('后续验证方案的设计',d['后续验证方案']))
        for old,new in [('一、单元性能不等于整板性能。','单元到整板的条件变化'),('二、连接段是新的阻力源。','连接段阻力与偏流')]:
            process=process.replace(r'\textbf{'+old+'}',r'\paragraph{'+new+'}')
        complete=sub('任务完成状态',status)+conclusion
    else:
        research=d['研究进展']
        if name.startswith('逻辑月3'):
            research,results=cut_sub(research,'关键结果')
            research,difference=cut_sub(research,'与预期的差异')
            research=research.replace(r'\subsection{翼型专题与数值验证}',r'\subsection{翼型参数与流热性能研究}')
            research=research.replace(r'\subsubsection{从初步编写到正式修正}',r'\subsection{UDF 正式修改与验证}'+'\n'+r'\subsubsection{从初步编写到正式修正}')
            research=research.replace(r'\subsubsection{七档网格分析与无关性检验}',r'\subsection{网格分析与无关性检验}'+'\n'+r'\subsubsection{七档网格分析与无关性检验}')
            research=research.replace(r'\subsubsection{初步数学模型与最小闭环验证}',r'\subsection{PID 纯数学模拟}'+'\n'+r'\subsubsection{初步数学模型与最小闭环验证}')
            research=re.sub(r'\\textbf\{\d+\. ([^}]+)\}',r'\\paragraph{\1}',research)
        else:
            research,results=cut_sub(research,'关键结果')
            research,difference=cut_sub(research,'与预期的差异')
        process=(demote(sec('文献与理论准备',d['进阶阅读与理论支撑'])) if '进阶阅读与理论支撑' in d else '')+research
        complete=sub('任务完成状态',status)+sub('关键结果与完成边界',results)+conclusion
        issues=sub('与预期的差异',difference)+issues
    # 月四的研究设计不可被“已完成的工作”误读为已取得计算结果。
    process=process.replace(r'\subsection{已完成的工作}',r'\subsection{研究步骤与分析框架}')
    s=pre+MARK+'\n'+sec('本月计划',plan)+sec('研究过程',process)+sec('完成情况',complete)+sec('问题与初步对策',issues)+sec('下个月计划',nextplan)+'\\clearpage\n'+bibliography
    s=s.replace(r'\titleformat{\paragraph}[runin]{\normalsize\heiti\color{ydzjblueiii}}{}{0pt}{}','').replace(r'\titlespacing{\paragraph}{0pt}{5pt}{1em}','').replace(r'\setcounter{secnumdepth}{3}',r'\setcounter{secnumdepth}{4}')
    write(p,s)
shutil.copyfile(REPORTS/'中期报告.tex',HERE/'midterm_expanded/final_report.tex')
print('六份正文已统一五部分；月二已合并22条记录和6种翼型基准。')
