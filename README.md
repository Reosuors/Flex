# FLEX SOURCE - يوزر بوت تيليجرام

يوزر بوت تيليجرام متقدم مبني على مكتبة Telethon مع ميزات متنوعة ومحسن للعمل على منصة Render.

## الميزات

- ✨ رسائل متحركة بالإيموجي (`.متت` و `.شرير`)
- 🎭 تقليد المستخدمين (`.تقليد` و `.ايقاف التقليد`)
- 💾 تخزين الرسائل الخاصة (`.تفعيل التخزين`)
- 😂 أوامر ترفيهية متنوعة (`.انتحار`)
- 🔄 إبقاء البوت نشطاً على Render
- 📝 نظام تسجيل محسن

## متطلبات التشغيل

- حساب تيليجرام شخصي (ليس بوت)
- API_ID و API_HASH من [my.telegram.org](https://my.telegram.org)
- Session String للحساب

## التثبيت والتشغيل

### 1. الحصول على Session String

```bash
# تشغيل مولد Session String
python session_generator.py
```

أدخل API_ID و API_HASH ورقم هاتفك وكود التحقق.

### 2. التشغيل المحلي

```bash
# تثبيت المتطلبات
pip install -r requirements_clean.txt

# تعيين متغيرات البيئة
export API_ID="your_api_id"
export API_HASH="your_api_hash"
export STRING_SESSION="your_session_string"

# تشغيل اليوزر بوت
python main.py
```

### 3. النشر على Render

#### الطريقة الأولى: استخدام Docker (مستحسن)

1. ارفع المشروع إلى GitHub
2. اذهب إلى [render.com](https://render.com) وأنشئ حساب
3. اضغط على "New +" ثم "Web Service"
4. اربط حسابك بـ GitHub واختر المستودع
5. في إعدادات الخدمة:
   - **Name**: flex-userbot
   - **Environment**: Docker
   - **Dockerfile Path**: ./Dockerfile
   - **Plan**: Free

#### الطريقة الثانية: استخدام Python Runtime

1. استخدم ملف `render_updated.yaml` كإعداد
2. أو قم بالإعداد اليدوي:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements_clean.txt`
   - **Start Command**: `python main.py`

#### تعيين متغيرات البيئة

في صفحة إعدادات الخدمة، أضف المتغيرات التالية:

- `API_ID`: معرف التطبيق من Telegram
- `API_HASH`: هاش التطبيق من Telegram  
- `STRING_SESSION`: الـ Session String الذي حصلت عليه

## الأوامر المتاحة

| الأمر | الوصف |
|-------|--------|
| `.متت` | رسالة متحركة بإيموجي الضحك |
| `.شرير` | رسالة متحركة بإيموجي شريرة |
| `.تقليد` | تقليد مستخدم معين (رد على رسالته) |
| `.ايقاف التقليد` | إيقاف التقليد |
| `.انتحار` | رسالة ترفيهية |
| `.تفعيل التخزين` | تفعيل تخزين الرسائل الخاصة |

## هيكل المشروع

```
flex_userbot_render/
├── main.py                 # الملف الرئيسي لليوزر بوت
├── session_generator.py    # مولد Session String
├── requirements_clean.txt  # المتطلبات المحسنة
├── Dockerfile             # ملف Docker للنشر
├── render_updated.yaml    # إعدادات Render
├── Procfile_updated       # ملف Procfile محدث
├── .env.example          # مثال لمتغيرات البيئة
├── .gitignore            # ملفات مستبعدة من Git
└── README.md             # هذا الملف
```

## ملاحظات مهمة

⚠️ **تحذيرات أمنية:**
- لا تشارك Session String مع أي شخص
- احتفظ بمتغيرات البيئة في مكان آمن
- هذا يوزر بوت وليس بوت عادي - يعمل على حسابك الشخصي

🔧 **ملاحظات تقنية:**
- البوت يحفظ البيانات في ملفات `.pkl` محلياً
- يتم إنشاء مجلد `iage` تلقائياً للصور
- البوت يحتوي على نظام keep-alive لـ Render

## استكشاف الأخطاء

### إذا فشل النشر:
1. تحقق من صحة متغيرات البيئة
2. تأكد من أن Session String صالح وحديث
3. راجع سجلات الأخطاء في Render
4. تأكد من رفع جميع الملفات للمستودع

### إذا لم يستجب اليوزر بوت:
1. تحقق من اتصال الإنترنت
2. تأكد من أن Session String لم ينته
3. راجع سجلات التشغيل
4. تحقق من أن الحساب غير محظور

## الدعم والتطوير

- **المطور**: @nS_R_T
- **السورس الأصلي**: FLEX SOURCE
- **النسخة**: محسنة للعمل على Render

## الترخيص

هذا المشروع مخصص للاستخدام التعليمي والشخصي. يرجى احترام شروط استخدام تيليجرام.

