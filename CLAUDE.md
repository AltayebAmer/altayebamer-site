# CLAUDE.md — دليل مشروع AltayebAmer.com

> هذا الملف يُحمَّل تلقائياً في كل جلسة Claude Code. اقرأه بالكامل قبل أي تعديل.
> This file loads into every Claude Code session. Read it fully before editing anything.

---

## 1. ما هو المشروع | What This Is

موقع محفظة أعمال ثنائي اللغة (عربي/إنجليزي) للفنان التشكيلي **الطيب عامر** — مقيم في دبي.
سبعة اختصاصات فنية، معرض أعمال، مجلة مقالات، ولوحة تحكم لإدارة المحتوى.

A bilingual (Arabic/English) portfolio site for visual artist **Altayeb Amer**, based in Dubai.
Seven art specialties, a gallery, a journal, and a content-management panel.

**المكدس التقني | Stack:** Pure static HTML + CSS + vanilla JavaScript. **No build step. No framework. No npm.**

---

## 2. قواعد حرجة — لا تكسرها أبداً | CRITICAL RULES — Never Break

1. **لا build process.** الموقع HTML خالص. لا تُضِف Vite/Webpack/React/npm. لا تُنشئ `package.json`.
   No build process. Pure HTML. Do not add Vite/Webpack/React/npm. Do not create `package.json`.

2. **كل البيانات مضمّنة inline داخل HTML.** لا يوجد `fetch()` للبيانات في أي صفحة موقع.
   ملفات `data/*.json` تُستخدم **فقط** من لوحة التحكم عبر GitHub API — لا يقرؤها المتصفح.
   All data is inline inside the HTML. There is **no `fetch()`** for data in any site page.
   The `data/*.json` files are used **only** by the CMS via GitHub API — the browser never reads them.

3. **الصور روابط `picsum.photos` مؤقتة** (placeholders) تُستبدل لاحقاً بالصور الحقيقية عبر لوحة التحكم.
   لا تُعِد Unsplash أبداً (تسبب مشاكل CORS/timeout على Cloudflare).
   Images are temporary `picsum.photos` placeholders, replaced later with real images via the CMS.
   Never reintroduce Unsplash (it causes CORS/timeout issues on Cloudflare).

4. **ثنائية اللغة عبر `data-lang`.** كل نص مرئي يُلَف في `<span class="t-en">...</span><span class="t-ar">...</span>`.
   تبديل اللغة يتحكم به `document.documentElement.getAttribute('data-lang')` بقيمة `'en'` أو `'ar'`.
   احترم هذا النمط دائماً — أي نص جديد يجب أن يكون بالنسختين.
   Bilingual via `data-lang`. Every visible string is wrapped in `<span class="t-en">…</span><span class="t-ar">…</span>`.
   Language toggle is driven by `document.documentElement.getAttribute('data-lang')` = `'en'` or `'ar'`.
   Always respect this — any new text must exist in both languages.

5. **لا تُعدّل الملفات داخل مجلدات نظامية** (`data/`, `js/`) دون فهم أثرها على لوحة التحكم.
   Do not edit files under system folders without understanding CMS impact.

6. **لا تُفهرِس لوحة التحكم.** `altayeb-cms-v5.html` محجوب في `robots.txt`. أبقِه محجوباً.
   Do not index the CMS. `altayeb-cms-v5.html` is blocked in `robots.txt`. Keep it blocked.

---

## 3. الاستضافة والنشر | Hosting & Deployment

- **النطاق + الخادم:** Cloudflare (النطاق مُشترى من Cloudflare، الاستضافة عبر Cloudflare Pages المجاني).
- **المستودع:** GitHub. لوحة التحكم تُعدّل الملفات عبر **GitHub token + GitHub API** مباشرة.
- **سير النشر:** رفع الملفات إلى GitHub → Cloudflare Pages يسحبها تلقائياً.
- **إعداد Cloudflare Pages:** Build command = **فارغ** | Output directory = **`/`** (الجذر).

