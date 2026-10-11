# 大创月度总结 · LaTeX 模板

三个人（不同方向、不同 AI 工具、不同编辑器）写出来的月度总结，**排版完全一致**。

编译环境任选：**Overleaf** 或 **本地 XeLaTeX**，同一份文件两边都能出同样的结果。

---

## 这是什么

一份共享的 LaTeX 文档类 `ydzjreport.cls`，把版式（字体、标题、章节编号、表格样式、页眉页脚、配色）全部固定下来。

你只需要：

1. 下载两个文件
2. 改开头六项信息
3. 往章节里填内容

**格式不用你操心**——章节编号、表格换行、字体选择都由类文件处理。

---

## 快速开始

### 第 1 步：拿文件

**会 Git**：

```bash
git clone https://github.com/Surpass567/dachuang-monthly-report.git
```

**不会 Git**：点本页绿色 `Code` 按钮 → `Download ZIP` → 解压。效果一样。

### 第 2 步：认准两个文件

```
template/ydzjreport.cls            ← 版式定义，不要改
template/阶段一_空白骨架.tex        ← 阶段一填这个
template/阶段二_空白骨架.tex        ← 阶段二填这个
```

**只需要这两个文件**（`.cls` + 你那个阶段的 `.tex`），**必须放在同一个目录**。

### 第 3 步：编译

**Overleaf**（推荐，零配置）：

1. 新建项目 → Blank Project
2. 上传上面两个文件
3. **Menu → Compiler → 选 `XeLaTeX`**
4. Recompile

> ⚠️ **必须改 Compiler**。Overleaf 默认是 pdfLaTeX，中文会编译失败。

**本地**（TeX Live / MiKTeX）：

```bash
xelatex 你的报告.tex
xelatex 你的报告.tex     # 跑两遍，交叉引用才正确
```

---

## 两种阶段

| | 阶段一 · 初步阅读 | 阶段二 · 研究推进 |
|---|---|---|
| **文档类选项** | `\documentclass[stage1]{ydzjreport}` | `\documentclass[stage2]{ydzjreport}` |
| **信息命令** | `\stageonesetup{...}` + `\makestageonehead` | `\stagetwosetup{...}` + `\makestagetwohead` |
| **主线** | 学习过程 | 研究推进 |
| **必须有** | 「导出与复现」环节（环境 + 步骤 + 结果） | 「关键结果」量化数据 |
| **不能为空** | 「尚存的疑问」≥ 2 条 | 「与预期的差异」「尚不能确定的」 |
| **常见病** | 只罗列文献不消化 | 只报喜不报忧 |
| **篇幅** | 3–5 页 | 4–6 页 |

**阶段一的核心**：只读不做不算完成，必须有复现。
**阶段二的核心**：全都符合预期 = 没有深入思考，必须写差异。

---

## 填哪里

只有两处：

### ① 导言区：六项信息（顺序不要变）

```latex
\documentclass[stage1]{ydzjreport}

% ============ 只改这里 ============
\stageonesetup
  {阶段一 · 初步阅读}%         报告阶段
  {张三}%                      姓名
  {导流柱结构设计}%             方向
  {2026-10-01 至 2026-10-31}%  报告周期
  {微通道；翼型导流柱；拓扑优化}% 关键词
  {一句话说清本月收获。}%        一句话摘要
% =================================

\begin{document}
\makestageonehead              % 产生标题与元信息表
```

> **为什么分两步？** `\stageonesetup` 只赋值，可以放导言区；`\makestageonehead` 会产生输出（表格、颜色），必须在 `\begin{document}` 之后。合成一步会报 `Missing \begin{document}`。

### ② 正文：往章节里填

章节骨架**已经写好，不要增删**，只填空白处。

---

## 硬性格式要求

1. **不要手写章节编号**。写 `\section{阅读范围}`，不要写 `\section{一、阅读范围}`——会自动编号
2. **数字与单位之间加空格**：`2.8 mm`，不是 `2.8mm`
3. **不要用 emoji 和圈号**：`✅ ❌ ⚠️ ★ ① ② ③` —— 中文字体没有这些字形，会渲染成**空白**
   改用：`已完成` / `未完成` / `注意` / `(1)` `(2)`
4. **表格列数 ≤ 6**，用 `tabularx` + `Y` 列
5. **图表必须被正文引用**：`见表~\ref{tab:xxx}`、`如图~\ref{fig:xxx}`
6. **参考文献**用 `thebibliography`，按引用顺序编号
7. **文件命名**：`YYYY-MM_阶段N_姓名_方向.tex`，例 `2026-10_阶段一_张三_导流柱结构设计.tex`

---

## 提交前自检

```bash
python check.py
```

它会：
- 检查括号平衡（LaTeX 最常见的低级错误）
- 实际编译两遍，统计 `Overfull` / `Missing character` / `Error`

**三项必须都是 0。**

手动核对：

