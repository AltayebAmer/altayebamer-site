# مجلد الصور | Images Folder

هذا المجلد يعكس **تماماً** بنية الصور في الموقع كما هي في لوحة التحكم (PIM + GIM).
This folder mirrors the site's image structure exactly as defined in the CMS (PIM + GIM manifests).

- **407 خانة صورة** موزعة على 78 مجلداً. | 407 image slots across 78 folders.
- كل خانة لها اسم ثابت (`hero-01.jpg`, `band-01.jpg`, `01.jpg` … `07.jpg`).
- الخريطة الكاملة: [`IMAGE_MAP.csv`](IMAGE_MAP.csv) و [`IMAGE_MAP.json`](IMAGE_MAP.json) — كل صف يربط مسار الملف بالصورة الاحتياطية الحالية ووصفها.

## البنية | Structure

```
images/
├── pages/                    صور الصفحات (Hero + Bands)
│   ├── index/hero/hero-01..07.jpg
│   ├── index/band/band-01..07.jpg
│   └── {calligraphy,horses,ai,design,portrait,education,photography}/band/band-0N.jpg
└── gallery/                  صور المعارض الفرعية (7 اختصاصات × 7 أقسام × 7 صور)
    └── {specialty}/{section-id}/01..07.jpg
```

## طريقتان للاستبدال | Two ways to replace placeholders

### 1) عبر المجلد مباشرة | Via this folder (local, immediate)
ضع الصورة الأصلية في مكان الخانة بنفس الاسم (مثلاً `images/gallery/horses/oil/01.jpg`)،
ثم شغّل من جذر المشروع:

```bash
python3 tools/apply-images.py
```

السكربت يستبدل رابط `picsum.photos` المقابل في صفحات HTML بمسار الصورة المحلية `/images/...`.
شغّله كلما أضفت صوراً جديدة. لمعاينة التغييرات دون كتابة: `python3 tools/apply-images.py --dry-run`.

### 2) عبر لوحة التحكم | Via the CMS
`altayeb-cms-v5.html` → أقسام PIM/GIM ترفع الصور إلى GitHub وتحدّث الروابط تلقائياً.
هذه الطريقة أفضل للنشر المباشر على Cloudflare دون رفع ملفات محلية.

## الصيغة الموصى بها | Recommended format: **WebP**

اختبار فعلي على نفس الصورة (1000×1333):

| الصيغة | الحجم | النسبة | وزن الموقع (407 صورة) |
|---|---|---|---|
| PNG | 1035 KB | 100% | ~411 MB |
| JPG | 557 KB | 54% | ~221 MB |
| **WebP** | **266 KB** | **26%** | **~106 MB** ✅ |

**WebP أصغر من JPG بـ 52%** بنفس الجودة تقريباً، ومدعوم في كل المتصفحات الحديثة
(Chrome, Firefox, Edge, Safari 14+) ويعمل مباشرة بلا أي build step.
WebP is 52% smaller than JPG at comparable quality, supported by all modern browsers.

> **المقاسات | Sizes:** 1600×1000 لصور المعرض والصفحات · 1200×1600 (نسبة 3:4) للصورة الشخصية.
> **الأسماء | Filenames:** حافظ على اسم الخانة، وغيّر اللاحقة فقط —
> الخانة المكتوبة `01.jpg` يقبلها السكربت بأي من: `.webp` `.jpg` `.jpeg` `.png` (الأولوية لـ WebP).
> A slot listed as `01.jpg` is satisfied by `01.webp`, `01.jpg`, `01.jpeg` or `01.png`.