- Domain + host: Cloudflare (domain bought from Cloudflare, hosted on free Cloudflare Pages).
- Repo: GitHub. The CMS edits files via **GitHub token + GitHub API** directly.
- Deploy flow: push files to GitHub → Cloudflare Pages auto-deploys.
- Cloudflare Pages config: Build command = **empty** | Output directory = **`/`** (root).

**ملفات إعداد Cloudflare الموجودة | Existing Cloudflare config files:**
- `_headers` — يضبط MIME types (JSON/JS/HTML) والتخزين المؤقت | sets MIME types & caching
- `_redirects` — يمنع 404 عند الدخول المباشر لصفحات gallery | prevents 404 on direct gallery URLs
- `sitemap.xml` — خريطة الموقع لمحركات البحث | sitemap for search engines
- `robots.txt` — يسمح بالفهرسة، يحجب لوحة التحكم | allows indexing, blocks the CMS

---

## 4. بنية الملفات | File Structure

```
/
├── index.html                  # الصفحة الرئيسية (Hero + 7 اختصاصات + مجلة)
├── altayeb-cms-v5.html         # لوحة التحكم (CMS) — لا تُفهرَس
├── _headers, _redirects        # إعداد Cloudflare
├── sitemap.xml, robots.txt     # SEO
├── CLAUDE.md                   # هذا الملف
│
├── data/
│   ├── specialties.json        # مرجع CMS فقط: التخصصات + الأقسام + الصور
│   └── gallery_quotes.json     # مرجع CMS فقط: مقولات الفنان
│
├── js/
│   └── random-gallery-engine.js  # محرك الغاليري (شبكة/منبثقات/سلايدشو)
│
├── الاختصاصات السبعة | 7 specialty pages:
│   ├── calligraphy/index.html  # الحروفية وفن الخط — var CALLIGRAPHY_DATA
│   ├── horses/index.html       # الخيل العربية
│   ├── ai/index.html           # الذكاء الاصطناعي
│   ├── design/index.html       # التصميم المرئي
│   ├── portrait/index.html     # الرسم والتشكيل (كان "البورتريه" سابقاً)
│   ├── education/index.html    # تعليم الفن
│   └── photography/index.html  # التطبيقات البصرية
│
├── gallery/
│   ├── index.html              # المعرض العام — var GALLERY_DATA (7 اختصاصات)
│   └── {ai,horses,calligraphy,design,portrait,education,photography}/index.html
│                               # صفحات معرض فرعية — var SECTION_DATA (7 أقسام × 7 صور)
│
├── statement/{7 اختصاصات}/index.html  # البيان الفني — 7 صفحات × 7 حركات، ثنائية اللغة
│                               # Artist Statement pages (7 movements each)
│
├── journal/index.html          # المجلة — const ARTICLES (14 مقال كامل)
│
└── صفحات إضافية | extra pages:
    ├── about/index.html
    ├── commission/index.html
    ├── contact/index.html
    ├── cv-ar.html, cv-en.html
```

---

## 5. أنظمة البيانات — أين يعيش كل شيء | Data Systems — Where Everything Lives

### أ) صور الاختصاصات | Specialty images
- **الصفحات الفرعية للمعرض** (`gallery/{x}/index.html`): متغير `var SECTION_DATA` — كائن يحوي `sections[]`، كل قسم فيه `id, en, ar, images[]`. كل قسم = 7 صور فريدة تتكرر لملء 49 خانة.
- **المعرض العام** (`gallery/index.html`): متغير `var GALLERY_DATA` — 7 اختصاصات، صورة واحدة لكل اختصاص في الـ Hero.
- **صفحة الحروفية** تحديداً تستخدم `var CALLIGRAPHY_DATA`. باقي صفحات الاختصاص تُخزّن الصور inline داخل عناصر band مباشرة.

### ب) المقولات | Quotes
- **صفحات الاختصاص السبع:** مصفوفات JS داخل الصفحة: `Q_SPEC` (7)، `Q_T1`، `Q_T2`، `Q_T3` (7 لكل منها) = 28 مقولة لكل صفحة.
- **`data/gallery_quotes.json`:** 56 مقولة (مرجع CMS).
- **إجمالي المقولات ~252، جميعها فريدة** عدا استثناء واحد معروف (انظر §7).

