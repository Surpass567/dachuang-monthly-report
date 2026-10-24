# 更新记录

## 2026-10-25 — 新增 docs/GitHub使用说明（面向不熟悉 Git 的队友）

仓库新增面向新队员的上手文档：[Markdown 版](docs/GitHub使用说明.md) 与 [PDF 版](docs/GitHub使用说明.pdf)（11 页）。内容覆盖：

- Git 安装、身份配置与 Windows 三条必配（`core.quotepath`／`core.autocrlf`／`credential.helper`）
- 首次登录、Personal Access Token（PAT）生成、协作者权限确认
- **让 AI 代执行 git 操作**的前置条件清单、话术表与「一次说清」的模板
- 推送被拒、合并冲突、CRLF 警告、中文文件名、大文件、误删恢复的处理方法
- 六条危险操作黑名单（`git push --force`、`git reset --hard` 等）
- 本仓库的具体规矩（编译两遍、`check.py` 三项为 0、图片放 `figs/`、提交信息用中文）

同步在 [README](README.md) 增加「新人上手」章节并更新目录结构，指向该文档。本次仅新增文档与 README 说明，未改动任何报告内容。

## 2026-10-25 — 中期报告：删除待补充列与表 2-12，参考文献扩充到 20 条

按「表格中【待补充】所在列直接删除、表格居中、参考文献不要列太少、表 2-12 直接删除」处理[中期报告](reports/中期报告.tex)，正文论述与数据未改动：

- **红字检查**：全文已无 `\textcolor{red}` 标注（0 处），无需处理。
- **删除整列待补充**：逐列统计各表 `\TBD` 占比，只删「除表头外没有任何真实内容」的列，共 9 列——表 2-3、2-6、2-7 的第 3 列，表 2-8 的第 2、3 列，表 2-9、2-10、2-11 的第 3 列，以及表 4-1 的「时间」列（longtable，`\multicolumn` 列数同步由 5 改 4）。保留列中的零星 `\TBD` 改为「—」，全篇「待补充」出现次数归零。
- **表格居中**：上述 7 张 `tabularx` 表列类型由 `lY` 改为 `CC`，longtable 的 `p{}` 列改为 `\centering`，避免删列后内容左对齐、右侧留白。
- **删除表 2-12**：整表删除「CFD 与代理模型计算开销记录模板」，并改写正文中对它的引用（改为说明实测计时尚未开展）。
- **参考文献扩充**：由 4 条增至 **20 条**，新增条目全部取自仓库内已核实文献（[逻辑月1](reports/逻辑月1_基础建立.tex)、[逻辑月2](reports/逻辑月2_指标与形态.tex)、[逻辑月3](reports/逻辑月3_形态与物理.tex) 的文献表）与项目计划书，未引入未经核实条目；[文献表](reports/中期报告.tex)由 3 行扩至 13 行，并在区域化冷板、最小闭环 PID、物理灰箱模型三处补充正文引用，20 条文献全部被正文引用。
- **修掉参考文献前的整页空白**：`\begin{thebibliography}` 前原有 `\FloatBarrier` + `\Needspace{27\baselineskip}`，要求预留约 16 cm，导致第 35 页正文结束后空 13.8 cm 才另起一页。改为 `\Needspace{8\baselineskip}` 并去掉该 `\FloatBarrier`，参考文献紧接正文排版，全篇由 39 页降至 **38 页**。
- **图表引用完整性**：逐条核对 37 个图表 label，合并组图的父标签 `fig:05-06` 原先未被正文引用，已在正文补入整板几何那一句的父图引用；现 28 张表、9 幅图（含组图）全部在正文被引用，无「有图无引」条目。

验证：xelatex 干净重建三遍，Overfull=0、Missing character=0、Error=0、未定义引用 0；`python check.py` 对全部 6 份报告与 2 份骨架均通过；[PDF](reports/中期报告.pdf) 38 页，表号连续（第二章止于表 2-11）、参考文献编号至 [20]、全文「待补充」0 处；逐页扫描空白带，除封面、目录、末页外仅第 7、12 页存在 3.0 cm 与 4.1 cm 的浮动体空隙。

