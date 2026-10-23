# 大创仓库 Agent 工作约定

适用于整个仓库。后续修改大创报告、配图和代码时，必须遵守以下核心要求。

## 大创修改核心要求

1. 月度报告统一命名为 `逻辑月N_主题.pdf`，对应源文件为同名 `.tex`。例如 `逻辑月1_基础建立.pdf` 和 `逻辑月1_基础建立.tex`。禁止添加 `_v1_1`、`_v2_0` 等版本后缀；修订更新同名文件，版本历史由 Git 管理。
2. 所有报告配图的生成代码、分析代码和辅助脚本统一放在 `reports/figs/src/`；相关输入数据、中间数据及复现说明也放在该目录。
3. `reports/figs/` 根目录只放报告使用的图片文件及 `src/` 子目录，不放代码、数据、说明文档或临时文件。备用图与中间图放在 `src/`，正式引用时再放入 `figs/`。
4. 重命名或移动文件时，同步更新报告引用、文档链接和脚本路径；提交前检查文件命名与目录归属，并按现有规范完成报告编译自检。

其余协作与排版要求见 `CONTRIBUTING.md`。

## GitHub 上传与同步

`main` 是唯一正式发布分支（不是文件夹，不另建 main 目录）。所有报告、配图、代码和文档更新均须最终合并到 `main` 并推送 `origin/main`。

维护者默认在 `main` 更新。上传前先 `git fetch origin`，合并远端 `main` 和本地更新，保留双方有效内容；冲突中的 PDF 根据合并后的 `.tex` 重新编译。禁止强制推送覆盖远端。临时分支须合并到 `main` 才算完成正式上传；PR 的目标分支统一为 `main`。

```bash
git switch main
git fetch origin
git merge origin/main
# 如有临时分支的更新，再 git merge 对应分支
# 修改报告后，按原规范运行 python check.py 对应报告.tex
# 核对并 git add 本次更新的源文件、同名 PDF、配图及数据
git diff --cached --stat
git commit -m "更新报告与配套资料"
git push origin main
git fetch origin
git rev-list --left-right --count HEAD...origin/main
git status --short
```

最后两项应分别输出 `0 0` 和空。网络失败须明确说明尚未同步。GitHub 网页上传也必须选择 `main`，并遵守相同目录与命名规则。切换分支前须妥善保存未提交改动。
