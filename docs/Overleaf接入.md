# Overleaf 接入指南

三种接入方式，按你会不会 Git 选。

---

## 方式一：GitHub 直接导入（推荐，会用 Git 的话）

**一次设置，之后改模板一键同步。**

### 第 1 步：在 Overleaf 里新建项目

1. 登录 Overleaf → `New Project`
2. 选 **`Import from GitHub`**
3. 第一次用会要求授权：点 `Link to GitHub`，登录 GitHub 账号，授权 Overleaf 访问
4. 从列表里选 `dachuang-monthly-report`
5. 等项目导入完成

> ⚠️ **只在第一次需要授权。** 之后新建项目不会再问。

### 第 2 步：改 Compiler（关键）

1. 点左上角 **`Menu`**
2. 找到 **`Compiler`**，从 `pdfLaTeX` 改成 **`XeLaTeX`**
3. 返回编辑区，点 **`Recompile`**

**不改这一步中文会编译失败。** 这是最常见的坑。

### 第 3 步：开始写

- 左边文件树里找到 `template/阶段一_空白骨架.tex`
- 复制一份到 `reports/`，改名为 `2026-10_阶段一_张三_方向.tex`
- 编辑，Recompile

### 之后怎么拉最新版

你在网页上编辑的内容**不会自动同步回 GitHub**。两种用法选一个：

**用法 A：只在 Overleaf 写，定期下载源文件交上来**

- `Menu → Download → Source` 下载 zip
- 从 zip 里取出你的 `.tex`，交到仓库 `reports/` 下

**用法 B：只在本地写，Overleaf 只用来编译**

- 本地用 Git 管理，写完推到 GitHub
- Overleaf 里 `Menu → GitHub → Pull` 拉最新

**别两边同时改**，会冲突。

---

## 方式二：手动上传（不会 Git 就用这个）

**只编译一次，不需要同步。**

### 第 1 步：下载两个文件

到 GitHub 仓库页面，分别点开这两个文件，点右上角 `Download raw file`（或 `Raw` 按钮后另存）：

```
template/ydzjreport.cls
template/阶段一_空白骨架.tex        （或 阶段二_空白骨架.tex）
```

**或者**：仓库首页绿色 `Code` → `Download ZIP`，解压后从 `template/` 里取。

### 第 2 步：新建 Overleaf 项目

1. `New Project` → **`Blank Project`**
2. 把上面两个文件拖进文件区
3. **Menu → Compiler → XeLaTeX**
4. Recompile

### 第 3 步：开始写

直接编辑那个 `.tex`。

**注意**：这种方式每次都要手动下载新模板。**如果 `.cls` 更新了，要重新下载一次并覆盖。**

---

## 方式三：本地编译，Overleaf 只作备用

适合本地装了 TeX Live / MiKTeX 的人。

```bash
# 1. 拉仓库
git clone https://github.com/<用户名>/dachuang-monthly-report.git
cd dachuang-monthly-report

# 2. 复制模板到 reports/
cp template/阶段一_空白骨架.tex reports/2026-10_阶段一_张三_方向.tex

# 3. 编辑
# ...

# 4. 编译（两遍）
cd reports
xelatex 2026-10_阶段一_张三_方向.tex
xelatex 2026-10_阶段一_张三_方向.tex

# 5. 自检
cd ..
python check.py reports/2026-10_阶段一_张三_方向.tex

# 6. 提交
git add reports/2026-10_阶段一_张三_方向.tex
git commit -m "提交 2026-10 阶段一报告（张三）"
git push
```

**本地编译有个好处**：`check.py` 能直接跑，Overleaf 上跑不了。

---

## 常见问题

### Q1：`Import from GitHub` 是灰的 / 点了没反应

**原因**：Overleaf 的 GitHub 集成需要账号权限，免费版也支持，但有时被浏览器扩展拦截。

**处理**：
1. 换浏览器（Chrome / Edge 无痕模式）试
2. 检查 Overleaf 账号是否已绑定邮箱（未验证邮箱时部分功能受限）
3. **实在不行就用方式二（手动上传）**，完全够用

---

### Q2：编译报 `font not found` 或中文不显示

**原因**：Compiler 还是 pdfLaTeX。

**处理**：`Menu → Compiler → XeLaTeX`，然后 **Recompile**（改完必须重新编译一次才会生效）。

---

### Q3：编译报 `File 'ydzjreport.cls' not found`

**原因**：`.cls` 和 `.tex` **不在同一目录**。

**处理**：
- Overleaf 里两个文件必须在**项目根目录**（或同层）
- 如果 `.cls` 在 `template/`，你的 `.tex` 也在 `template/`，就没事
- 如果你的 `.tex` 在 `reports/`，而 `.cls` 在 `template/`，**会找不到**

**解法**：把 `.cls` 复制一份到 `reports/`，或者干脆把你的 `.tex` 也放在 `template/` 下写，写完再移。

---

### Q4：中文字体本地和 Overleaf 不一样，排版有细微差异

**原因**：ctex 按平台自动选字体（Windows→SimSun，Overleaf→Fandol）。

**处理**：三人统一加 `fontset` 选项：

```latex
\documentclass[stage1,fontset=fandol]{ydzjreport}
```

`fandol` 在 Overleaf 上一定有，本地 TeX Live 也带。

---

### Q5：编译超时 / 超过免费版时长限制

**原因**：免费版有编译时长限制。

**处理**：
- 本模板很轻（3–5 页），正常不会超时
- 如果超时，检查是不是误传了大图片。图片压到 1 MB 以内

---

### Q6：Overleaf 上怎么跑 `check.py`

**跑不了。** Overleaf 不执行 Python 脚本。

**替代**：看 Overleaf 的编译日志（点 `Recompile` 旁边的 `Logs` → `Raw Log`），搜索：

```
Overfull
Missing character
```

**有任何一条就要修。** 修法见 [CONTRIBUTING.md](../CONTRIBUTING.md) 第八节。

---

### Q7：我想在 Overleaf 里直接改 `.cls`

**别改。** `.cls` 是三人共用的唯一源，各自改会导致格式分叉。

要改版式 → 看 [CONTRIBUTING.md](../CONTRIBUTING.md) 第三节，先提 Issue。

---

### Q8：`.tex` 里的中文注释在 Overleaf 里显示乱码

**原因**：文件编码不是 UTF-8。

**处理**：本地保存时选 `UTF-8`（不要选 GBK / ANSI）。Overleaf 一律按 UTF-8 读。

---

## 一句话总结

```
会用 Git → GitHub 导入 + 本地 git 管理 + Overleaf 只编译
不会 Git → 下载 ZIP + 手动传 Overleaf + 交 .tex 源文件
```

**不管走哪条路，Compiler 必须选 XeLaTeX，这一条不能忘。**
