"""Use N=3235081 as the sole comparison reference and add existing flow fields."""
from pathlib import Path
import csv, hashlib, json, re, shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DATA=HERE/'month3_mesh_data'
SOURCE=ROOT.parent/'no/NACA2416_v3/outlet_audit_20261009'
REF=3235081
def read(name):
    with (DATA/name).open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))
rows=read('raw_02s.csv'); dims=read('dimensionless_02s.csv')
reference=next(x for x in rows if int(x['grid'])==REF)
dimref=next(x for x in dims if int(x['grid'])==REF)
error=lambda value,base:abs(float(value)-float(base))/abs(float(base))*100
metrics=['t_avg','t_max','dp','Nu','h','f_D']
results=[]
for row,dim in zip(rows,dims):
    assert row['grid']==dim['grid']
    out={'grid':row['grid'],'reference_grid':REF}
    out.update({key+'_error_pct':error((row if key in row else dim)[key],(reference if key in reference else dimref)[key]) for key in metrics})
    results.append(out)
with (DATA/'errors_reference323.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
assert abs(results[-1]['dp_error_pct']-4.275130331185569)<1e-9
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.unicode_minus':False})
fig,axes=plt.subplots(2,3,figsize=(12.5,6.5),constrained_layout=True)
x=[int(z['grid'])/1e4 for z in results]
for ax,key,title in zip(axes.flat,metrics,['平均温度','最高温度','压降','Nu','换热系数 h','摩擦因子 f_D']):
    ax.plot(x,[z[key+'_error_pct'] for z in results],'o-',color='#246B8E',linewidth=1.5,markersize=4)
    ax.axhline(1,color='#B65035',linestyle='--',linewidth=1,label='1% 比较线')
    ax.axvline(REF/1e4,color='#777777',linestyle=':',linewidth=1)
    ax.set(title=title,xlabel='网格单元数 / 万',ylabel='相对323万档差异 / %')
    ax.grid(alpha=.18); ax.set_ylim(bottom=-.15)
axes[0,0].legend(fontsize=9)
fig.savefig(HERE.parent/'month3_mesh_errors_ref323.png',dpi=240,facecolor='white')
plt.close(fig)
mapping={
    'month3_mesh_flowfield.png':'尾迹速度温度压力_z1.50mm_标注版.png',
    'month3_mesh_outlet.png':'出口回流分布对比_标注版.png',
}
manifest=[]
for dest,source in mapping.items():
    p=SOURCE/source;shutil.copy2(p,HERE.parent/dest)
    manifest.append({'source':str(p),'copy':'../'+dest,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
for name,source in [('flowfield_notes.md','排查结论.md'),('flowfield_comparison.csv','两组定量对比.csv')]:
    p=SOURCE/source;shutil.copy2(p,DATA/name)
    manifest.append({'source':str(p),'copy':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(DATA/'flowfield_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
rawtable='\n'.join(f"{int(x['grid'])/1e4:.2f} & {float(x['t_avg']):.4f} & {float(x['t_max']):.4f} & {float(x['dp']):.3f} \\\\" for x in rows)
errtable='\n'.join(f"{int(x['grid'])/1e4:.2f} & {x['t_avg_error_pct']:.4f} & {x['t_max_error_pct']:.4f} & {x['dp_error_pct']:.4f} \\\\" for x in results)
block=r'''\textbf{（二）网格无关性检验}

本节以 NACA2416 的 $N_{\mathrm{ref}}=3\,235\,081$ 单元（以下简称323万档）
为\textbf{唯一对比参考}，统一分析七档网格的温度、压降、换热与流阻指标，
并补充流动场及出口截面图。参考档是本阶段的比较基准，不作为精确解。

\textbf{1. 统一比较条件与误差定义。}

七档结果统一取 $t=0.2\,\mathrm{s}$，最终时间步长均为 $0.001\,\mathrm{s}$。
461万档早期保留了一段 $0.0001\,\mathrm{s}$ 的推进历史，且其边界层设置和网格尺度策略
与323万档存在差别，比较时保留这些条件差异。
平均温度沿用全域单元算术平均，压降取液体入口与出口面积加权静压之差。
对所有指标统一计算
\begin{equation}
e_{\phi,i}=\frac{|\phi_i-\phi_{323}|}{|\phi_{323}|}\times100\%,
\qquad \phi\in\{\overline T,T_{\max},\Delta p,Nu,h_c,f_D\}.
\label{eq:mesh_error}
\end{equation}
式~\eqref{eq:mesh_error} 中分母始终取323万档对应指标，
温度与压降三项差异均不超过 $1\%$ 作为本轮联合比较线。
参考档自身差异为零仅由定义决定，不能据此宣布网格无关性通过。

\begin{table}[H]\centering
\caption{NACA2416 在 $0.2\,\mathrm{s}$ 的七档网格结果}
\label{tab:mesh}
\begin{tabular}{rrrr}\toprule
单元数 / 万 & $\overline T$ / K & $T_{\max}$ / K & $\Delta p$ / Pa \\
\midrule
RAWTABLE
\bottomrule\end{tabular}\end{table}

表~\ref{tab:mesh} 保留七档原始值，图~\ref{fig:month3_mesh} 展示其变化；
曲线沿用已有分析图，收敛判断以离散数据点为准。
\begin{figure}[H]\centering
\includegraphics[width=\textwidth]{figs/month3_mesh_temperature_pressure.png}
\caption{七档网格的平均温度、最高温度与静压差原始值}
\label{fig:month3_mesh}\end{figure}

\textbf{2. 全部相对323万档的定量比较。}

\begin{table}[H]\centering
\caption{以323万档为参考的温度与压降相对差异（\%）}
\label{tab:mesh_ref323}
\begin{tabular}{rrrr}\toprule
单元数 / 万 & 平均温度差异 & 最高温度差异 & 压降差异 \\
\midrule
ERRTABLE
\bottomrule\end{tabular}\end{table}

按表~\ref{tab:mesh_ref323}，294万档相对323万档的平均温度、最高温度和压降差异分别为
$0.0239\%$、$0.0057\%$ 和 $0.3201\%$，三项均低于 $1\%$。
两档绝对差分别为 $0.0726\,\mathrm{K}$、$0.0198\,\mathrm{K}$ 和 $7.518\,\mathrm{Pa}$，
表明294--323万附近存在局部接近区间。152万档压降差异为 $1.7722\%$，
不能将约150万单元认定为本组已验证的网格基准。
461万档相对323万档的平均温度、最高温度和压降差异分别为
$0.5537\%$、$0.1835\%$ 和 $4.2751\%$，压降仍超过比较线。
因此，统一以323万为参考后，局部两档接近与全部网格达到同一阈值仍需区分。

图~\ref{fig:month3_errors323} 将温度、压降和换热流阻指标的参考口径统一到323万档。
流体侧换热采用 $D_h=2.8070\,\mathrm{mm}$、$L=3.5\,\mathrm{mm}$；
物性取入口、出口质量流量加权温度平均值对应的数值。
323万档 $Nu=175.818$、$h_c\approx38210.0\,\mathrm{W/(m^2\cdot K)}$，
294万档相对其差异均约为 $0.11\%$。
461万档 $Nu=173.114$、$h_c\approx37621.5\,\mathrm{W/(m^2\cdot K)}$，
相对323万档差异均约为 $1.54\%$；$f_D$ 差异约为 $4.28\%$。
$Re$ 与 $Pr$ 接近主要反映入口及物性条件接近，不能替代换热与压降核查。

\begin{figure}[H]\centering
\includegraphics[width=0.98\textwidth]{figs/month3_mesh_errors_ref323.png}
\caption{各指标统一以323万档为参考的相对差异；虚线为 $1\%$ 比较线}
\label{fig:month3_errors323}\end{figure}

\textbf{3. 流动场与出口回流的图像核查。}

图~\ref{fig:month3_flowfield} 以323万档为参照，对照461万档在
$z=1.50\,\mathrm{mm}$ 平面的主流向速度、平面投影流线、温度与静压。
流线是三维速度在该平面的投影，黑色边界为 $U_x=0$，不能直接等同于完整三维流线。
两档均呈现翼型间主流加速、尾缘低速区和沿流向的压力降低；
局部逆向速度区的形状与范围存在差别。
原始图中两档使用相同变量色标，便于按323万档观察局部差异，
但二维图像本身不能证明空间离散误差已收敛。

\begin{figure}[H]\centering
\includegraphics[width=\textwidth]{figs/month3_mesh_flowfield.png}
\caption{以323万档（上排）为参照的中高平面流动场对比；下排为461万档，$t=0.2\,\mathrm{s}$}
\label{fig:month3_flowfield}\end{figure}

图~\ref{fig:month3_outlet} 进一步给出出口法向速度与温度分布。
323万档的回流面积比例为 $5.1720\%$，回流质量流量占入口流量的 $0.4754\%$；
461万档对应为 $5.3886\%$ 与 $0.2777\%$。
相对323万档，461万档回流面积比例增加约0.2167个百分点，
回流质量流量比例反而减少约0.1977个百分点，不能据此称其回流整体更严重。
两档回流面质量加权温度均为 $305\,\mathrm{K}$。
出口局部回流与内部尾迹应分别识别，不能只凭投影流线将二者混为一类。

\begin{figure}[H]\centering
\includegraphics[width=\textwidth]{figs/month3_mesh_outlet.png}
\caption{以323万档（上排）为参照的出口速度与温度对比；下排为461万档}
\label{fig:month3_outlet}\end{figure}

以相同统计区域的体积加权温度辅助核查时，323万档与461万档分别为
$305.7793\,\mathrm{K}$ 和 $305.8673\,\mathrm{K}$，
相对323万档仅约 $0.0288\%$。
这说明单元算术平均值受网格统计权重影响；七档主表仍保留原始统一口径，
两档体积加权数值单列说明，不能与其他档算术平均值混用。
流场与出口对比能定位差异位置，但未进行出口延长或回流温度敏感性重算，
不能把 $4.2751\%$ 的压降差异直接归因于某一种出口因素。

\textbf{4. 以323万为细档的 GCI 与阶段结论。}

GCI 沿用以323万为细档、从较粗网格选取对比档的已有结果，
采用三维等效尺度 $\ell=(V/N)^{1/3}$、安全系数 $F_s=1.25$。
294万与323万的细化比仅约1.032，尺度间隔较近。
107万、152万、323万组合的压降形式 GCI 为 $0.7275\%$，表观阶约5.57；
26万、107万、323万组合的 $Nu$ 与 $h_c$ 形式 GCI 约为 $7.13\%$ 与 $7.24\%$。
GCI 是三档网格外推指标，不等于式~\eqref{eq:mesh_error} 中的两档相对差异，
不能通过挑选最小的形式 GCI 认定全部指标通过。

本轮统一以323万档作为\textbf{后续诊断与成本折中的参考网格}，
294万档相对该参考的温度、压降和换热指标均较接近；
但461万档的压降与换热差异仍需解释，现有结果不支持全部网格均已通过联合检验。
其他构型资料另行保留，直线与混合结构的网格质量合格只表明准备条件满足，
gao2.1 较早批次也不与本节七档序列混用。
后续应统一初场、时间推进历史和网格策略，并以323万档为参照，
继续核查出口、近壁及尾迹区的敏感性。原始数据、统一误差表与流场出处均保留在源码目录。

'''.replace('RAWTABLE',rawtable).replace('ERRTABLE',errtable)
p=ROOT/'reports/逻辑月3_形态与物理.tex'
s=p.read_text(encoding='utf-8');reds=re.findall(r'\\textcolor\{red\}\{[^\n]*',s)
a=s.index(r'\textbf{（二）网格无关性检验}');b=s.index(r'\textbf{（三）机理分析',a)
mesh_red='\n'.join(x for x in reds if '图片说明' in x)
s=s[:a]+block+mesh_red+'\n\n'+s[b:]
s=s.replace('完整序列的压降尚未满足 $1\\%$ 联合判据，正式网格基准仍待复核。',
            '统一以323万为参考时，294万档温度与压降差异低于 $1\\%$；\n        461万档压降差异为 $4.2751\\%$，参考网格的适用范围仍待复核。')
assert all(x in s for x in reds)
assert '4.0999' not in s and '0.5507' not in s
p.write_text(s,encoding='utf-8')
(DATA/'README.md').write_text('''# 逻辑月3网格检验补充材料

当前报告的所有两档相对差异统一以 N=3235081 为分母。errors_reference323.csv 由 raw_02s.csv 和 dimensionless_02s.csv 计算，包含全部七档；不删除461万档，不将参考档零差异视为通过证明。

流场图取同批t=0.2 s的中高平面与出口截面，323万为上排参考、461万为下排对照。flowfield_notes.md 和 flowfield_comparison.csv 保留定量出处，flowfield_manifest.json 记录来源SHA256。原始说明可能保留早期参考口径，仅作历史证据；当前报告误差分析以 errors_reference323.csv 为准。

执行 finalize_month3_reference323.py 可从已归档CSV重新计算统一误差、作图，并导入本机既有流场图。update_month3_mesh.py 执行后也会调用该脚本生成当前版本。仅整理现有结果，未重新运行Fluent。
''',encoding='utf-8')
print('Updated month 3 with reference323 errors and two flow-field figures.')