```
[ ] 六项信息齐全，顺序未变
[ ] 章节骨架与模板一致，无手写编号
[ ] 数字与单位之间有空格
[ ] 没有 emoji / 圈号
[ ] 表格 ≤ 6 列，未超出页面
[ ] 图表都被正文引用
[ ] 阶段一：有复现的环境 + 步骤 + 结果
[ ] 阶段二：「与预期的差异」和「尚不能确定的」非空
[ ] 「下月计划」是表格且带时间
```

---

## 类文件提供什么

| 功能 | 用法 |
|---|---|
| 元信息表 | `\stageonesetup{...}` / `\stagetwosetup{...}` |
| 防超框表格列 | `Y`（自适应页宽自动换行）、`C`（居中自适应） |
| 表头行 | `\rowcolor{ydzjlight} 列1 & 列2 \\` |
| 提示盒子 | `\note ... \noteend`（黄线）、`\keypoint ... \keypointend`（蓝线） |
| 章节自动编号 | `1` / `1.1` / `1.1.1` |
| 图表标题 | `\caption{...}`，自动带编号 |
| 页眉 | 左：报告名；右：姓名 |
| 页脚 | 页码 |

### 配色（想改在 `ydzjreport.cls` 里改）

| 颜色名 | 色值 | 用途 |
|---|---|---|
| `ydzjblue` | `#0B4C8C` | 主标题、一级章节 |
| `ydzjblueii` | `#1868A8` | 二级章节、表头线 |
| `ydzjlight` | `#F2F7FB` | 表头底色 |
| `ydzjwarnline` | `#E6A23C` | 注意事项边框 |

---

## 为什么在 Overleaf 和本地都能编译

中英混排的 LaTeX 最容易在**字体**上翻车：Windows 有 SimSun，Overleaf 上只有 Noto/Fandol，写死任何一个另一边就报 `font not found`。

**本方案的处理**：字体交给 **ctex 的自动检测**——它本来就是为跨平台中文排版设计的。

| 平台 | ctex 自动选择 |
|---|---|
| Windows | SimSun / SimHei |
| Overleaf / Linux | Fandol 或 Noto CJK |
| macOS | Songti SC / Heiti SC |
| 都没有 | 回退 ctex 默认，**不报错** |

**代价**：本地和 Overleaf 的字形可能略有差异。

**想完全一致**，三人统一加 `fontset` 选项：

```latex
\documentclass[stage1,fontset=fandol]{ydzjreport}
```

`fandol` 在 Overleaf 上一定有，推荐用它保证字形一模一样。

### 依赖

只加载标准宏包，Overleaf 全部自带：

```
geometry  xcolor(table)  booktabs  tabularx  array  ragged2e
multirow  enumitem  titlesec  fancyhdr  graphicx  float
caption   amsmath   amssymb   ulem      hyperref
```

本地最少需要：TeX Live 完整版，或 MiKTeX + `ctex`。

---

## 目录结构

```
.
├── README.md                    ← 本文件
├── CONTRIBUTING.md              ← 修改规范（改模板、提报告都要看）
├── CHANGELOG.md                 ← 更新记录
├── check.py                     ← 编译自检脚本
├── .gitignore
├── template/
│   ├── ydzjreport.cls           ★ 共享文档类（唯一源，不要各自改）
│   ├── 阶段一_空白骨架.tex        ★ 阶段一填这个
│   └── 阶段二_空白骨架.tex        ★ 阶段二填这个
├── examples/
│   ├── 阶段一_初步阅读.tex        填好的样例（照它的详略写）
│   └── 阶段一_初步阅读_编译结果.pdf
├── reports/                     ← 各人的报告放这里
│   └── README.md                （命名规则与编译说明）
└── docs/
    ├── 群通知.md                 可直接发群里的文案
    └── Overleaf接入.md           Overleaf 与 GitHub 集成的操作步骤
```

---

## 遇到问题

| 现象 | 原因 | 处理 |
|---|---|---|
| `font not found` | 用了不存在的字体 | 删掉 `fontset` 选项，或改成 `fontset=fandol` |
| 中文不显示 / 报错 | Compiler 是 pdfLaTeX | Menu → Compiler → 改 XeLaTeX |
| `Missing \begin{document}` | 在导言区调用了会输出的命令 | 检查是否把 `\makestageonehead` 放到了 `\begin{document}` 之前 |
| 某些字符是空白 | 用了 emoji / 圈号 | 换成中文描述 |
| 表格右侧超出页面 | 用了 `l` 列 | 改 `Y` 列 |
| 章节编号重复 `2 一、` | 手写了编号 | 去掉手写编号 |
| `File ended while scanning` | 括号不配对 | 跑 `python check.py` |

**解决不了就把编译日志贴群里。** 日志在 `你的报告.log`，或者 Overleaf 的 Raw Log。

---

## 改版式怎么办

`template/ydzjreport.cls` 是**唯一源**，所有人引用它、**不改它**。

要改版式（配色、字号、加上某个命令）：

1. 看 [CONTRIBUTING.md](CONTRIBUTING.md)
2. 或直接在群里说，由维护者统一改完推上去

**只要 `.cls` 是同一个版本，三人排版就一致。**