### ج) المقالات / المجلة | Articles / Journal
نظامان مختلفان — انتبه للفرق:

1. **`journal/index.html`** — النظام الكامل: `const ARTICLES = [...]` فيه 14 مقالاً **بمحتوى كامل** (`cat_en, cat_ar, title_en, title_ar, excerpt_en, excerpt_ar, body_en, body_ar`). دالة العرض `openArticle(idx)`.

2. **الصفحات الثماني الأخرى** (`index.html` + 7 اختصاصات) — نظام البطاقات المختصر: `var JRN_ARTICLES = [...]` فيه 14 عنصراً، **العناوين موجودة والمحتوى فارغ** (`body_en:'', body_ar:''`). دالة العرض `jrnOpen(idx)`. عند فتح مقال فارغ يظهر "المقال قيد الإعداد — سيُضاف قريباً".
   > **المهمة المتبقية:** ملء `body_en` و`body_ar` لهذه المقالات (الطيب سيفعل ذلك عبر لوحة التحكم، أو يمكن ملؤها برمجياً هنا).

---

## 6. أنظمة لوحة التحكم | CMS Systems (`altayeb-cms-v5.html`)

لوحة مستقلة تعمل من المتصفح عبر **GitHub API**. تحتاج: token + owner + repo + branch.

**الدخول:** لا توجد كلمة مرور مكتوبة داخل الملف. أول فتح يطلب إنشاء واحدة تُحفظ **مُشفّرة (SHA-256)**
في `localStorage` تحت `aa_pass_h`. القفل بعد ٥ محاولات يصمد بعد إعادة التحميل (`aa_lock`)،
والجلسة تُقفل تلقائياً بعد ٣٠ دقيقة خمول. **لا تُعِد كلمة مرور صريحة — الملف قابل للتنزيل علناً.**

**التوكن:** `aa_gh_tok` بترميز base64 في `localStorage`، أو `sessionStorage` عند اختيار
«لهذه الجلسة فقط». الترميز ليس تشفيراً — التحذير مكتوب داخل اللوحة، لا تحذفه.

### ما يكتب في الموقع فعلاً | Writes to the live site
- **PIM** — `var PIM_MANIFEST`: **١٧ صفحة / ١٢٦ خانة** (شاملة قسم البيان الفني والمعرض العام).
- **GIM** — `var GIM_MANIFEST`: ٧ صفحات معرض × ٧ أقسام × ٧ صور فريدة = ٣٤٣.
- **محرر الملفات** (٣٥ ملفاً) · **الرقع Patches** · **إصلاح الروابط / Responsive**.

### ما يُحفظ محلياً فقط | Local-only (localStorage)
المقالات، الاقتباسات، الروابط، بيانات التواصل، مكتبة الصور — **لا تصل صفحات الموقع**،
وزر «النشر» يرفع `content.json` ولا يقرؤه أي جزء من الموقع. التنبيهات موضّحة داخل اللوحة؛ لا تُزلها.

### قواعد صيانة | Maintenance rules
- **المانيفستات لقطات ثابتة.** أي تغيير لروابط الصور يجب أن يُقابله تحديث المانيفست،
  وإلا فشل الاستبدال برسالة «الرابط القديم غير موجود».
  استخدم **«فحص صحة مانيفست الصور»** في صفحة الأدوات — وهي موجودة لهذا الغرض.
- **مصدر الحقيقة للصور هو `images/IMAGE_MAP.json`.** أعِد توليد المانيفستات منه عند أي تغيير بنيوي.
- **لا تكتب أداة تستبدل كتلة HTML كاملة.** `runNavFix` كان يستبدل `<nav>` كله فيحذف روابط؛
  صار يصحّح **المسارات فقط**، ومعه وضع «فحص بلا تعديل». أبقِ هذا النمط.

---

## 7. المهام المتبقية | Outstanding Tasks

