"""Render the synthetic Q2 2027 packet (termination-right case) as a one-page PNG so the upload -> Parse 2.0 -> assess path
can be demonstrated live. Output: samples/cedarbridge-q2-2027.png. Needs Pillow (already installed here)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from data import PACKETS

pk = next(p for p in PACKETS if p["id"] == "pkt-2027q2")
W, H, M = 1240, 1754, 90   # A4 at 150 dpi
im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
def font(sz, bold=False):
    for name in (("arialbd.ttf" if bold else "arial.ttf"), "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"):
        try: return ImageFont.truetype(name, sz)
        except OSError: pass
    return ImageFont.load_default()
def wrap(text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > width: lines.append(cur); cur = w
        else: cur = t
    return lines + [cur]
y = M
d.text((M, y), "CedarBridge Workflow, Inc.", font=font(34, True), fill="black"); y += 46
d.text((M, y), "Quarterly lender reporting packet, Q2 2027 (SYNTHETIC, for demonstration)", font=font(20), fill="#444"); y += 60
sections = {}
for loc, para in pk["text"].items():
    sec = loc.split(",")[0]; sections.setdefault(sec, []).append(para)
for sec, paras in sections.items():
    d.text((M, y), sec, font=font(26, True), fill="black"); y += 44
    for para in paras:
        for line in wrap(para, font(21), W - 2 * M):
            d.text((M, y), line, font=font(21), fill="black"); y += 30
        y += 16
    y += 12
d.text((M, H - 60), "Page 1 of 1", font=font(16), fill="#888")
out = Path(__file__).parent / "samples"; out.mkdir(exist_ok=True)
im.save(out / "cedarbridge-q2-2027.png"); print("wrote", out / "cedarbridge-q2-2027.png")
