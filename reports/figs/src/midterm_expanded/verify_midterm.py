from pathlib import Path
import json
import re

import fitz

SRC = Path(__file__).resolve().parent
REPORT = SRC.parents[2]
tex = REPORT / '中期报告.tex'
log = tex.with_suffix('.log')
pdf = fitz.open(tex.with_suffix('.pdf'))
log_text = log.read_text(encoding="utf-8", errors="replace")
summary = json.loads((SRC / "integration_summary.json").read_text(encoding="utf-8"))
checks = {
    "pages": len(pdf),
    "overfull": log_text.count("Overfull"),
    "missing_glyphs": log_text.count("Missing character"),
    "tex_errors": len(re.findall(r"^! ", log_text, re.M)),
    "undefined_references": len(re.findall(r"undefined", log_text)),
    "missing_images": [name for name in summary["referenced_images"] if not (REPORT / name).exists()],
}
(SRC / "validation.json").write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding="utf-8")
assert checks["pages"] > 0
assert all(checks[name] == 0 for name in ("overfull", "missing_glyphs", "tex_errors", "undefined_references"))
assert not checks["missing_images"], checks["missing_images"]
print(json.dumps(checks, ensure_ascii=False))
