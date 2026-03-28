"""Download arXiv PDFs and render their first page as thumbnails."""

import io
import os
import time

import fitz  # pymupdf
import requests

PAPERS = [
    ("2602.15927", "thumb_visual_memory_injection.jpg"),
    ("2507.00670", "thumb_mind_the_detail.jpg"),
    ("2506.03355", "thumb_robustness_both_domains.jpg"),
    ("2506.03096", "thumb_fuselip.jpg"),
    ("2502.11725", "thumb_robust_clip_perceptual.jpg"),
    ("2411.14834", "thumb_ensemble_everywhere.jpg"),
    ("2402.12336", "thumb_robust_clip.jpg"),
    ("2308.10741", "thumb_adversarial_robustness_mm.jpg"),
]

OUT_DIR = "assets/thumbnails"
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (personal-website thumbnail generator)"}


def fetch_first_page_thumb(arxiv_id: str, out_path: str, width: int = 400) -> None:
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    print(f"  Downloading {url} …")
    r = requests.get(url, headers=HEADERS, timeout=60, stream=True)
    r.raise_for_status()
    pdf_bytes = r.content

    doc = fitz.open(stream=io.BytesIO(pdf_bytes), filetype="pdf")
    page = doc[0]
    # scale so the page width equals `width` pixels
    zoom = width / page.rect.width
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    pix.save(out_path)
    print(f"  Saved → {out_path}")


for arxiv_id, filename in PAPERS:
    out_path = os.path.join(OUT_DIR, filename)
    if os.path.exists(out_path):
        print(f"  Skipping {filename} (already exists)")
        continue
    print(f"\n[{arxiv_id}]")
    try:
        fetch_first_page_thumb(arxiv_id, out_path)
    except Exception as e:
        print(f"  ERROR: {e}")
    time.sleep(1)  # be polite to arXiv

print("\nDone.")
