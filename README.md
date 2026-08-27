# AltayebAmer.com

موقع محفظة أعمال الفنان التشكيلي الطيب عامر — ثنائي اللغة (عربي/إنجليزي).
Bilingual portfolio site for visual artist Altayeb Amer.

> **لـ Claude Code:** اقرأ `CLAUDE.md` أولاً — فيه كل قواعد وبنية المشروع.
> **For Claude Code:** Read `CLAUDE.md` first — it contains all project rules and structure.

> **للنشر:** اتبع `DEPLOY.md` — قائمة تحقق كاملة.
> **To launch:** follow `DEPLOY.md`.

---

## النشر | Deployment

الموقع HTML خالص بلا build. الاستضافة عبر **Cloudflare Pages** والمستودع على **GitHub**.
Pure static HTML, no build. Hosted on **Cloudflare Pages**, repo on **GitHub**.

### الخطوات | Steps

1. ارفع كل الملفات إلى مستودع GitHub (ليس ملف ZIP — الملفات نفسها).
   Push all files to a GitHub repo (not a ZIP — the files themselves).

2. في Cloudflare Pages → **Connect to Git** → اختر المستودع.
   In Cloudflare Pages → **Connect to Git** → select the repo.

3. الإعدادات | Settings:
   - **Build command:** (اتركه فارغاً | leave empty)
   - **Output directory:** `/` (الجذر | root)

4. اربط النطاق من لوحة Cloudflare Pages مباشرة.
   Attach the domain directly from the Cloudflare Pages panel.

---

## لوحة التحكم | Content Management

`altayeb-cms-v5.html` — لوحة تحكم تعمل من المتصفح عبر GitHub API.
تحتاج: GitHub token + owner + repo + branch.
منها تُدير الصور، المقولات، والمحتوى بلا لمس الكود.

A browser-based CMS working via GitHub API. Needs a GitHub token + owner + repo + branch.
Manage images, quotes, and content without touching code.

> محجوبة من محركات البحث في `robots.txt`. | Blocked from search engines in `robots.txt`.

---

## معاينة محلية | Local Preview

```bash
python3 -m http.server 8000
# http://localhost:8000
```

### عبر Docker | Via Docker

```bash
docker compose up --build
# http://localhost:8080  (روابط نظيفة + MIME صحيح عبر nginx)
```

## الصور | Images

مجلد `images/` يعكس بنية الصور بالكامل (407 خانة). لاستبدال الصور الاحتياطية محلياً:
ضع الصور الأصلية بأسماء الخانات ثم `python3 tools/apply-images.py`.
راجع `images/README.md` و`PROJECT_AUDIT_REPORT.md`.

The `images/` folder mirrors all 407 image slots. To swap placeholders locally, drop real
images using the slot filenames, then run `python3 tools/apply-images.py`.
