# تقرير فحص مشروع AltayebAmer.com | Project Audit Report

**التاريخ | Date:** 2026-07-20 · **الفاحص | Auditor:** Claude Code
**الحالة العامة | Overall:** الموقع سليم بنيوياً ويعمل — أُصلحت أخطاء لغوية جوهرية، وبقيت مهام محتوى وتكامل.
Structurally sound and working — a major language bug was fixed; content & integration tasks remain.

---

## 1. ملخص تنفيذي | Executive Summary

| البند Item | العدد Count |
|---|---|
| صفحات HTML \| HTML pages | 23 |
| أخطاء بنيوية (html/body/script) \| structural tag errors | **0** |
| حقول لغة معكوسة أُصلحت \| swapped language fields fixed | **100** (calligraphy 52 + horses 48) |
| صور احتياطية (placeholders) \| placeholder images | **3,273** picsum + 1 unsplash |
| خانات صور مُهيّأة للاستبدال \| image slots scaffolded | **407** in 78 folders |
| مقالات مجلة فارغة المحتوى \| empty journal bodies | **112** (8 pages × 14) |

---

## 2. ما تم إنجازه في هذه الجلسة | Done This Session

1. **إصلاح تبادل اللغة (خطأ جوهري):** في `calligraphy/index.html` و`horses/index.html` كانت حقول `_en` تحوي نصاً عربياً و`_ar` تحوي إنجليزياً — أي النسخة الإنجليزية كانت تعرض عربي والعكس. صُحّح 100 زوج حقول، وتحقّقت سلامة JavaScript والعرض (HTTP 200 + المحتوى الصحيح).
   Fixed the `_en`/`_ar` reversal in the calligraphy & horses article arrays (100 field-pairs). JS parses; pages serve correctly.

2. **إصلاح مقولة مكررة:** استُبدلت مقولة "We do not photograph faces…" المكررة بين `portrait` و`photography` بمقولة أصلية جديدة خاصة بالبورتريه (ثنائية اللغة).
   Replaced the duplicate quote shared by portrait & photography with a new original bilingual one.

3. **مجلد صور احترافي `images/`:** 78 مجلداً / 407 خانة تعكس مانيفست لوحة التحكم (PIM + GIM) حرفياً، مع:
   - `images/IMAGE_MAP.csv` و`IMAGE_MAP.json` — خريطة كل خانة ↔ الصورة الاحتياطية الحالية.
   - `images/README.md` — دليل الاستبدال بطريقتين.
   - `tools/apply-images.py` — سكربت يستبدل روابط picsum بالصور المحلية تلقائياً (يدعم `--dry-run`).
   A professional `images/` tree (407 slots) mirroring the CMS manifests, with map files, a bilingual README, and an auto-swap script.

4. **بيئة اختبار Docker:** `Dockerfile` + `docker-compose.yml` + `nginx.conf` + `.dockerignore` — تشغيل الموقع محلياً على `http://localhost:8080` مع روابط نظيفة و MIME صحيح.
   Docker test environment (nginx) serving the site at localhost:8080 with clean URLs.

5. **اختبار:** تحقّق من تحميل كل الصفحات الرئيسية (200)، صفر أخطاء بنيوية في 23 صفحة.
   Verified all key pages load (200); zero structural errors across 23 pages.

---

## 3. المهام المتبقية (حسب الأولوية) | Outstanding Tasks (by priority)

### أولوية عالية | High
- **محتوى المقالات (112 مقالاً):** الصفحات الثماني (`index` + 7 اختصاصات) بها `JRN_ARTICLES` بعناوين كاملة ومحتوى فارغ (`body_en:''`). تحتاج كتابة بصوت الفنان وثنائية اللغة. *(نُفّذت 14 مقالاً لصفحة الحروفية في جلسة سابقة كنموذج.)*
  Fill 112 empty journal bodies in the artist's voice, bilingual.
- **الصور الحقيقية:** استبدال 3,273 صورة احتياطية بأعمال الفنان — الآن ميسّر عبر مجلد `images/` أو لوحة التحكم.
  Replace 3,273 placeholders with real artwork (now enabled via `images/` or the CMS).

### أولوية متوسطة | Medium
- **ربط النماذج:** `contact/` يستخدم `mailto:` فقط، و`commission/` بلا خدمة إيميل. يُنصح بـ Formspree أو EmailJS (عبر CDN، دون npm).
  Wire contact/commission forms to a real email service.
- **محتوى `about/` و`cv-*`:** سيرة الفنان الحقيقية وصورة شخصية (`about/` ما زال placeholder).
  Fill real bio & photo in about/ and CVs.
- **مرجع unsplash متبقٍّ:** إشارة واحدة داخل نص لوحة التحكم فقط (ليست صورة حية) — للتنظيف.
  One residual `unsplash` string inside the CMS text (not a live image) — cleanup only.

### أولوية منخفضة / تحسينات | Low / Enhancements
- Lightbox، انيميشن سكرول، تحويل PWA — عبر CDN فقط.
- مراجعة تكرار المقولات على مستوى الموقع (فحص أوّلي: أغلب المتكرر أوصاف meta وهي مقبولة).

---

## 4. لوحة التحكم | CMS (`altayeb-cms-v5.html`)

- **البنية سليمة:** تعمل من المتصفح عبر **GitHub API** (token + owner + repo + branch)، وتضم PIM (صور الصفحات) وGIM (343 صورة معرض) وإدارة المقولات والروابط.
- **لتشغيلها فعلياً تحتاج:** إنشاء مستودع GitHub، توليد Personal Access Token بصلاحية `repo`، وإدخال البيانات في اللوحة. لا يمكنني التحقق من الاتصال الحيّ دون هذه البيانات (وهي خطوة تخصّك — لا أُدخل رموز وصول).
  The CMS is structurally complete but requires your GitHub repo + token to verify live — that step is yours (I don't enter access tokens).
- محجوبة عن الفهرسة في `robots.txt` ✅.

---

## 5. كيفية الاختبار | How to Test

**Docker (المُوصى به):**
```bash
cd project
docker compose up --build      # ثم افتح http://localhost:8080
```

**بدون Docker:**
```bash
python3 -m http.server 8080    # ثم افتح http://localhost:8080
```

**استبدال الصور محلياً:**
```bash
# ضع الصور في images/... بنفس أسماء الخانات، ثم:
python3 tools/apply-images.py --dry-run   # معاينة
python3 tools/apply-images.py             # تطبيق
```

---

## 6. ملاحظة | Note
هذا المجلد لا يحتوي `CLAUDE.md` ولا `README.md` (موجودان في حزمة التسليم السابقة). يُنصح بنسخهما هنا ليقرأهما Claude Code تلقائياً في الجلسات القادمة.
This folder lacks `CLAUDE.md`/`README.md` (they were in the earlier delivery zip). Copy them here so future Claude Code sessions load the project rules automatically.
