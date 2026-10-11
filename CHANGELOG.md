# 更新记录

## v1.0 — 2026-10-08

**首次发布。**

### 内容

- `template/ydzjreport.cls`：共享文档类
  - 两种阶段共用同一套版式（标题、元信息表、页眉页脚、章节编号、表格、配色）
  - 字体由 ctex 自动检测，Overleaf 与本地均可用
  - 提供 `Y` / `C` 自适应列型，杜绝表格超框
  - 提示盒子：`\note ... \noteend`、`\keypoint ... \keypointend`
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
