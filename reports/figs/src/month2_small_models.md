# 逻辑月2补充说明

本版来自 E:/simulation/UDFwrite/upload_month2，源提交 f7692f1（逻辑月2补充小模型数据及网格温度配图）。报告已同步至 reports/逻辑月2_指标与形态.tex，保留原有控制文献内容。

新增 17 条代表分支：前面的流道形态与网格部分 4 条，NACA 部分 13 条。37 条原始提取记录中的网格变化、归档副本未重复视为独立模型。

small_model_results.csv 与 model_sources.json 保留所有原值和源文件路径。新增表格平均温度为固体单元算术平均，历史表格沿用原来的体积平均或底板平均口径。

配图直接读取 Fluent HDF5 Case 面节点及 Data 表面温度，不推进求解，也不进行几何重建。每个界面提取面元最多的坐标平面，六边形为 x-z 视图，其他模型为 x-y 视图；这些是界面平面面元，不宣称为内部体网格截面。温度图为加热面局部值，采用各自色标，不能把图上最大值当作固体全域最大值。

复现：从仓库根目录运行 python reports/figs/src/build_small_model_figures.py，然后在 reports 内用 XeLaTeX 或 Tectonic 编译同名 tex。输入汇总位于本目录，源 Case/Data 文件须可读。update_month2.py 是一次性正文插入脚本，当前报告已完成插入，无需再次执行。
