#!/usr/bin/env python3
"""
apply-images.py — استبدال الصور الاحتياطية (picsum) بالصور المحلية الأصلية.
Replace picsum placeholders in the HTML with local /images/... paths,
for every real image the artist has dropped into the images/ tree.

Usage:
    python3 tools/apply-images.py            # apply changes
    python3 tools/apply-images.py --dry-run  # show what would change, write nothing

How it works:
  images/IMAGE_MAP.json maps every target file path -> its current placeholder URL.
  For each target that now contains a REAL image (exists and is not a .gitkeep stub),
  every occurrence of that placeholder URL across all site HTML is rewritten to the
  local absolute path (e.g. /images/gallery/horses/oil/01.jpg).

Notes:
  - A placeholder seed can appear in several pages; all occurrences are updated.
  - Safe to run repeatedly. Already-localised URLs are left untouched.
"""
import json, os, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry-run" in sys.argv

mp = json.load(open(os.path.join(ROOT, "images", "IMAGE_MAP.json"), encoding="utf-8"))

# Accepted extensions, in priority order (smallest/most modern first).
# A file listed as "x.webp" is satisfied by x.webp, x.jpg, x.jpeg or x.png.
EXTS = (".webp", ".jpg", ".jpeg", ".png")

# NEW MODEL: one unique image = one file, reused wherever its placeholder appears.
repl = {}
missing = 0
for row in mp:
    stem = os.path.splitext(row["file"])[0]
    found = None
    for ext in EXTS:
        cand = os.path.join(ROOT, stem + ext)
        if os.path.isfile(cand) and os.path.getsize(cand) > 0:
            found = stem + ext
            break
    if found:
        repl[row["placeholder"]] = found.replace(os.sep, "/")
    else:
        missing += 1


def rel_for(html_path, img_path):
    """Path from the HTML file to the image (works under file:// and when served)."""
    d = os.path.dirname(os.path.abspath(html_path))
    return os.path.relpath(os.path.join(ROOT, img_path), d).replace(os.sep, "/")


# --- about/ uses inline base64 images, replaced positionally, not by URL ---
b64 = {k: v for k, v in repl.items() if k.startswith("BASE64#")}
for k in b64:
    del repl[k]

if b64:
    import re
    ab = os.path.join(ROOT, "about", "index.html")
    if os.path.isfile(ab):
        txt = open(ab, encoding="utf-8").read()
        # Inline images appear in document order: first 7 = portrait slides,
        # the following 21 = workshop grid. Replace strictly by position.
        order = ([f"BASE64#about_portrait#{i}" for i in range(1, 8)] +
                 [f"BASE64#about_workshop#{i}" for i in range(1, 22)])
        pos = [0]
        swapped = [0]

        def sub_inline(mm):
            i = pos[0]
            pos[0] += 1
            if i >= len(order):
                return mm.group(0)
            local = b64.get(order[i])
            if not local:
                return mm.group(0)
            swapped[0] += 1
            return mm.group(1) + rel_for(ab, local) + mm.group(3)

        new = re.sub(r'(<img[^>]*\ssrc=")(data:image[^"]*)(")', sub_inline, txt)
        if swapped[0]:
            print(f"{'[dry] ' if DRY else ''}about/index.html: "
                  f"{swapped[0]} inline image(s) replaced")
            if not DRY:
                open(ab, "w", encoding="utf-8").write(new)

if not repl:
    print(f"No URL-based images found yet. Drop images into images/ then re-run. "
          f"({missing} slots still empty)")
    sys.exit(0)

htmls = [f for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)]
total = 0
for f in htmls:
    txt = open(f, encoding="utf-8").read()
    orig = txt
    n = 0
    for ph, local in repl.items():
        if ph in txt:
            n += txt.count(ph)
            txt = txt.replace(ph, rel_for(f, local))
    if n and txt != orig:
        total += n
        rel = os.path.relpath(f, ROOT)
        print(f"{'[dry] ' if DRY else ''}{rel}: {n} replacement(s)")
        if not DRY:
            open(f, "w", encoding="utf-8").write(txt)

print(f"\n{'Would replace' if DRY else 'Replaced'} {total} placeholder occurrence(s) "
      f"using {len(repl)} local image(s). {missing} slot(s) still empty.")
if not DRY and total:
    print("Remember to update the CMS manifests too if you deploy via GitHub, "
          "or keep using local paths for Cloudflare.")
