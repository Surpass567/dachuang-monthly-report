# 中期报告补充稿：来源与复核

## 文件

- `reports/中期报告.tex` 与 `reports/中期报告.pdf` 是提交稿。
- 本目录中的 `final_report.tex` 是同一份最终 LaTeX 源码；`midterm_original.tex` 是构建脚本使用的原始报告底稿。
- `build_midterm.py` 读取五个月度报告快照与证据文件，更新报告和配图引用；`verify_midterm.py` 检查最终 PDF 页数、编译日志、引用和图片路径。
- `prepare_midterm_figures.py` 复算 PID 图并读取 Fluent HDF5 网格，生成对应图件。`figure_manifest.json` 记录报告图片的源文件、仓库文件名、SHA-256 和大小。
- `monthly_sources/` 保存逻辑月 1 至月 5 的整理时快照；`evidence/` 保存相关数值表、校核说明与仿真代码片段。

## 来源与适用范围

报告结合月报正文、表格和引用图片补充。月 1 的历史温度场图只作为流程记录，图注说明了其边界条件与当前单相水计算的差异；月 2 的 17 个代表分支、月 3 的网格与流场对比、物性 UDF 复核、PID 仿真、整板 CAD 和连接件 CAD 按各自证据范围描述。月 4、月 5 尚未完成的系统级计算作为后续验证任务呈现。

几何图表示 CAD 结构。NACA 网格图来自已有 HDF5 网格文件的表面截取，未运行新的 Fluent 求解，也不是边界层剖面。物性拟合误差说明指定温压范围内的函数拟合一致性，不能替代绝对精度校核。PID 数值来自已保存数组及原仿真代码，不代表 Fluent 闭环控制。

复算 PID 图需要 `evidence/pid_sim.npz` 和脚本；重绘 NACA 网格图还需要 `mesh_figure_manifest.json` 中列出的原始 Fluent HDF5 网格文件，这些大文件未纳入仓库。月报快照、数值证据、脚本和已生成图件均保留供审阅。

## 版面检查

最终 PDF 共 45 页。自动检查为 0 个 overfull、0 个缺字、0 个 LaTeX 错误、0 个未定义引用和 0 个缺失图片；页面已逐页通过联系页检查。编译日志中的字体路径提示取决于本机字体环境。
