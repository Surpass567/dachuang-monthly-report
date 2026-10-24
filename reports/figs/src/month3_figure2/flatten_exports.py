# -*- coding: utf-8 -*-
"""把 draw.io 手工导出的 A--D 透明 PNG 压白，写入报告用图目录。

用法（仓库根目录）：
    python reports/figs/src/month3_figure2/flatten_exports.py

输入：manual_export/A.png ... D.png（draw.io 以 100% 导出、透明背景）
输出：reports/figs/udf_learning_interfaces_a.png ... _d.png

面板在 LaTeX 中按 A/B 上排、C/D 下排组成一幅图，不再合成单张位图。
"""
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = ROOT / "reports" / "figs"

for key in "ABCD":
    src = HERE / "manual_export" / f"{key}.png"
    image = Image.open(src).convert("RGBA")
    canvas = Image.new("RGBA", image.size, (255, 255, 255, 255))
    canvas.alpha_composite(image)
    target = OUT / f"udf_learning_interfaces_{key.lower()}.png"
    canvas.convert("RGB").save(target, optimize=True)
    print(f"{target.relative_to(ROOT)}  {canvas.width}x{canvas.height}")