## 2026-10-24 — 中期报告云图改为单张组图，42 页降至 39 页

针对「第 23–25 页大图太突兀」的问题，[中期报告](reports/中期报告.tex)的三组复现云图原先各自使用 `[p]` 强制浮动页，连续三页各被一张 2×2 彩色云图占满、上下留白明显。本轮改为：

- **三张整页浮动合并为一张 3×4 组图**（图 3-1）：行为方形／六边形／圆形微通道并加行首标题，列为水侧温度、水侧表压、水侧速度大小与铜基板温度，列名只写在首行，共 12 个子图；父图注说明行列含义与色标口径。面板宽度 0.235 版心，整图约占半页。
- **正文引用改为单处**：原「图 3-1、图 3-2 至图 3-3」改为「图 3-1」，`fig:repro-square/hex/round` 三个标签合并为 `fig:repro`。
- **浮动位置放宽**：全文 41 处 `[htbp]` 改为 `[!htbp]`，减少浮动体被推迟而产生的整页空白。
- **删除组图后的 `\FloatBarrier`**：该屏障会把待定浮动体一次性输出，造成只有图、没有正文的整页。

验证：xelatex 干净重建三遍，Overfull=0、Missing character=0、Error=0、未定义引用 0；`python check.py reports/中期报告.tex` 全部通过；[PDF](reports/中期报告.pdf) 由 42 页降至 **39 页**，全篇仅末页存在正常收尾留白。正文文字与数据未改动。

## 2026-10-24 — 中期报告压缩排版：59 页降至 42 页

按「页数偏多、行距调小、非流程图图片合并、流程图字号接近正文」的要求，调整[类文件版式](template/midterm.cls)与[中期报告](reports/中期报告.tex)的图组，正文内容未改动：

**版式压缩**（[类文件](template/midterm.cls)）
- 行距 `\linespread` 1.5 → 1.15；页边距上下 2.54→1.9 cm、左右 3.17→1.8 cm，版心由 14.66×24.6 cm 增至 17.4×25.9 cm
- 标题段前段后由 2.2/1.8 ex 收到 1.6/1.2 ex（三级同比例收紧）；图表题注间距 6→3 pt
- 浮动体参数放宽（`\topfraction` 0.92、`\textfraction` 0.05、topnumber 4、totalnumber 6），缩小 `\floatsep`/`\textfloatsep` 以减少浮动体留下的空白

**流程图字号**：11 张概念图此前按 0.98 版心插入，图内文字等效仅 8.1 pt（正文 12 pt）。改为满版心插入并配合页边距收窄后，等效约 **10.4 pt**，与正文接近；经测量这些图墨迹占页宽 97%，无可裁留白，故不再裁边。

**非流程图合并**（[中期报告](reports/中期报告.tex)）：把相邻的单图两两并成 `subfigure` 双列组图，共 6 组——整板 CAD 与条带接缝、流固界面网格与七档温度静压、参考相对差异与无量纲指标、两种网格档流场与出口、物性曲线与 1601 点误差、两种物性实现结果与耗时。原 `\label` 保留在子图上，正文 `\ref` 自动变为「图 N-Ma」形式，引用关系不变。

验证：xelatex 干净重建三遍，Overfull=0、Missing character=0、Error=0、未定义引用 0；`python check.py reports/中期报告.tex` 全部通过；[PDF](reports/中期报告.pdf) 由 59 页降至 **42 页**（原蓝色月度模板版本为 44 页）。

## 2026-10-24 — 中期报告正式版式收尾：封面、中文断行与长表格

[中期报告](reports/中期报告.tex)改用[正式版式类文件](template/midterm.cls)后（随 `9d61316` 入库），本轮修掉三处遗留问题，使其达到可打印的正式程度：

