# 逻辑月3 图2：UDF 接口与实现流程组图

本目录保存“水物性 UDF 的接口与实现流程”组图的源文件。组图由四个面板组成，不再合成一张位图：

- A 常用接口及作用
- B 密度接口示例
- C 编译与挂接流程
- D 三种水物性实现方式

## 报告中的排版

月三与中期报告均在同一个 `figure` 环境内用四个 `subfigure` 排列：

- 上排 A、B，下排 C、D；宽度各 `0.49\linewidth`。
- 图片文件位于 `reports/figs/`：`udf_learning_interfaces_a.png` 至 `_d.png`。
- 月三标签为 `fig:udf-interfaces`，中期报告标签为 `fig:udf-interface`。

## 源文件与导出

| 路径 | 说明 |
|---|---|
| `drawio/A.drawio` ~ `D.drawio` | 四个面板的 draw.io 源文件，可由 draw.io 直接打开编辑 |
| `manual_export/A.png` ~ `D.png` | 从 draw.io 以 100% 比例、透明背景手工导出的原图 |
| `flatten_exports.py` | 把透明原图压到白底，生成 `reports/figs/` 下的报告用图 |
| `archive/` | 旧的单张合成图、旧 drawio 草稿与旧验证记录，仅作历史保留 |

修改面板后重新导出的步骤：

1. 在 draw.io 中打开 `drawio/<面板>.drawio`，修改后导出 PNG（100%，透明背景），覆盖 `manual_export/<面板>.png`。
2. 在仓库根目录运行：

   ```bash
   python reports/figs/src/month3_figure2/flatten_exports.py
   ```

3. 重新编译 `reports/逻辑月3_形态与物理.tex` 与 `reports/中期报告.tex`。

当前四张报告用图的尺寸（压白后）为 A 642×235、B 642×251、C 640×485、D 641×235 像素，均按原始 640 px 设计宽度导出；在 `0.49\linewidth` 下四图像素比例一致。
