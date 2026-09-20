"""Read embedded PDF text directly; use NVIDIA Nemotron Parse 2.0 for scanned pages/images.
Page text or OCR elements -> packet text dict {locator: paragraph}.
Request shape and extra params follow NVIDIA's vllm_example.py for this model; output tags follow its postprocessing.py."""
import base64, io, json, os, re, urllib.request
from concurrent.futures import ThreadPoolExecutor

PARSE_MODEL = os.environ.get("NEMOTRON_PARSE_MODEL", "nvidia/nemotron-parse-2.0")
URL = "https://integrate.api.nvidia.com/v1/chat/completions"
PROMPT = "</s><s><predict_bbox><predict_classes><output_markdown><predict_no_text_in_pic>"
TAG = re.compile(r'<x_(\d+(?:\.\d+)?)><y_(\d+(?:\.\d+)?)>(.*?)<x_(\d+(?:\.\d+)?)><y_(\d+(?:\.\d+)?)><class_([^>]+)>', re.S)
SKIP = {"Page-header", "Page-footer", "Picture", "Page-number"}
MAX_W, MAX_H = 1664, 2048   # model card's recommended maximum
MAX_PDF_PAGES = 300
MAX_OCR_PAGES = 20

def _fit(img_bytes):
    """Downscale to the model's recommended max if PIL is available; otherwise send as-is."""
    try:
        from PIL import Image
    except ImportError:
        return img_bytes, "image/png"
    im = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    if im.width > MAX_W or im.height > MAX_H:
        im.thumbnail((MAX_W, MAX_H))
    buf = io.BytesIO(); im.save(buf, "PNG"); return buf.getvalue(), "image/png"

def parse_image(img_bytes):
    """One page image -> list of {class, bbox, text} in reading order."""
    key = os.environ.get("NVIDIA_API_KEY")
    if not key:
        raise RuntimeError("NVIDIA_API_KEY not set")
    data, mime = _fit(img_bytes)
    body = {"model": PARSE_MODEL, "max_tokens": 4000, "temperature": 0, "top_k": 1, "repetition_penalty": 1.1,
            "skip_special_tokens": False,   # bbox/class tags are special tokens; without this the output is empty
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": PROMPT},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{base64.b64encode(data).decode()}"}}]}]}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        content = json.load(r)["choices"][0]["message"]["content"] or ""
    return [{"class": m.group(6), "bbox": tuple(float(v) for v in (m.group(1), m.group(2), m.group(4), m.group(5))),
             "text": m.group(3).replace("<tbc>", "").strip()} for m in TAG.finditer(content)]

def elements_to_packet_text(pages):
    """[[elements per page]] -> {locator: paragraph}. Locator = current section header + running paragraph number,
    so a well-structured packet yields locators like 'Customer contracts, para 2', matching the demo data."""
    text, section, n = {}, "Document", 0
    for pno, els in enumerate(pages, 1):
        for e in els:
            if e["class"] in SKIP or not e["text"]:
                continue
            if e["class"] in ("Section-header", "Title"):
                section, n = re.sub(r"^#+\s*|\*+", "", e["text"]).strip(), 0
                continue
            n += 1
            label = "table" if e["class"] == "Table" else "para"
            text[f"{section}, {label} {n} (p{pno})"] = e["text"]
    return text

def parse_upload(filename, file_bytes):
    if filename.lower().endswith('.pdf'):
        import pymupdf
        with pymupdf.open(stream=file_bytes, filetype='pdf') as doc:
            if doc.page_count > MAX_PDF_PAGES:
                raise ValueError(f'PDF uploads support at most {MAX_PDF_PAGES} pages per file.')
            native = []
            for page in doc:
                text = page.get_text('text', sort=True).strip()
                # A footer alone is not a text layer; retain usable text layers on searchable scans.
                scanned = len(text) < 200 and any(
                    pymupdf.Rect(info['bbox']).get_area() >= page.rect.get_area() / 2
                    for info in page.get_image_info())
                native.append(text if text and not scanned else None)
            if native.count(None) > MAX_OCR_PAGES:
                raise ValueError(f'PDFs support at most {MAX_OCR_PAGES} pages requiring OCR. '
                                 'Upload a searchable PDF with an embedded text layer for longer documents.')
            # Render only the scanned pages, after checking the OCR budget; pymupdf is not thread-safe, so only the hosted calls run in parallel.
            scans = [doc[number].get_pixmap(dpi=150).tobytes('png') for number, text in enumerate(native) if text is None]
            with ThreadPoolExecutor(4) as pool:
                ocr = iter(list(pool.map(parse_image, scans)))
            pages = [[{'class': 'Text', 'text': text}] if text is not None else next(ocr) for text in native]
    else:
        pages = [parse_image(file_bytes)]
    return {"pages": len(pages), "elements": sum(len(p) for p in pages), "text": elements_to_packet_text(pages)}
