from telethon import events, Button
from core.client import client
from core.bot_client import bot

# تصميم مميز لقائمة الأوامر مع تقسيمات واضحة وزخرفة بسيطة
HEADER = (
    "╔════════════════════════════════════════════════╗\n"
    "║   𓆩 قائمة أوامر FLEX – مميّزة وسهلة الاستخدام 𓆪   ║\n"
    "╚════════════════════════════════════════════════╝\n"
)

FOOTER = "\n— مستند الأوامر • FLEX —\n"

SEPARATOR = "\n┄┄┄┄┄┄┄┄┄┄┄\n"

COMMANDS = {
    "الإحصائيات": [
        (".احصائياتي", "يعرض إحصائيات الحساب: المستخدمين، المجموعات، القنوات، البوتات."),
        (".معلوماتي", "تفاصيل متقدمة عن الحساب: عدد المحادثات، البوتات، المجموعات والقنوات."),
    ],
    "التخزين": [
        (".تفعيل التخزين", "إنشاء وتفعيل كروب تخزين خاص بالرسائل الواردة من الخاص."),
        (".تعطيل التخزين", "إيقاف التخزين وحذف تعريف مجموعة التخزين المحلية."),
    ],
    "الردود التلقائية": [
        (".اضف رد + الكلمة + الرد", "إضافة رد تلقائي للكلمة المحددة."),
        (".الردود", "عرض جميع الردود المخزنة."),
        (".تفعيل هنا", "تفعيل الردود التلقائية في المجموعة الحالية."),
        (".تعطيل هنا", "تعطيل الردود التلقائية في المجموعة الحالية."),
    ],
    "وضع الغياب والردود المخصصة": [
        (".تشغيل الرد", "تشغيل الرد التلقائي للخاص."),
        (".المخصص تشغيل", "تشغيل الردود المخصصة المبنية على نصوص محددة."),
        (".تعطيل الرد", "تعطيل الرد التلقائي والردود المخصصة."),
        (".كليشة الرد", "تعيين رسالة محددة لتكون كليشة الرد (بالرد على رسالة)."),
        (".رد <النص>", "إضافة رد مخصص لنص يتم الرد عليه."),
        (".حذف رد", "حذف رد مخصص (بالرد على نص مضاف سابقًا)."),
        (".سماح", "سماح محادثة خاصة معينة من قيود الرد."),
        (".الغاء السماح", "إلغاء السماح لمحادثة خاصة."),
    ],
    "الألعاب": [
        (".سهم [1-6] | 🎯", "لعبة السهم. يمكن تحديد رقم مطلوب."),
        (".نرد [1-6] | 🎲", "لعبة النرد. يمكن تحديد رقم مطلوب."),
        (".سله [1-5] | 🏀", "لعبة كرة السلة."),
        (".كرة [1-5] | ⚽️", "لعبة كرة القدم."),
        (".حظ [1-64] | 🎰", "آلة الحظ."),
        (".gym", "عرض متحرك رياضي بسيط."),
        (".احكام", "فتح قائمة لعبة الأحكام (حكم/حقيقة)."),
        (".حكم", "يولّد تحدّي/مهمّة خفيفة وعفوية."),
        (".حقيقة", "يولّد سؤال حقيقة محترم."),
    ],
    "الوسائط والأدوات": [
        (".يوتيوب <بحث>", "جلب أول فيديو مطابق من يوتيوب."),
        (".ملصق", "صنع ملصق من صورة/ملصق بالرد على الوسائط."),
        (".معلومات الملصق", "جلب معلومات حزمة الملصقات."),
        (".تك <رابط>", "تحميل فيديو تيك توك بدون علامة مائية."),
    ],
    "الذكاء الاصطناعي": [
        (".ترجم <لغة> [نص/بالرد]", "ترجمة ذكية عبر Google (gpytranslate/deep-translator)."),
        (".كشف_لغة [نص/بالرد]", "كشف لغة النص تلقائيًا."),
        (".تلخيص [عدد_الجمل] (بالرد)", "تلخيص سريع للنص إلى عدد جمل محدد."),
    ],
    "الصيد (يوزرات)": [
        (".صيد <نمط>", "بدء عملية صيد يوزر وفق النمط المحدد."),
        (".حالة الصيد", "عرض حالة الصيد وعدد المحاولات."),
        (".ايقاف الصيد", "إيقاف عملية الصيد الحالية."),
    ],
    "المراقبة": [
        (".مراقبة <@user>", "بدء مراقبة تغييرات الاسم/الصورة/البايو للمستخدم."),
        (".ايقاف_المراقبة <@user>", "إيقاف مراقبة المستخدم."),
    ],
    "الملف الشخصي": [
        (".تفعيل الاسم الوقتي", "إضافة الوقت تلقائيًا إلى الاسم."),
        (".تعطيل الاسم الوقتي", "إيقاف وإزالة الوقت من الاسم."),
        (".الاسم (الاسم)", "تعيين الاسم (مع الوقت الحالي)."),
        (".انتحال", "انتحال مستخدم ترد عليه (اسم/بايو/صورة)."),
        (".ارجاع", "استرجاع الاسم/البايو/الصورة الأصلية المخزنة."),
    ],
    "حماية الخاص والتحذيرات": [
        (".حماية الخاص", "تفعيل/تعطيل حماية الخاص من الكلمات السيئة."),
        (".قبول", "قبول مستخدم محدد (بالرد) لاستثنائه من التحذيرات."),
        (".الغاء القبول", "إلغاء قبول مستخدم (بالرد)."),
        (".مسح التحذيرات", "مسح جميع تحذيرات المستخدم (بالرد)."),
        (".التحذيرات", "عرض عدد تحذيراتك الحالية."),
        (".تعيين كليشة التحذير", "تغيير رسالة التحذير (بالرد على النص)."),
        (".عرض كليشة", "عرض رسالة التحذير الحالية."),
        (".عدد التحذيرات <n>", "تعديل الحد الأقصى المسموح من التحذيرات."),
        (".المحظورين", "عرض قائمة المحظورين (حسب التحذيرات)."),
        (".مسح المحظورين", "مسح جميع المحظورين من القائمة."),
    ],
    "الاختصارات والميمز": [
        (".اختصار + <كلمة>", "حفظ اختصار نصي (بالرد على رسالة)."),
        (".حذف اختصار + <كلمة>", "حذف اختصار محفوظ."),
        (".الاختصارات", "عرض جميع الاختصارات المحفوظة."),
        (".ميمز <key> <url>", "إضافة بصمة ميمز كرابط."),
        (".ميمز حفظ <key>", "حفظ بصمة ميمز من وسائط بالرد."),
        (".ميمز جلب <key>", "إرسال الميمز كملف إن كان وسيطًا أو عرض الرابط."),
        (".ميمز عرض <key>", "عرض الميمز المرتبط بالبصمة."),
        (".قائمة الميمز", "عرض قائمة بصمات الميمز."),
        ("ازالة <key>", "حذف بصمة ميمز."),
        (".ازالة_البصمات", "حذف جميع بصمات الميمز."),
    ],
    "النشر الآلي": [
        (".تكرار <ثواني> <عدد> [نص]", "نشر متكرر، يمكن بالرد على صورة/ألبوم."),
        (".تك <ثواني> <عدد> [نص]", "اختصار لأمر التكرار."),
        (".نشر <ثواني> <عدد> [نص]", "اختصار آخر لأمر التكرار."),
        (".ايقاف النشر التلقائي", "إيقاف جميع عمليات النشر المتكررة."),
    ],
    "أدوات القنوات والمجموعات": [
        (".قائمه جميع القنوات", "عرض قائمة القنوات العامة/الخاصة."),
        (".قائمه القنوات المشرف عليها", "عرض القنوات التي أنت مشرف فيها."),
        (".قائمه قنواتي", "عرض القنوات التي أنت مالكها."),
        (".قائمه جميع المجموعات", "عرض جميع المجموعات (العادية/الخارقة)."),
        (".قائمه مجموعات اديرها", "عرض المجموعات التي أنت مشرف فيها."),
        (".قائمه كروباتي", "عرض المجموعات التي أنت مالكها."),
        (".كشف المجموعة [reply/ID]", "كشف معلومات متقدمة عن مجموعة/قناة."),
    ],
    "الإدارة": [
        (".حظر [reply/ID/@]", "حظر مستخدم من المجموعة."),
        (".طرد [reply/ID/@]", "طرد مستخدم من المجموعة."),
        (".تقييد [reply/ID/@]", "تقييد إرسال الرسائل لمستخدم."),
        (".الغاء الحظر [reply/ID/@]", "إلغاء الحظر."),
        (".الغاء التقييد [reply/ID/@]", "إلغاء التقييد."),
    ],
}

