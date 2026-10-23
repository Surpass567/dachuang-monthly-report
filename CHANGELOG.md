# 更新记录

本文件统一记录更新内容、具体位置和验证结果；每次修改与对应文件一起提交到 `main`。更早的过程文档保存在 `archive/full-20261015` 分支。

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
