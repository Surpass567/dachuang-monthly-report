# 复合微通道分区冷却 · 月度报告

五个逻辑月的月度报告，按组长提纲的关键词组织。

## 报告清单

| 逻辑月 | 报告 | 页数 | 组长关键词 |
|---|---|---|---|
| 1 | [基础建立](reports/逻辑月1_基础建立.pdf) | 4 | 复现 2~3 学长（结构／物理性质 UDF）· 小块 到 具体 · 算法 提要 |
| 2 | [指标与形态](reports/逻辑月2_指标与形态.pdf) | 6 | 指标 · 小块（形态／仿生／扰流性 到 翼型）· 控制 |
| 3 | [形态与物理](reports/逻辑月3_形态与物理.pdf) | 4 | 形态　物理 |
| 4 | [连接成网络](reports/逻辑月4_连接成网络.pdf) | 4 | 网络 · 优化 · 连接 · UDF修正 |
| 5 | [整板验证](reports/逻辑月5_整板验证.pdf) | 4 | 整板验证（待做） |

每份报告同时提供 `.tex` 源文件，位于同名路径。

## 报告的写法

- **有素材的写实**——数据来自三人的实际仿真与文献工作
- **无素材的留空**——用标记标出，不编造：

| 标记 | 含义 |
|---|---|
| `【待确认N】` | 需组长明确的信息 |
| `【缺数据：……】` | 手上没有的数据 |
| `【待补：……】` | 工作尚未开展 |

## 编译

需要 XeLaTeX（中文）。每份报告跑两遍：

```bash
xelatex 逻辑月1_基础建立.tex
xelatex 逻辑月1_基础建立.tex
```

**Overleaf**：上传 `.tex` 与 `template/ydzjreport.cls` 到同一目录，
Menu 到 Compiler 选 **XeLaTeX**（默认是 pdfLaTeX，不改会报错）。

字体由 ctex 自动检测（Windows 用 SimSun，Overleaf 用 Fandol），
三人的 PDF 字形可能略有差异；若要求完全一致，在 `\documentclass` 加 `fontset=fandol`。

## 自检

```bash
python check.py
```

会检查括号平衡、交叉引用、图片文件，并编译验证。
**`Overfull` / `Missing character` / `Error` 三项必须都是 0。**

## 目录结构

```
.
├── README.md
├── CONTRIBUTING.md          格式规范（单位、符号、表格）
├── CHANGELOG.md             版本记录
├── check.py                 编译自检
├── reports/
│   ├── 逻辑月1_基础建立.tex / .pdf
│   ├── ...
│   ├── 逻辑月5_整板验证.tex / .pdf
│   ├── figs/                报告配图与生成脚本
│   └── README.md
└── template/
    ├── ydzjreport.cls       报告文档类（编译必需）
    ├── 阶段一_空白骨架.tex
    └── 阶段二_空白骨架.tex
```

## 历史版本

旧的两阶段月度报告、研究主线整合方案、缺口说明、修正记录等过程文档，
已归档到分支 **`archive/full-20261015`**（或同名 tag）：

```bash
git checkout archive/full-20261015
```
