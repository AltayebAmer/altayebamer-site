#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check-images.py — التحقق من الصور قبل ربطها بالموقع.

يفحص:
  • الأسماء   : ملفات باسم خاطئ أو في المجلد الخطأ
  • المقاسات  : أبعاد غير مطابقة للمطلوب (تحذير فقط)
  • النواقص   : الخانات التي لم تُملأ بعد
  • الزوائد   : ملفات لا تخصّ أي خانة

الاستعمال:
    python3 tools/check-images.py            # تقرير كامل
    python3 tools/check-images.py --missing  # الناقص فقط
"""
import json, os, sys, subprocess, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTS = (".webp", ".jpg", ".jpeg", ".png")
ONLY_MISSING = "--missing" in sys.argv

IMAGES = json.load(open(os.path.join(ROOT, "images", "IMAGE_MAP.json"), encoding="utf-8"))

# المقاس المتوقّع لكل نوع مجلد
def expected_dim(folder):
    if "/about/portrait" in folder:  return (1200, 1600)
    if "/about/workshop" in folder:  return (1200, 1200)
    if "/gallery/" in folder or "/_shared/" in folder: return (1600, 1200)
    return (1600, 1000)

def dims(path):
    """أبعاد الصورة عبر sips (متوفّر على macOS)."""
    try:
        out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path],
                             capture_output=True, text=True, timeout=10).stdout
        w = h = None
        for line in out.splitlines():
            if "pixelWidth:" in line:  w = int(line.split(":")[1])
            if "pixelHeight:" in line: h = int(line.split(":")[1])
        return (w, h) if w and h else None
    except Exception:
        return None

def find(stem):
    for e in EXTS:
        p = os.path.join(ROOT, stem + e)
        if os.path.isfile(p) and os.path.getsize(p) > 0:
            return stem + e
    return None

present, missing, wrong_dim, oversize = [], [], [], []
expected_files = set()

for im in IMAGES:
    stem = os.path.splitext(im["file"])[0]
    expected_files.add(os.path.join(ROOT, stem))
    got = find(stem)
    if not got:
        missing.append(im); continue
    present.append(im)
    p = os.path.join(ROOT, got)
    ew, eh = expected_dim(os.path.dirname(im["file"]))
    d = dims(p)
    if d and (abs(d[0]/d[1] - ew/eh) > 0.06):
        wrong_dim.append((got, d, (ew, eh)))
    if os.path.getsize(p) > 400 * 1024:
        oversize.append((got, os.path.getsize(p) // 1024))

# ملفات زائدة لا تخصّ أي خانة
stray = []
for root, _, files in os.walk(os.path.join(ROOT, "images")):
    for f in files:
        if f.startswith("00_") or f.startswith(".") or f.endswith((".json", ".csv", ".md", ".html")):
            continue
        full = os.path.join(root, f)
        if os.path.splitext(full)[0] not in expected_files:
            stray.append(os.path.relpath(full, ROOT))

tot = len(IMAGES)
print(f"\n{'='*58}")
print(f"  الصور المطلوبة: {tot}   |   موجودة: {len(present)}   |   ناقصة: {len(missing)}")
print(f"{'='*58}\n")

if missing and not ONLY_MISSING or (ONLY_MISSING and missing):
    by = collections.OrderedDict()
    for im in missing: by.setdefault(os.path.dirname(im["file"]), []).append(os.path.basename(im["file"]))
    print(f"■ ناقصة ({len(missing)}):")
    for folder, names in by.items():
        print(f"   {folder}/  — {len(names)} صورة")
        if len(names) <= 8:
            for n in names: print(f"      {n}")
    print()

if ONLY_MISSING:
    sys.exit(0)

if stray:
    print(f"■ ⚠️ ملفات باسم غير متوقّع ({len(stray)}) — تحقّق من التسمية:")
    for s in stray[:20]: print(f"      {s}")
    print()

if wrong_dim:
    print(f"■ ⚠️ نسبة أبعاد غير مطابقة ({len(wrong_dim)}):")
    for f, got, exp in wrong_dim[:15]:
        print(f"      {f}  →  {got[0]}×{got[1]}  (المتوقّع نسبة {exp[0]}×{exp[1]})")
    print()

if oversize:
    print(f"■ ⚠️ أكبر من 400KB ({len(oversize)}):")
    for f, kb in oversize[:15]: print(f"      {f}  —  {kb}KB")
    print()

if not missing and not stray and not wrong_dim and not oversize:
    print("✅ كل شيء سليم. شغّل الآن:  python3 tools/apply-images.py\n")
elif not missing:
    print("✅ لا توجد صور ناقصة (التحذيرات أعلاه اختيارية).\n")