SECTIONS = list(COMMANDS.keys())

def build_section(title, items):
    lines = [f"• {cmd}\n  ⤷ {desc}" for cmd, desc in items]
    return f"【 {title} 】\n" + "\n".join(lines)

def build_help_text():
    parts = [HEADER]
    for title, items in COMMANDS.items():
        parts.append(build_section(title, items))
        parts.append(SEPARATOR)
    parts.append(FOOTER)
    text = "\n".join(parts)
    return text

def build_section_text(title):
    items = COMMANDS.get(title, [])
    return HEADER + build_section(title, items) + FOOTER

def build_menu_text():
    return (
        HEADER
        + "اختر قسمًا من الأزرار أدناه لعرض أوامره مع الشرح.\n"
        + FOOTER
    )

def build_menu_buttons():
    # ترتيب الأسماء في أزرار من صفوف متوازنة
    rows = []
    row = []
    for idx, title in enumerate(SECTIONS):
        row.append(Button.inline(title, data=f"help:idx:{idx}".encode()))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    # صف أخير للأوامر العامة
    rows.append([Button.inline("عرض الكل", data=b"help:ALL")])
    return rows

def build_section_buttons_by_index(index):
    # أزرار تنقل: السابق/التالي + رجوع للقائمة
    buttons = []
    nav = []
    if index > 0:
        nav.append(Button.inline("⟵ السابق", data=f"help:idx:{index-1}".encode()))
    else:
        nav.append(Button.inline("⟵ القائمة", data=b"help:MENU"))
    if index < len(SECTIONS) - 1:
        nav.append(Button.inline("التالي ⟶", data=f"help:idx:{index+1}".encode()))
    else:
        nav.append(Button.inline("⟵ القائمة", data=b"help:MENU"))
    buttons.append(nav)
    # زر العودة الصريح + عرض الكل
    buttons.append([
        Button.inline("القائمة الرئيسية", data=b"help:MENU"),
        Button.inline("عرض الكل", data=b"help:ALL")
    ])
    return buttons

