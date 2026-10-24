"""把用户提供的两张“小块逻辑”示意图裁去四周空白后放入 reports/figs/。

输入（用户补充的原始文件，归档在 reports/figs/src/month1_block_inputs/，不做修改）：
  02_小块热特征分类_已编辑.png
  03_局部微结构匹配_已编辑.png

输出（报告插图）：
  reports/figs/month1_小块热特征分类.png
  reports/figs/month1_局部微结构匹配.png

只按背景色做外接框裁剪，不重绘、不缩放内容；重新运行时结果一致。
用法：python reports/figs/src/prepare_month1_block_figures.py
"""

from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[3]
FIGS = ROOT / "reports" / "figs"
INPUTS = Path(__file__).resolve().parent / "month1_block_inputs"

JOBS = [
    ("02_小块热特征分类_已编辑.png", "month1_小块热特征分类.png"),
    ("03_局部微结构匹配_已编辑.png", "month1_局部微结构匹配.png"),
]

MARGIN = 40          # 裁剪后保留的边距（像素）
BG_TOLERANCE = 12    # 与背景色的差异阈值，滤掉 JPEG/抗锯齿噪声


def crop_to_content(src: Path, dst: Path) -> None:
    im = Image.open(src).convert("RGB")
    bg = Image.new("RGB", im.size, im.getpixel((2, 2)))
    diff = ImageChops.difference(im, bg).convert("L")
    mask = diff.point(lambda p: 255 if p > BG_TOLERANCE else 0)
    box = mask.getbbox()
    if box is None:
        raise SystemExit(f"未找到内容区域: {src}")
    left = max(box[0] - MARGIN, 0)
    top = max(box[1] - MARGIN, 0)
    right = min(box[2] + MARGIN, im.width)
    bottom = min(box[3] + MARGIN, im.height)
    im.crop((left, top, right, bottom)).save(dst, optimize=True)
    print(f"{src.name}: {im.size} -> {(right - left, bottom - top)} -> {dst.name}")


def main() -> None:
    for source_name, target_name in JOBS:
        source = INPUTS / source_name
        if not source.exists():
            raise SystemExit(f"缺少原始图片: {source}")
        crop_to_content(source, FIGS / target_name)


if __name__ == "__main__":
    main()