- **封面**：组员一行 5 人在小四字号下超出下划线框，改为「标签 5.4em + 值栏 0.60 版心、值用小四」；封面底部原同时打印「截至中期检查（2026 年 10 月）」与「二〇二六年十月」，改为只保留后者，日期不再重复。实现见[类文件封面段](template/midterm.cls)。
- **中文断行**：[类文件](template/midterm.cls)补入 `\XeTeXlinebreaklocale "zh"`、`\XeTeXlinebreakskip`、`\tolerance=3000`、`\emergencystretch=3em` 后，两处正文段落超框（23.27 pt、8.59 pt）消失；此前缺失该设置会让中文长段落断不开。
- **长表格**：[中期报告](reports/中期报告.tex)「下一阶段任务、里程碑与建议分工」表五列宽度合计 0.91 版心，叠加 5 列 × 2 × 4 pt 列间距后超出 2.45 pt；第三列由 0.31 收窄至 0.29（合计 0.89），该表 5 处对齐超框一并消除。

验证：xelatex 干净重建三遍，Overfull=0、Missing character=0、Error=0、未定义引用与引文均为 0，[中期报告 PDF](reports/中期报告.pdf) 59 页；封面、目录、正文标题、图题在下/表题在上、三线表浅灰表头均按正式版式输出。未改动正文内容与图表数据。

## 2026-10-24 — 汇总最新报告与配套资料发布到 main

将本地待发布修订统一提交到 `main`：包括[月一](reports/逻辑月1_基础建立.tex)小块理论及配图、[月二](reports/逻辑月2_指标与形态.tex)合并图及联合分析、[月三](reports/逻辑月3_形态与物理.tex)与[中期报告](reports/中期报告.tex)的 UDF 四面板组图、中期正文修订及概念图，以及[中期汇报框架](reports/中期汇报_PPT框架.md)和[学校报告模板](reports/本科生科研训练中期+结题报告模板-20251023.docx)。源文件、同名 PDF、配图和复现资料随本次更新一起上传；具体章节调整见下方记录与本次文件差异。

发布检查补齐月一正文引用但缺失的两张配图：原始素材移入[输入目录](reports/figs/src/month1_block_inputs/)，同步[生成脚本](reports/figs/src/prepare_month1_block_figures.py)输入路径。归档[本机编译环境脚本与说明](reports/figs/src/latex_environment/README.md)，共享[类文件](template/ydzjreport.cls)增加可重定义的收尾落款 `ydzjclosingnote`。同步[主目录](README.md)页数及[报告目录](reports/README.md)文件说明。

验证：`python check.py` 对全部当前报告和空白骨架的静态检查通过；本机无独立 XeLaTeX，使用[发布检查脚本](reports/figs/src/verify_upload.py)调用 Tectonic 离线实际编译，六份报告及两份骨架的 Overfull、Missing character、Error、未定义引用均为 0，记录于[upload_validation.json](reports/figs/src/upload_validation.json)。月一至月五分别为 10、11、16、8、4 页，中期报告 44 页；四份本轮修改报告的正式 PDF 已由当前源文件重新生成。上传前获取并合并远端，保留双方内容；按仓库规则推送 `origin/main` 后再次核对分支差异及工作区。未运行新的数值仿真。

## 2026-10-24 — UDF 配图改为 A–D 四面板组图

按“使用手工导出的 A、B、C、D 四张 PNG 搭配成组图、替换现有 UDF 图片”的要求，将[逻辑月3](reports/逻辑月3_形态与物理.tex)「UDF 正式修改与验证」与[中期报告](reports/中期报告.tex)「从接口学习到数值自检」中的单张合成图替换为四个 `subfigure` 组成的组图：上排 A 常用接口、B 密度接口示例，下排 C 编译与挂接流程、D 三种水物性实现方式。两处保持原有图号与主图注，仅新增 (a)–(d) 子图注；正文、数据与结论未改动。

报告用图为 `reports/figs/udf_learning_interfaces_a.png` 至 `_d.png`，由手工导出的透明 PNG 压白生成；源文件、导出原图和复现脚本归档在[图源目录](reports/figs/src/month3_figure2/README.md)，旧单张合成图与旧 drawio 草稿移入该目录 `archive/`，不再被报告引用。同步更新[报告图片目录](reports/README.md)与中期图源清单。

验证：使用本机 Tectonic 离线编译两份报告，日志中 Missing character、Overfull、Error 与未定义引用均为 0；[月三 PDF](reports/逻辑月3_形态与物理.pdf)共 16 页，[中期报告 PDF](reports/中期报告.pdf)共 44 页；已渲染检查月三第 6 页、中期第 10 页的四面板组图与图注。本次未新增仿真或改动数值。

