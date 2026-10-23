# 月度报告目录

本目录存放中期报告、五个月度报告，以及配图。

---

## 一、当前文件

| 文件 | 说明 |
|---|---|
| `中期报告.tex` / `.pdf` | 中期检查报告（45 页，含月报整合、UDF 复核与配套依据） |
| `逻辑月1_基础建立.tex` / `.pdf` | 逻辑月1 · 基础建立（含 14 张图） |
| `逻辑月2_指标与形态.tex` / `.pdf` | 逻辑月2 · 指标与形态（10 页，含四种流道云图及 17 条小模型补充结果） |
| `逻辑月3_形态与物理.tex` / `.pdf` | 逻辑月3 · 形态与物理 |
| `逻辑月4_连接成网络.tex` / `.pdf` | 逻辑月4 · 连接成网络 |
| `逻辑月5_整板验证.tex` / `.pdf` | 逻辑月5 · 整板验证 |
| `figs/` | 报告图片；代码在 figs/src/ |

---

## 二、命名约定

**强制格式**：`逻辑月N_主题.tex` / `.pdf`，不带版本后缀。

例如 `逻辑月1_基础建立.pdf`。修订更新同名文件，历史版本由 Git 管理；禁止使用 `_v1_1`、`_v2_0` 等后缀。

**逻辑月不对应自然月**，月份边界待定。

---

## 三、编译

在 `reports/` 目录下，每份跑**两遍**：

```powershell
cd reports
xelatex 逻辑月2_指标与形态.tex
xelatex 逻辑月2_指标与形态.tex
```

**需要 `../template/ydzjreport.cls`。**
若报找不到该文件，把 `template/ydzjreport.cls` 复制到本目录。

**Overleaf**：上传 `.tex` 和 `ydzjreport.cls` 到项目根目录，
Menu → Compiler 选 **XeLaTeX**。

---

## 四、配图

**图片统一放 `figs/`，不要和 `.tex` 混放在一起。**

当前 `figs/` 内容：

| 文件 | 用途 |
|---|---|
| `01_temperature_midplane.png` ~ `12_copper_base_temperature.png` | 逻辑月1 的 12 张流场/温度场图 |
| `13_控制框架框图.png` | 逻辑月1 §2.3 的控制框架框图 |
| `udf_learning_interfaces.png` | 逻辑月1 的水物性 UDF 接口与实现流程 |
| `month2_other_models.png` / `month2_naca_models.png` | 逻辑月2 的小模型界面网格与加热面温度 |

**代码、数据、脚本产出的备用图都在 `figs/src/`，不要和报告引用的图混放：**

| `figs/src/` 下的文件 | 说明 |
|---|---|
| `PID仿真.py`、`生成配图.py` | 控制配图的生成脚本 |
| `pid_sim.npz` | 中间仿真数据 |
| `fig_block.png` 等 4 张 | 控制算法旧图（备用，当前无报告引用） |

目录规则：**`figs/` 根只放报告里真正引用的图**，代码、数据、备用图与复现说明统一进 `src/`。

**引用写法**：

```latex
\includegraphics[width=\linewidth]{figs/01_temperature_midplane.png}
```

**要点**：

- 路径带 `figs/` 前缀
- 图片找不到时 **LaTeX 不中断编译**，只会留空——**要查日志，别只看"PDF 生成了"**
- 路径不能用 Windows 反斜杠（`\` 是命令起始符）
- 图题里不要直接写带下划线的文件名（`_` 要转义为 `\_`）

### 中期报告配套文件

中期报告使用的图片已补齐，统一放在 `figs/`，文件名以 `midterm_` 开头。
构建脚本、月报快照、来源清单和校核依据位于
[`figs/src/midterm_expanded/`](figs/src/midterm_expanded/README.md)。

详见 [`figs/src/README.md`](figs/src/README.md)。

---

## 五、自检

```powershell
cd reports
python ..\check.py
```

会检查括号、交叉引用、**图片文件是否存在**，并编译验证。
`Overfull` / `Missing character` / `Error` 三项必须都是 0。

---

## 六、留空标记

报告里不明确、缺数据之处用标记标出：

| 标记 | 含义 |
|---|---|
| `【待确认N】` | 需组长明确的信息 |
| `【缺数据：……】` | 手上没有的数据 |
| `【待补：……】` | 工作尚未开展 |
