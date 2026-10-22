# 逻辑月3网格检验补充材料

数据来自既有网格无关性阶段报告，未重新运行 Fluent。温度为全域单元算术平均；压降为液体入口至出口面积加权静压差。七档均取 t=0.2 s，最终步长0.001 s；最细档早期有不同步长历史。

- raw_02s.csv：表格与温度、压降误差复核数据。
- dimensionless_02s.csv：Re、Pr、Nu、h、f_D 数据。
- comparison_notes.md / gci_notes.md：原始判据、GCI组合与局限。
- mesh_preparation.md：其他结构仅完成网格准备的证据。
- source_manifest.json：来源与SHA256。

update_month3_mesh.py 从工作区原始报告整理数据并更新月3网格段；同目录数据可用于独立复核数值。正式配图位于 reports/figs/，沿用原始分析图，以离散数据点判断。未声明已通过完整网格无关性检验。