## 2026-10-24 — 新增中期汇报 PPT 框架与图文脚本

按「文字尽量少、图表搭配、信息密度高」的要求，基于[中期报告](reports/中期报告.tex)整理[中期汇报 PPT 框架](reports/中期汇报_PPT框架.md)：确定「问题→对象→平台可信度→三方向结果→结论边界→里程碑」叙事线，给出 16 页正文 + 3 页附录的逐页版式、标题与结论句、数字卡、图上标注、图注、页脚口径与讲稿；并列出视觉规范、16 项素材的处理方式（概念图 PDF 导出、30–35 系列裁标题与脚注）、口径禁忌表及下一步 python-pptx 生成参数。所有数值逐项取自中期报告表 8、表 12、表 15、表 23、图 11、图 16–17，并与 §3.1–§3.3 正文逐一核对，未新增仿真或改动报告与配图。本次仅交付框架，未生成 `.pptx`；[报告目录](reports/README.md)已登记该文件。

## 2026-10-24 — 合并逻辑月2的图2、图3及对应分析

在[月二源文件](reports/逻辑月2_指标与形态.tex)「成果总结 → 仿真结构设计展示与分析」中，将原四种流道的16幅后处理云图与三种代表小模型的网格、加热面温度合并为同页图2，删除独立图3并统一引用；原有图像直接由 LaTeX 排列，不修改源图或数值。图后保留22条性能记录与保存条件表，分散的分析整合至「各类小块的联合分析」，统一说明温度与水力代价、网格及色标解读、不同工况的比较边界；明确 gao2.1 上下两组分别为500和600 W/cm$^2$。修正表前记录数量说明，保留当前其他正文编辑。

[合并脚本](reports/figs/src/merge_month2_figures.py)、[验证记录](reports/figs/src/month2_merge_qa/validation.json)和[报告目录](reports/README.md)同步；个人 LaTeX 配置不纳入本次发布内容。`python check.py reports/逻辑月2_指标与形态.tex` 静态检查通过，使用本机全局编译器完成离线编译，Overfull、Missing character、Error、未定义引用均为0；第6页合并图与第8页联合分析渲染核对通过。[同名 PDF](reports/逻辑月2_指标与形态.pdf)更新为11页。本次保存本地，未上传。

## 2026-10-23 — 逻辑月4 补入四种流道温度趋势、工况表与适用区间结论

按「在四种流道形态之后补入温度分辨的图片、表格与结论」的要求，在[月四](reports/逻辑月4_迭代与调试.tex)「完成情况」部分新增 3.3 节「四种流道的温度表现与适用热流密度区间」：图 1 为四种流道的最高温度、体均温度、压差与峰值—平均温差随热流密度的变化；图 2 为 150--300 W/cm$^2$ 共同数据点的四项比较；图 3 为归一化温升、峰值热阻与水力代价；图 4 为 gao2.1 在 500--1050 W/cm$^2$ 的热点与压差；图 5 为正弦瞬态与表列稳态的对照。表 2 为四种流道的工况与几何核对，表 3 为适用区间与依据。

结论按现有数据明确为三条：中低热流密度下直线与正弦性能较好；NACA2416 的压降控制最好（压差为直线的 31.8%、正弦的 19.9%），适合在中低热流密度下以减少压降为目标时采用；gao2.1 覆盖 500--1050 W/cm$^2$，适合高热流密度下的应对与处理。曲线、表格与月二保存记录的排序一致。

配图取自现有的四种流道分析报告与折线图，新增 `figs/30_四流道总览.png`、`31_共同热流密度比较.png`、`32_归一化指标与水力代价.png`、`33_gao2.1高热流密度.png`、`35_正弦稳态对照.png` 五张；末步温度变化一张未采用，未入库。同步更新[报告目录](reports/README.md)的月四说明与配图表。

验证：`python check.py 逻辑月4_迭代与调试.tex` 全部通过；`xelatex` 两遍编译，Overfull、Missing character、Error 与未定义引用均为 0；PDF 共 8 页。