async def send_chunked(event, text, chunk_size=3500):
    chunks = []
    while text:
        chunks.append(text[:chunk_size])
        text = text[chunk_size:]
    if chunks:
        await event.edit(chunks[0])
        for ch in chunks[1:]:
            await event.respond(ch)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.(?:الاوامر|اوامر|help)$"))
async def show_commands(event):
    await event.edit("جارٍ إعداد قائمة الأوامر...")
    text = build_help_text()
    await send_chunked(event, text)

# قائمة المساعدة التفاعلية
@client.on(events.NewMessage(outgoing=True, pattern=r"\.(?:المساعدة|مساعدة)$"))
async def show_help_menu(event):
    # إذا كان هناك بوت مساعد؛ استخدمه لإرسال الأزرار (حسابات المستخدم لا تدعم الأزرار على الأغلب)
    if bot is not None:
        await bot.send_message(event.chat_id, build_menu_text(), buttons=build_menu_buttons())
        await event.delete()
    else:
        await event.edit(build_menu_text())
        await event.respond("BOT_TOKEN غير مضبوط؛ سيتم عرض القائمة بدون أزرار.")

# معالجات الأزرار عبر البوت
if bot is not None:
    @bot.on(events.CallbackQuery)
    async def help_callback(event):
        data = event.data or b""
        if not data.startswith(b"help:"):
            return
        parts = data.decode().split(":")
        # parts could be ["help", "MENU"] | ["help", "ALL"] | ["help", "idx", "N"] | ["help", "<title>"]
        if len(parts) == 2 and parts[1] in {"MENU", "ALL"}:
            key = parts[1]
            if key == "MENU":
                await event.edit(build_menu_text(), buttons=build_menu_buttons())
            elif key == "ALL":
                await event.edit("جارٍ عرض جميع الأقسام...")
                text = build_help_text()
                await bot.send_message(event.chat_id, text)
                await event.answer("تم الإرسال.")
            return
        if len(parts) == 3 and parts[1] == "idx":
            try:
                index = int(parts[2])
            except ValueError:
                await event.answer("فهرس غير صالح.", alert=True)
                return
            if not (0 <= index < len(SECTIONS)):
                await event.answer("خارج النطاق.", alert=True)
                return
            title = SECTIONS[index]
            text = build_section_text(title)
            await event.edit(text, buttons=build_section_buttons_by_index(index))
            await event.answer(f"تم فتح قسم: {title}")
            return
        # دعم قديم: العنوان مباشرةً
        key = parts[1]
        if key in COMMANDS:
            title = key
            index = SECTIONS.index(title)
            text = build_section_text(title)
            await event.edit(text, buttons=build_section_buttons_by_index(index))
            await event.answer(f"تم فتح قسم: {title}")
        else:
            await event.answer("قسم غير معروف.", alert=True)
else:
    # Fallback: لو لم يوجد بوت، لا داعي لالتقاط CallbackQuery
    pass