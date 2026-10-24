# 本机 VS Code 全局 LaTeX 环境修复

2026-10-24：原有 Tectonic 已安装，但 VS Code 的两次失败日志均为 `File ydzjreport.cls not found`。原脚本没有显式加入项目共享模板目录；系统也没有独立的 `xelatex`、`latexmk` 或 Perl。此次继续使用已安装并有离线缓存的 Tectonic，不将其伪装为 XeLaTeX 命令。

## 安装与使用

在仓库根目录运行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File reports/figs/src/latex_environment/install.ps1
```

安装器先备份，再更新 `%LOCALAPPDATA%/LaTeXPortable/compile.ps1` 和 VS Code 默认用户设置、现有配置档；LaTeX 设置加入 `workbench.settings.applyToAllProfiles`，供之后的配置档共享。其他编辑器设置保留。本次安装前的原始备份位于 `%LOCALAPPDATA%/LaTeXPortable/backups/20261024-110931/`。

已移除独立流程的 `finlay-ab.vscode-latex-runner`，保留 `james-yu.latex-workshop`。如在其他电脑复现，需先安装 Tectonic、资源缓存与 LaTeX Workshop；安装器不负责下载发行版，也不自动移除扩展。已有设置文件需为合法 JSON。

VS Code 重载窗口后，打开 `.tex`，保存自动编译，或按 `Ctrl+Alt+B`。默认配方为 `Global Tectonic`，PDF、日志及 SyncTeX 输出到源文件旁的 `build-latex/`，不会覆盖正式交付 PDF。通过 LaTeX Workshop 的 PDF 预览命令打开生成结果。

全局脚本以源文件目录为工作目录，显式添加祖先目录的 `template/`、`templates/`，到 Git 根目录后添加 `reports/`，并加入源文件目录；使用 Tectonic 的 `-Z search-path` 查找共享类文件及图片，不复制模板到每份报告旁。离线验证可加 `-Offline`，平时允许按需下载未缓存宏包。

```powershell
& "$env:LOCALAPPDATA/LaTeXPortable/compile.ps1" -Source reports/逻辑月1_基础建立.tex -Offline
```

VS Code 的工作区、语言或远程设置仍可能覆盖用户设置；此次仓库没有 `.vscode/settings.json` 覆盖项，未发现其他现有用户配置档。未来特意设置项目独立配方时，需删除该覆盖项以恢复全局配方。详见 [VS Code 设置优先级](https://code.visualstudio.com/docs/configure/settings)和 [LaTeX Workshop 编译配方](https://github.com/James-Yu/LaTeX-Workshop/wiki/Compile)。

## 验证

[validation.json](validation.json)记录根目录月一、`reports/` 月一及中期报告三次离线编译。三次均退出码 0，生成同名 PDF 与 SyncTeX；日志中 Overfull、Missing character、TeX Error 和未定义引用均为 0。仓库归档脚本与安装后的全局脚本 SHA256 一致。这里只验证环境和编译日志，未修改报告正文及正式 PDF。

`python check.py` 仍依赖独立 XeLaTeX，本机没有该命令，因此该旧自检只执行静态检查；环境实际编译验证使用上述全局脚本。Tectonic 不保证支持所有需要完整 TeX Live、外部程序或 shell-escape 的项目。
