"""Import the existing mesh study into month 3; no Fluent rerun."""
from pathlib import Path
import csv
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT.parent / 'UDFwrite' / '网格无关性报告'
HERE = Path(__file__).resolve().parent
DATA = HERE / 'month3_mesh_data'
DATA.mkdir(exist_ok=True)
inputs = {
    'raw_02s.csv': SOURCE/'data/analysis_02s_20261009/原始数据_0.2s.csv',
    'dimensionless_02s.csv': SOURCE/'data/dimensionless_02s_20261009/无量纲原始指标.csv',
    'gci_notes.md': SOURCE/'data/gci_without_4610k_20261009/GCI判断说明_不含461万.md',
    'comparison_notes.md': SOURCE/'data/analysis_02s_20261009/检验结论.md',
    'mesh_preparation.md': SOURCE/'data/mesh_preparation/网格无关性检验汇总_20260920.md',
}
for name, source in inputs.items():
    shutil.copy2(source, DATA/name)
figs = {'month3_mesh_temperature_pressure.png': 'naca_all.png',
        'month3_mesh_dimensionless.png': 'dimensionless.png'}
for name, source in figs.items():
    shutil.copy2(SOURCE/'figures'/source, HERE.parent/name)
manifest = [{'source':str(p),'copy':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
            for name,p in inputs.items()]
(DATA/'source_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
with (DATA/'raw_02s.csv').open(encoding='utf-8-sig',newline='') as f:
    rows=list(csv.DictReader(f))
by_n={int(x['grid']):x for x in rows}
err=lambda x,y:abs(float(x)-float(y))/abs(float(y))*100
coarse,mid,fine=(by_n[n] for n in (2943269,3235081,4610769))
assert abs(err(mid['dp'],fine['dp'])-4.099856)<1e-5
table='\n'.join(f"{int(x['grid'])/1e4:.2f} & {float(x['t_avg']):.4f} & {float(x['t_max']):.4f} & {float(x['dp']):.3f} \\\\" for x in rows)
block=r'''\textbf{（二）网格无关性检验}

本阶段补充整理了 NACA2416 在统一物理时刻下的七档网格结果，
并结合换热指标、GCI 及前期其他构型的资料，核查网格选择依据。
\textbf{网格质量合格、局部两档结果接近与完整序列通过网格无关性检验是不同层次的判断}，
不能仅由单元总数确定后续全部模型的精度。

\textbf{1. 比较条件与判据。}

NACA2416 七档单元数为 26.02 万至 461.08 万，比较时刻统一为
$t=0.2\,\mathrm{s}$，最终时间步长均为 $0.001\,\mathrm{s}$。
前六档由 $0.1\,\mathrm{s}$ 续算；461 万档在早期保留了一段
$0.0001\,\mathrm{s}$ 的小步长历史，因此最终时刻与最终步长相同仍不等于时间推进历史完全一致。
平均温度沿用原记录的\textbf{全域单元算术平均}，不是体积加权平均；
压降取液体入口与出口的面积加权静压之差。
相对参考网格误差定义为
\begin{equation}
e_{\phi,i}=\frac{|\phi_i-\phi_{\mathrm{ref}}|}{|\phi_{\mathrm{ref}}|}\times100\%,
\qquad \phi\in\{\overline T,T_{\max},\Delta p\}.
\label{eq:mesh_error}
\end{equation}
本轮以三项误差均不超过 $1\%$ 为联合比较判据，同时检查相邻加密后的变化；
某一粗网格偶然接近参考结果不能单独证明已进入稳定平台。

\begin{table}[H]
\centering
\caption{NACA2416 在 $0.2\,\mathrm{s}$ 的七档网格结果}
\label{tab:mesh}
\begin{tabular}{rrrr}
\toprule
单元数 / 万 & $\overline T$ / K & $T_{\max}$ / K & $\Delta p$ / Pa \\
\midrule
TABLE_ROWS
\bottomrule
\end{tabular}
\end{table}

表~\ref{tab:mesh} 与图~\ref{fig:month3_mesh} 表明，温度与压降并未随加密共同单调收敛。
图中曲线沿用已有分析图，判断以原始离散数据点为准。
\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{figs/month3_mesh_temperature_pressure.png}
\caption{NACA2416 七档网格的平均温度、最高温度与面积加权静压差}
\label{fig:month3_mesh}
\end{figure}

\textbf{2. 局部平台与完整序列的区别。}

294.33 万与 323.51 万两档的平均温度相差 $0.0726\,\mathrm{K}$，
最高温度相差 $0.0198\,\mathrm{K}$，压降相差 $7.518\,\mathrm{Pa}$。
按式~\eqref{eq:mesh_error}，以 323.51 万为参考时，三项差异分别为
$0.0239\%$、$0.0057\%$ 和 $0.3201\%$，可视为当前批次的\textbf{局部接近区间}。
但以 461.08 万为参考时，323.51 万档的平均温度、最高温度和压降误差分别为
$0.5507\%$、$0.1832\%$ 和 $4.0999\%$；温度两项低于 $1\%$，压降仍不满足要求。
152.49 万档相对 461.08 万档的压降误差也为 $2.4003\%$，
因此现有数据不支持将约 150 万单元认定为已验证的通用网格基准。

\textbf{3. 换热与流阻指标的交叉核查。}

进一步比较同批结果的 $Re$、$Pr$、$Nu$、换热系数 $h_c$ 和达西摩擦因子 $f_D$，
其中 $h_c$ 与 $f_D$ 按流体侧壁面换热及入口至出口压差计算。
本组统一水力直径 $D_h=2.8070\,\mathrm{mm}$，流道长度 $L=3.5\,\mathrm{mm}$；
流体参考温度为入口、出口质量流量加权温度的平均值，物性取该温度下的数值。
图~\ref{fig:month3_mesh_dim} 中，$Re$ 约为 6602、$Pr$ 约为 5.807，变化较小；
294.33 万与 323.51 万档的 $Nu$ 分别为 175.628 和 175.818，
$h_c$ 分别约为 38168.7 和 38210.0 $\mathrm{W/(m^2\cdot K)}$，
二者差异约为 $0.11\%$。
461.08 万档的 $Nu$ 降至 173.114，$h_c$ 降至
37621.5 $\mathrm{W/(m^2\cdot K)}$，说明仅看温度接近仍不足以确认换热与流阻均已稳定。

\begin{figure}[H]
\centering
\includegraphics[width=0.96\textwidth]{figs/month3_mesh_dimensionless.png}
\caption{同批七档网格的换热与流动指标对比}
\label{fig:month3_mesh_dim}
\end{figure}

\textbf{4. GCI 核查与当前结论。}

已有 GCI 分析采用截至 323.51 万的六档网格，461.08 万档仍保留在完整对比中，
不并入该组 GCI 计算。按三维等效尺度 $\ell=(V/N)^{1/3}$，
294.33 万与 323.51 万的细化比仅约为 1.032。
107.36 万、152.49 万、323.51 万组合的压降形式 GCI 为 $0.7275\%$，
但表观阶约为 5.57；换用 26.02 万、107.36 万、323.51 万组合时，
$Nu$ 与 $h_c$ 的形式 GCI 分别约为 $7.13\%$ 与 $7.24\%$。
因此不能挑选单个较小 GCI 值，宣称传热与压降已共同通过 $1\%$ 标准。

其他构型的资料应分别使用：直线与混合结构已完成三档 Poly-Hexcore 网格准备，
规模分别约为 101--496 万与 165--488 万，网格检查通过；
这只说明具备对比计算的准备条件。gao2.1 的较早数据与本节七档结果属于不同批次，
不能拼接成同一条收敛序列，也不能据此补齐正弦流道的通过结论。

综上，当前成果是\textbf{完成多档结果整理并定位约 300 万附近的局部平台}，
323.51 万可作为后续诊断与计算成本折中的候选网格，尚不能作为最终通过结论。
后续需统一初场、时间推进历史和网格加密策略，复核出口回流及温度统计口径，
再以传热与压降联合判据确定正式基准。现阶段不把最细档差异直接归因于某一种边界因素。
原始数据、判据说明与文件指纹保留在配图源码目录，供后续复核。

'''.replace('TABLE_ROWS',table)
p=ROOT/'reports/逻辑月3_形态与物理.tex'
s=p.read_text(encoding='utf-8')
reds=re.findall(r'\\textcolor\{red\}\{[^\n]*',s)
a=s.index(r'\textbf{（二）网格无关性检验}')
b=s.index(r'\textbf{（三）机理分析',a)
red_mesh='\n'.join(x for x in reds if '图片说明' in x)
s=s[:a]+block+red_mesh+'\n\n'+s[b:]
s=s.replace('网格无关性检验 & 已完成 & 约 150 万网格作为后续划分基准',
            '网格无关性检验 & 阶段完成 & 完成七档对比；约 300 万局部接近，联合判据待复核')
s=s.replace('四种流道均已通过网格无关性检验，形成约 150 万网格的后续划分基准。',
            '已完成 NACA2416 七档网格结果整理，294 万与 323 万档局部接近；\n        完整序列的压降尚未满足 $1\\%$ 联合判据，正式网格基准仍待复核。')
assert all(x in s for x in reds), 'Original red text must remain intact'
assert s.count(r'\section{')==5
p.write_text(s,encoding='utf-8')
(DATA/'README.md').write_text('''# 逻辑月3网格检验补充材料

数据来自既有网格无关性阶段报告，未重新运行 Fluent。温度为全域单元算术平均；压降为液体入口至出口面积加权静压差。七档均取 t=0.2 s，最终步长0.001 s；最细档早期有不同步长历史。

- raw_02s.csv：表格与温度、压降误差复核数据。
- dimensionless_02s.csv：Re、Pr、Nu、h、f_D 数据。
- comparison_notes.md / gci_notes.md：原始判据、GCI组合与局限。
- mesh_preparation.md：其他结构仅完成网格准备的证据。
- source_manifest.json：来源与SHA256。

update_month3_mesh.py 从工作区原始报告整理数据并更新月3网格段；同目录数据可用于独立复核数值。正式配图位于 reports/figs/，沿用原始分析图，以离散数据点判断。未声明已通过完整网格无关性检验。
''',encoding='utf-8')
print('Updated month 3; preserved all original red text.')
