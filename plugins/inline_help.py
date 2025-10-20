from telethon import events, Button
from core.bot_client import bot

# Inline-mode helper so users can get interactive buttons in any chat
# even if the bot is not a member. Requires enabling inline mode in BotFather.

HEADER = (
    "╔════════════════════════════════════════════════╗\n"
    "║   𓆩 قائمة أوامر FLEX – مميّزة وسهلة الاستخدام 𓆪   ║\n"
    "╚════════════════════════════════════════════════╝\n"
)
FOOTER = "\n— مستند الأوامر • FLEX (Inline) —\n"
SEPARATOR = "\n┄┄┄┄┄┄┄┄┄┄┄\n"

# Keep sections in sync with plugins.help COMMANDS
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
    rows = []
    row = []
    for idx, title in enumerate(SECTIONS):
        row.append(Button.inline(title, data=f"inline_help:idx:{idx}".encode()))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([Button.inline("عرض الكل", data=b"inline_help:ALL")])
    return rows

def build_section_buttons_by_index(index):
    buttons = []
    nav = []
    if index > 0:
        nav.append(Button.inline("⟵ السابق", data=f"inline_help:idx:{index-1}".encode()))
    else:
        nav.append(Button.inline("⟵ القائمة", data=b"inline_help:MENU"))
    if index < len(SECTIONS) - 1:
        nav.append(Button.inline("التالي ⟶", data=f"inline_help:idx:{index+1}".encode()))
    else:
        nav.append(Button.inline("⟵ القائمة", data=b"inline_help:MENU"))
    buttons.append(nav)
    buttons.append([
        Button.inline("القائمة الرئيسية", data=b"inline_help:MENU"),
        Button.inline("عرض الكل", data=b"inline_help:ALL")
    ])
    return buttons

# Only register if bot client exists
if bot is not None:
    @bot.on(events.InlineQuery)
    async def inline_query_handler(event):
        # Trigger on keywords like 'help'/'مساعدة' or empty
        q = (event.query or "").strip().lower()
        if q not in ("", "help", "مساعدة", "الاوامر", "اوامر"):
            return
        # Build a single article that shows the menu with buttons
        text = build_menu_text()
        buttons = build_menu_buttons()
        await event.answer([
            event.builder.article(
                title="قائمة المساعدة • FLEX",
                text=text,
                buttons=buttons,
                description="أفتح قائمة الأقسام بأزرار تنقل",
            )
        ], cache_time=0)

    @bot.on(events.CallbackQuery)
    async def inline_help_callback(event):
        data = event.data or b""
        if not data.startswith(b"inline_help:"):
            return
        parts = data.decode().split(":")
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
        else:
            await event.answer("أمر غير معروف.", alert=True)