> اكتملت جاهزية النشر التقنية على ٣١ صفحة: SEO كامل، أيقونات، ٤٠٤، أمان، وصولية،
> بيانات منظمة، ومانيفستات لوحة سليمة ١٠٠٪. انظر `DEPLOY.md`.

1. **الصور الحقيقية** — `images/` فيه ٤٧٠ خانة مسمّاة و٢٩ صورة جاهزة فقط.
   ضع الصور بأسمائها ثم `python3 tools/apply-images.py`. الصور الفريدة المطلوبة نحو **٢٨٥**.

2. **ربط النموذجين بالبريد** — ضع معرّف Formspree في `FORMSPREE_ID` داخل
   `contact/index.html` و`commission/index.html`. بدونه يعمل الاحتياط عبر برنامج البريد.

3. **الروابط الاجتماعية** — JSON-LD في `index.html` يحوي يوتيوب فقط في `sameAs`.

4. **مراجعة نصوص المقالات** — ١١٢ مقالاً بلغتين مكتوبة، متوسطها نحو ٨٥ كلمة.
   جيدة كبطاقات، قصيرة كمقالات — قرار محتوى لا عطل.

---

## 8. أسلوب العمل المطلوب | How to Work Here

- **جلسات صغيرة مركّزة:** هدف واحد واضح لكل جلسة (مثل: "املأ مقالات الحروفية الأربعة عشر فقط"). لا جلسات ماراثونية.
  Small focused sessions: one clear objective each. No marathon sessions.

- **حرّر الملفات مباشرة وتحقّق فوراً.** لا تُنتج نصوصاً طويلة في المحادثة — اكتب في الملف واختبره.
  Edit files directly and verify immediately. Don't dump long text in chat — write to the file and test it.

- **راجع قبل الدفع:** استخدم `git diff` لمراجعة كل تغيير، و`git checkout -- <file>` للتراجع عند الحاجة، قبل `git push`.
  Review before pushing: use `git diff`, revert with `git checkout -- <file>` if needed, before `git push`.

- **افحص توازن الوسوم** بعد أي تعديل HTML كبير (html/body/script يجب أن تكون متوازنة). الحالة الحالية: صفر أخطاء هيكلية في 23 صفحة.
  Check tag balance after big HTML edits. Current state: zero structural errors across 23 pages.

- **الحفاظ على ثنائية اللغة** في كل إضافة نصية (§4 قاعدة 4).
  Preserve bilingualism in every text addition.

- **لا تلمس `node_modules` أو ملفات النظام** إن ظهرت — فهي ليست جزءاً من المشروع.

---

## 9. اختبار سريع | Quick Test

لا يوجد اختبارات آلية. للتحقق البصري، شغّل خادماً محلياً بسيطاً:
No automated tests. For visual verification, run a simple local server:

```bash
python3 -m http.server 8000
# ثم افتح | then open: http://localhost:8000
```

تحقق من: تبديل اللغة يعمل، الغاليري يفتح، أزرار المجلة تفتح المنبثقات، التنقل بين الصفحات سليم.
Verify: language toggle works, gallery opens, journal buttons open overlays, page navigation intact.

---

## 10. حقائق سريعة | Quick Facts

- ٣١ صفحة عامة (منها ٤٠٤) + لوحة التحكم | 31 public pages + CMS
- ٧ اختصاصات × (صفحة اختصاص + بيان فني + معرض فرعي)
- ٤٧٠ خانة صورة في `images/` عبر ٧٨ مجلداً، ٢٩ جاهزة
- ١١٢ مقالاً × لغتين = ٢٢٤ نصاً مكتوباً + ١٤ مقالاً كاملاً في المجلة
- ~٢٥٢ مقولة أصلية، جميعها فريدة
- SEO كامل: canonical + Open Graph + Twitter على ٣٠ صفحة، وJSON-LD في الرئيسية
- مانيفستات اللوحة: PIM ١٢٦/١٢٦ · GIM ٣٤٣/٣٤٣ سليمة
- صفر أخطاء بنيوية · صفر روابط مكسورة · صفر حقول لغة معكوسة