## 2026-10-23 — 汇总本轮全部报告修订并发布到 main

按“全部更新上传”的指令，将此前本地保存的五个月报及[中期报告](reports/中期报告.tex)的源文件和同名 PDF、[共享模板](template/ydzjreport.cls)、两份空白骨架、[标题及表格规范](CONTRIBUTING.md#报告结构与标题层级)、[配套脚本及核查记录](reports/figs/src/README.md)、[报告目录](reports/README.md)和本更新记录一起提交到 `main`，同步更新文档中的发布状态。具体章节、文件位置与验证结果见下两条记录。上传前获取并合并 `origin/main`，保留远端和本地有效内容；推送后再次获取并检查分支差异和工作区状态。未新增数值仿真或补造待补数据。

## 2026-10-23 — 统一五部分结构、标题层级与表格，纠正月二小块数据拆分

按补充要求修改[月一](reports/逻辑月1_基础建立.tex)、[月二](reports/逻辑月2_指标与形态.tex)、[月三](reports/逻辑月3_形态与物理.tex)、[月四](reports/逻辑月4_迭代与调试.tex)、[月五](reports/逻辑月5_整板尝试.tex)和[中期报告](reports/中期报告.tex)，并重新生成同名 PDF。正文均按“本月计划、研究过程、完成情况、问题与初步对策、下个月计划”排列；完成状态从计划中移至第三部分。月一将软件、物理与 UDF、小块理论、自控基础分层，使用三级和四级标题；各报告的结构与控制方向按主题组织。

月二“完成情况 → 全部小块的合并展示与分析”恢复全部17条小模型保存分支，与5条既有流道记录合为22条性能记录；六翼型基准表也纳入同一部分。增加全部分支的流量/时刻/时间步条件表及跨类型综合分析，纠正原先只保留非 NACA 的拆分方式。原始 [CSV](reports/figs/src/small_model_results.csv) 不变，同一几何的设置分支不重复计作新结构；月三保留参数分组与数值验证专题。

[基础说明](CONTRIBUTING.md#报告结构与标题层级)、[根目录入口](README.md)、[报告目录](reports/README.md)和[迁移说明](reports/figs/src/结构调整说明.md)同步。共享[类文件](template/ydzjreport.cls)支持自动编号的四级独立行标题，并统一三线表、浅蓝表头、表题、字号与间距；两份空白骨架按五部分重写。[结构迁移脚本](reports/figs/src/revise_report_outline.py)及[表格统一脚本](reports/figs/src/unify_report_tables.py)归档于规定目录，旧基线脚本增加防覆盖检查；中期 `final_report.tex` 副本同步。

验证：六份报告均通过离线编译、引用与日志检查，Overfull、Missing character、Error 和未定义引用均为0，见[验证记录](reports/figs/src/structure_validation.json)。[层级与数据核查](reports/figs/src/outline_data_audit.json)确认六份正文各有固定五部分、无标题跳级，月二22条记录与原始数值一致；两份空白模板编译通过。PDF 联系页已逐份检查。未运行新仿真，未提交或上传。

本文件统一记录更新内容、具体位置和验证结果；每次修改与对应文件一起提交到 `main`。更早的过程文档保存在 `archive/full-20261015` 分支。

## 2026-10-23 — 本地重排五个逻辑月并取消开篇信息框

按确认的研究顺序调整现有内容：学习复现、探索尝试、优化验证、迭代调试、整板尝试。**本次仅保存本地修改，按要求未提交、未上传。**

| 更新内容 | 文件与章节 |
|---|---|
| 月一保留软件与文献复现、基础物理和 UDF 入门、自控基础，突出初步小块理论形成 | [月一正文](reports/逻辑月1_基础建立.tex)「阶段一：通读与摘录」「阶段二：导出与复现」「初步小块理论的形成」及[PDF](reports/逻辑月1_基础建立.pdf) |
| 月二保留代表结构探索，移入传统 PID 学习与控制流程图；详细翼型表和数学模拟后移 | [月二正文](reports/逻辑月2_指标与形态.tex)「研究进展 → 关键结果」及[PDF](reports/逻辑月2_指标与形态.pdf) |
| 月三集中翼型参数分组、六翼型与十三分支、正式 UDF 修改、网格检验和 PID 数学模拟 | [月三正文](reports/逻辑月3_形态与物理.tex)「研究进展 → 翼型专题与数值验证」及[PDF](reports/逻辑月3_形态与物理.pdf)；参数组完整数据明确待补，历史分支不当作完整扫描 |
| 月四改为小块选择分界线、复杂性与性能、Bi、扰流柱数量和 XGBoost 准备 | [月四正文](reports/逻辑月4_迭代与调试.tex)「研究进展」及[PDF](reports/逻辑月4_迭代与调试.pdf)；由原“连接成网络”同步更名，XGBoost 明确尚未开展 |
| 月五吸收网络、连接、分流与控制接口，围绕整板尝试及验证准备组织 | [月五正文](reports/逻辑月5_整板尝试.tex)「整板布局与连接尝试」「后续验证方案」及[PDF](reports/逻辑月5_整板尝试.pdf)；由原“整板验证”同步更名 |
| 中期报告同步月份归属、待补状态及引文，保留已有累计数值依据 | [中期正文](reports/中期报告.tex)「五个逻辑月的成果承接」「承接月4理论迭代与月5整板尝试」及[PDF](reports/中期报告.pdf) |
| 模板 v1.4 取消开篇标题、日期与信息框；正文直接从第一节开始，主题与署名保留在页眉 | [共享模板](template/ydzjreport.cls) `ydzjmakereporthead`、`stageonesetup`、`stagetwosetup`；[阶段一骨架](template/阶段一_空白骨架.tex)、[阶段二骨架](template/阶段二_空白骨架.tex)同步说明；中期概述移入第一节 |
| 更新目录、迁移说明与复现脚本；避免旧快照脚本覆盖当前中期稿 | [主目录](README.md)、[报告目录](reports/README.md)、[调整说明](reports/figs/src/结构调整说明.md)、[重排脚本](reports/figs/src/restructure_monthly_reports.py)、[验证脚本](reports/figs/src/validate_restructured_reports.py)、[中期复现说明](reports/figs/src/midterm_expanded/README.md) |
| 修复中期自检中 reportfigure 宏标签和图片参数的误报，取消旧验证脚本固定45页的限制 | [自检](check.py) `check_refs`、[中期验证](reports/figs/src/midterm_expanded/verify_midterm.py) |

验证：`python check.py` 对六份当前报告的括号、图片及交叉引用静态检查通过；本机无独立 `xelatex`，使用 Tectonic 的 XeTeX 引擎补充实际编译。逐份结果见[结构验证记录](reports/figs/src/structure_validation.json)，六份报告均通过：Overfull=0、Missing character=0、Error=0、未定义引用=0、缺失图片=0，页面联系页已目视检查。月一至月五分别为 8、11、16、3、4 页，中期报告 45 页；两份空白骨架也已编译通过。没有新运行 CFD 或训练 XGBoost；已有 UDF 与 PID 结果按仓库复核材料表述，未编造缺失数据。

## 2026-10-23 — 对齐 main 与 GitHub 上传规则

已将 `report/month3-mesh` 的 6 个更新提交与原 `main` 的 2 个更新提交合并，正式内容统一发布到 `main`。对应合并提交：`df56ab3`。

| 更新内容 | 具体位置 |
|---|---|
| GitHub 上传、拉取、合并和同步验证规则；后续更新位置记录要求 | [Agent 约定](AGENTS.md#github-上传与同步)、[修改规范](CONTRIBUTING.md#github-上传与同步)、[项目说明](README.md#github-上传与同步) |
| 月 2 合并四种流道的 16 张云图和 17 条小模型结果，保留双方内容并重新生成 10 页 PDF | [月 2 正文](reports/逻辑月2_指标与形态.tex)「研究进展 → 关键结果 → （一）流道与小模型性能汇总」、[月 2 PDF](reports/逻辑月2_指标与形态.pdf)；云图位于 PDF 第 3 页 |
| 月 1 物性 UDF 学习补充及统一命名 | [月 1 正文](reports/逻辑月1_基础建立.tex)、[月 1 PDF](reports/逻辑月1_基础建立.pdf) |
| 月 3 网格检验、流场对比及 323 万网格参考口径 | [月 3 正文](reports/逻辑月3_形态与物理.tex)、[月 3 PDF](reports/逻辑月3_形态与物理.pdf)、[网格依据资料](reports/figs/src/month3_mesh_data/README.md) |
| 中期报告补充稿、配图与证据资料 | [中期报告正文](reports/中期报告.tex)、[中期报告 PDF](reports/中期报告.pdf)、[复现与资料说明](reports/figs/src/midterm_expanded/README.md) |
| 报告清单及月 2 页数说明 | [报告目录](reports/README.md#一当前文件) |

验证：月 2 合并正文的括号、图片和交叉引用静态检查通过；使用 Tectonic 的 XeTeX 引擎重新编译，Overfull=0、Missing character=0、Error=0、未定义引用=0，共 10 页，云图页面目视检查通过。其他报告沿用原分支已提交文件。本次合并推送后本地 `main` 与 `origin/main` 一致，工作区干净。

## v1.2 — 2026-10-12

**改了什么**：修复参考文献被拆成两页的问题；优化浮动体排版。

**影响范围**：**所有人都要重新拉取 `.cls` 并重新编译**——这份改动会改变分页。

**现象**：阶段二报告里参考文献第 1 条在第 6 页，第 2、3 条被挤到第 8 页，中间隔了一页。

**原因**：图/表浮动体漂移，把参考文献冲开了。同时第 5 页只剩 3 行正文。

**改法**：

1. 参考文献前加 `\FloatBarrier` 排空浮动体，并要求至少 6 行空间（不够就另起一页）；
2. 放宽浮动体参数（`\topfraction` / `\floatpagefraction` / `topnumber` 等），让图尽量留在原文附近；
3. 加防孤行设置（`\widowpenalty` / `\clubpenalty` = 10000）；
4. 阶段二图 2 宽度 0.86 → 0.70（原图接近正方形，太高）。

**踩到的坑（别改回去）**：

- **不要在每个 `\section` 前加 `\FloatBarrier`。** 实测会把正文挤成空白页：
  加了是 8 页且出现一页只有 109 字符，去掉是 7 页且无空白页。
  只在参考文献前用。
- 不要用 `\renewcommand{\section}` 配 `\@ifstar` 的老写法，会和 titlesec 冲突，
  报 `Missing \begin{document}` + `TeX capacity exceeded`。

**验证结果**：

```
examples/阶段一_初步阅读.tex     Overfull=0 Missing=0 Error=0   4 页  无空白页
reports/阶段一_控制算法.tex      Overfull=0 Missing=0 Error=0   6 页  无空白页
reports/阶段二_控制算法.tex      Overfull=0 Missing=0 Error=0   7 页  无空白页
template/阶段一_空白骨架.tex     Overfull=0 Missing=0 Error=0   3 页
template/阶段二_空白骨架.tex     Overfull=0 Missing=0 Error=0   3 页
```

两份报告的参考文献均完整落在同一页（阶段一第 5 页、阶段二第 7 页）。

---

## v1.1 — 2026-10-12

**改了什么**：修复提示盒子的实现，`\note ... \noteend` 改为标准环境写法。

**影响范围**：用了提示盒子的报告需改写法；未用的也要重新拉取 `.cls` 再编译。

**要做什么**：

1. 重新拉取 `template/ydzjreport.cls`
2. 如果你用过提示盒子，把
   `\note` / `\noteend` 改成 `\begin{notebox}` / `\end{notebox}`；
   `\keypoint` / `\keypointend` 改成 `\begin{keybox}` / `\end{keybox}`
3. 重新编译，确认日志三项为 0

**改的原因**：旧实现有两个问题——

- 用 `minipage` 包内容，**不能跨页**，内容里出现段落命令时报
  `begin{minipage} ... ended by \end{...}`；
- 把环境包装成 `\newcommand{\note}{...}` 再配 `\noteend` 收尾时，
  LaTeX 会做环境名匹配检查，报 `\begin{list} ended by \end{note}`。

新实现用「`list` + 上下彩色横线」：**可跨页、可嵌套、无需额外宏包**。

**验证结果**：

```
examples/阶段一_初步阅读.tex     Overfull=0 Missing=0 Error=0   4 页
reports/阶段一_控制算法.tex      Overfull=0 Missing=0 Error=0   5 页
reports/阶段二_控制算法.tex      Overfull=0 Missing=0 Error=0   6 页
template/阶段一_空白骨架.tex     Overfull=0 Missing=0 Error=0   3 页
template/阶段二_空白骨架.tex     Overfull=0 Missing=0 Error=0   3 页
```

**新增内容**：`reports/` 下加入控制算法方向的两份报告示例。

---

## v1.0 — 2026-10-08

**首次发布。**

### 内容

- `template/ydzjreport.cls`：共享文档类
  - 两种阶段共用同一套版式（标题、元信息表、页眉页脚、章节编号、表格、配色）
  - 字体由 ctex 自动检测，Overleaf 与本地均可用
  - 提供 `Y` / `C` 自适应列型，杜绝表格超框
  - 提示盒子：`\begin{notebox} ... \end{notebox}`、`\begin{keybox} ... \end{keybox}`
- `template/阶段一_空白骨架.tex`：阶段一（初步阅读）骨架
- `template/阶段二_空白骨架.tex`：阶段二（研究推进）骨架
- `examples/阶段一_初步阅读.tex`：填好的样例
- `check.py`：编译自检脚本（括号检查 + 编译两遍 + 统计 Overfull/Missing/Error）
- 文档：`README.md`、`CONTRIBUTING.md`、`docs/Overleaf接入.md`、`docs/群通知.md`

### 验证结果

```
阶段一_空白骨架.tex    Overfull=0  Missing=0  Error=0   3 页
阶段二_空白骨架.tex    Overfull=0  Missing=0  Error=0   3 页
阶段一_初步阅读.tex    Overfull=0  Missing=0  Error=0   4 页
```

字体全部正确嵌入（SimSun / SimHei / Microsoft YaHei，`emb=yes`）。

### 已修复的坑（改类文件前必读）

| # | 坑 | 现象 | 处理 |
|---|---|---|---|
| 1 | 类文件顶层用 `\IfFontExistsTF` 做字体 fallback | `Missing \begin{document}` + 大量错乱报错 | 改用 ctex 的 `fontset` 机制 |
| 2 | 导言区调用会输出的命令 | 同上 | 拆成 `\stagesetup`（赋值）与 `\makestagehead`（输出）两步 |
| 3 | `\colorbox{\begin{minipage}...\end{minipage}}` | `Extra }, or forgotten \endgroup` | `\colorbox` 参数提前闭合，改用 minipage + `\hrule` |
| 4 | `\newenvironment` 参数组括号不配对 | `File ended while scanning use of \@newenv` | `check.py` 增加括号检查 |
| 5 | 命令名 `\endnotebox` 与 LaTeX 内部冲突 | `Command already defined` | 内部环境加项目前缀 |
| 6 | `\rowcolor` 未加载对应宏包选项 | `Undefined control sequence \rowcolor` | `\RequirePackage[table]{xcolor}` |
| 7 | 颜色名带 `@` 在正文里使用 | `Undefined color 'ydzj@light'` | 颜色名一律不带 `@` |
| 8 | 中英混排长 token 导致行被撑开 | 两端对齐出现大空隙 | `\XeTeXlinebreaklocale "zh"` + 放宽 `\tolerance` |

---

## 后续版本模板

```markdown
## vX.Y — YYYY-MM-DD

**改了什么**：<一句话>

**影响范围**：<哪些报告需要重新编译>

**要做什么**：<其他人需要执行的操作>

**验证结果**：
```
<check.py 的输出>
```
```

### 版本号规则

| 变化 | 版本号 | 例 |
|---|---|---|
| 配色、间距、字号等外观微调 | `v1.0` → `v1.1` | 表头底色改浅灰 |
| 骨架变化、命令改名、增删章节 | `v1.1` → `v2.0` | 新增"实验方法"章节 |
