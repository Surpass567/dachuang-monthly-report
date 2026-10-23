# 中期报告补充稿：来源与复核

## 文件

- `reports/中期报告.tex` 与 `reports/中期报告.pdf` 是提交稿。
- 本目录中的 `final_report.tex` 是同一份最终 LaTeX 源码；`midterm_original.tex` 是构建脚本使用的原始报告底稿。
- `build_midterm.py` 保留旧稿重建能力；默认停止，指定 `--historical-only` 时只输出本目录中的 `historical_rebuilt.tex` 和历史清单，不覆盖当前报告。`verify_midterm.py` 检查当前中期 PDF 与日志，不再固定旧页数。
- `prepare_midterm_figures.py` 复算 PID 图并读取 Fluent HDF5 网格，生成对应图件。`figure_manifest.json` 记录报告图片的源文件、仓库文件名、SHA-256 和大小。
- `monthly_sources/` 保存逻辑月 1 至月 5 的整理时快照；`evidence/` 保存相关数值表、校核说明与仿真代码片段。

## 来源与适用范围

本目录 `monthly_sources/` 为重排前的历史快照，不能用其旧月份归属替代当前正文。2026-10-23 已同步中期报告：月一学习复现；月二小块探索和控制流程；月三翼型参数、UDF 修改、网格与数学 PID；月四分界线、Bi、数量和 XGBoost 待开展；月五整板尝试。当前稿直接维护在 `reports/中期报告.tex`，`final_report.tex` 同步为其副本。

几何图表示 CAD 结构。NACA 网格图来自已有 HDF5 网格文件的表面截取，未运行新的 Fluent 求解，也不是边界层剖面。物性拟合误差说明指定温压范围内的函数拟合一致性，不能替代绝对精度校核。PID 数值来自已保存数组及原仿真代码，不代表 Fluent 闭环控制。

复算 PID 图需要 `evidence/pid_sim.npz` 和脚本；重绘 NACA 网格图还需要 `mesh_figure_manifest.json` 中列出的原始 Fluent HDF5 网格文件，这些大文件未纳入仓库。月报快照、数值证据、脚本和已生成图件均保留供审阅。

## 版面检查

当前页数与编译结果以 [`../structure_validation.json`](../structure_validation.json) 为准；新版模板去掉开篇标题及元信息框，中期概述移入第一节，正文直接从第一节开始。编译日志中的字体路径提示取决于本机字体环境。
