from telethon import events, Button
from core.bot_client import bot

# Inline-mode helper with bilingual support (AR/EN)

HEADER_AR = (
    "╔════════════════════════════════════════════════╗\n"
    "║   𓆩 قائمة أوامر FLEX – مميّزة وسهلة الاستخدام 𓆪   ║\n"
    "╚════════════════════════════════════════════════╝\n"
)
FOOTER_AR = "\n— مستند الأوامر • FLEX (Inline) —\n"

HEADER_EN = (
    "╔════════════════════════════════════════════════╗\n"
    "║   𓆩 FLEX Commands – Beautiful and Easy to Use 𓆪   ║\n"
    "╚════════════════════════════════════════════════╝\n"
)
FOOTER_EN = "\n— Commands Reference • FLEX (Inline) —\n"

SEPARATOR = "\n┄┄┄┄┄┄┄┄┄┄┄\n"

COMMANDS_AR = {
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
        (".ذكاء <نص/بالرد>", "رد ذكي مختصر—مثال: .ذكاء كيف حالك → 'بخير الحمد لله!'."),
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
        (".ازالة <key>", "حذف بصمة ميمز."),
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

COMMANDS_EN = {
    "Statistics": [
        (".stats", "Show account stats: users, groups, channels, bots."),
        (".meinfo", "Advanced details: dialogs, bots, groups and channels."),
    ],
    "Storage": [
        (".enable_storage", "Create/enable a storage group for forwarding private messages."),
        (".disable_storage", "Disable storage and remove local group binding."),
    ],
    "Auto Replies": [
        (".add_reply + KEY + VALUE", "Add an auto reply for a specific keyword."),
        (".replies", "List all saved replies."),
        (".enable_here", "Enable auto replies in this group."),
        (".disable_here", "Disable auto replies in this group."),
    ],
    "AFK & Custom Replies": [
        (".afk_on", "Enable AFK auto replies."),
        (".custom_on", "Enable custom replies based on triggers."),
        (".afk_off", "Disable AFK and custom replies."),
        (".reply_template", "Set a reply template (reply to a message)."),
        (".reply <text>", "Add a custom reply to the replied message."),
        (".del_reply", "Delete a custom reply (reply to the original message)."),
        (".allow", "Allow this private chat from AFK restrictions."),
        (".disallow", "Remove allow for this private chat."),
    ],
    "Games": [
        (".dart [1-6] | 🎯", "Dart game. Optionally pick a number."),
        (".dice [1-6] | 🎲", "Dice game. Optionally pick a number."),
        (".basket [1-5] | 🏀", "Basketball mini game."),
        (".ball [1-5] | ⚽️", "Football mini game."),
        (".slot [1-64] | 🎰", "Slot machine."),
        (".gym", "Simple animated gym."),
        (".truthdare", "Open Truth/Dare menu."),
        (".dare", "Generate a light dare."),
        (".truth", "Generate a respectful truth question."),
    ],
    "Media & Tools": [
        (".youtube <query>", "Fetch first matching video from YouTube."),
        (".sticker", "Create a sticker from an image/sticker (reply to media)."),
        (".sticker_info", "Get sticker pack info."),
        (".tiktok <url>", "Download TikTok video without watermark."),
    ],
    "AI": [
        (".ai <text/reply>", "Smart brief answer—example: .ai how are you → 'I’m fine!'"),
        (".translate <lang> [text/reply]", "Smart translation via Google."),
        (".detect_lang [text/reply]", "Detect text language automatically."),
        (".summarize [sentences] (reply)", "Quick summary to N sentences."),
    ],
    "Hunting (Usernames)": [
        (".hunt <pattern>", "Start username hunting according to pattern."),
        (".hunt_status", "Show hunting status and attempts."),
        (".hunt_stop", "Stop current hunting process."),
    ],
    "Monitoring": [
        (".watch <@user>", "Watch user changes: name/photo/bio."),
        (".unwatch <@user>", "Stop watching user."),
    ],
    "Profile": [
        (".time_name_on", "Enable time in first name."),
        (".time_name_off", "Disable time and clean name."),
        (".name (text)", "Set first name with current time."),
        (".impersonate", "Impersonate replied user (name/bio/photo)."),
        (".restore", "Restore original name/bio/photo."),
    ],
    "Private Protection & Warnings": [
        (".private_protect", "Toggle private protection against bad words."),
        (".accept", "Accept replied user (no warnings)."),
        (".unaccept", "Remove acceptance for replied user."),
        (".clear_warnings", "Clear replied user warnings."),
        (".my_warnings", "Show your warnings count."),
        (".set_warning_template", "Change warning message (reply to text)."),
        (".show_template", "Show current warning template."),
        (".set_max_warnings <n>", "Set max warnings limit."),
        (".banned_list", "Show banned users list."),
        (".clear_banned", "Clear all banned users."),
    ],
    "Shortcuts & Memes": [
        (".shortcut + <key>", "Save a shortcut (reply to message)."),
        (".del_shortcut + <key>", "Delete a saved shortcut."),
        (".shortcuts", "List all saved shortcuts."),
        (".memes <key> <url>", "Add meme fingerprint as a link."),
        (".memes_save <key>", "Save meme from replied media."),
        (".memes_get <key>", "Send meme file if media or show link."),
        (".memes_show <key>", "Show meme linked to key."),
        (".memes_list", "Show meme keys list."),
        ("remove <key>", "Delete meme fingerprint."),
        (".memes_clear", "Delete all memes."),
    ],
    "Auto Publishing": [
        (".repeat <sec> <count> [text]", "Repeated publishing; can reply to photo/album."),
        (".rep <sec> <count> [text]", "Shortcut for repeat."),
        (".publish <sec> <count> [text]", "Another shortcut for repeat."),
        (".stop_auto_publish", "Stop all active publishing tasks."),
    ],
    "Channels & Groups Tools": [
        (".list_all_channels", "List public/private channels."),
        (".list_admin_channels", "List channels you admin."),
        (".list_my_channels", "List channels you own."),
        (".list_all_groups", "List all groups (normal/mega)."),
        (".list_admin_groups", "List groups you admin."),
        (".list_my_groups", "List groups you own."),
        (".inspect_group [reply/ID]", "Advanced info about group/channel."),
    ],
    "Administration": [
        (".ban [reply/ID/@]", "Ban a user from the group."),
        (".kick [reply/ID/@]", "Kick a user from the group."),
        (".restrict [reply/ID/@]", "Restrict user from sending messages."),
        (".unban [reply/ID/@]", "Unban user."),
        (".unrestrict [reply/ID/@]", "Unrestrict user."),
        (".admin_log", "Show last 25 admin actions with reasons."),
    ],
}

def build_section(title, items):
    lines = [f"• {cmd}\n  ⤷ {desc}" for cmd, desc in items]
    return f"【 {title} 】\n" + "\n".join(lines)

def build_help_text(commands, header, footer):
    parts = [header]
    for title, items in commands.items():
        parts.append(build_section(title, items))
        parts.append(SEPARATOR)
    parts.append(footer)
    return "\n".join(parts)

def build_menu_text(lang):
    return (HEADER_AR if lang == "AR" else HEADER_EN) + \
        ("اختر قسمًا من الأزرار أدناه لعرض أوامره مع الشرح.\n" if lang == "AR" else "Choose a section from the buttons below to view its commands and descriptions.\n") + \
        (FOOTER_AR if lang == "AR" else FOOTER_EN)

def build_menu_buttons(lang, sections):
    rows = []
    row = []
    prefix = f"inline_help:{lang}:idx:"
    for idx, title in enumerate(sections):
        row.append(Button.inline(title, data=(prefix + str(idx)).encode()))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([Button.inline("عرض الكل" if lang == "AR" else "Show All", data=f"inline_help:{lang}:ALL".encode())])
    return rows

def build_section_buttons_by_index(index, lang, sections):
    buttons = []
    nav = []
    if index > 0:
        nav.append(Button.inline("⟵ السابق" if lang == "AR" else "⟵ Prev", data=f"inline_help:{lang}:idx:{index-1}".encode()))
    else:
        nav.append(Button.inline("⟵ القائمة" if lang == "AR" else "⟵ Menu", data=f"inline_help:{lang}:MENU".encode()))
    if index < len(sections) - 1:
        nav.append(Button.inline("التالي ⟶" if lang == "AR" else "Next ⟶", data=f"inline_help:{lang}:idx:{index+1}".encode()))
    else:
        nav.append(Button.inline("⟵ القائمة" if lang == "AR" else "⟵ Menu", data=f"inline_help:{lang}:MENU".encode()))
    buttons.append(nav)
    buttons.append([
        Button.inline("القائمة الرئيسية" if lang == "AR" else "Main Menu", data=f"inline_help:{lang}:MENU".encode()),
        Button.inline("عرض الكل" if lang == "AR" else "Show All", data=f"inline_help:{lang}:ALL".encode())
    ])
    return buttons

# Only register if bot client exists
if bot is not None:
    @bot.on(events.InlineQuery)
    async def inline_query_handler(event):
        q = (event.query or "").strip().lower()
        # detect language from query keywords
        if q in ("", "الاوامر", "اوامر", "مساعدة", "help", "assist"):
            lang = "EN" if q in ("help", "assist") else "AR"
        elif q in ("english", "en"):
            lang = "EN"
        else:
            # default to AR for non-recognized queries to avoid confusion
            lang = "AR"

        commands = COMMANDS_AR if lang == "AR" else COMMANDS_EN
        sections = list(commands.keys())
        text = build_menu_text(lang)
        buttons = build_menu_buttons(lang, sections)
        await event.answer([
            event.builder.article(
                title=("قائمة المساعدة • FLEX" if lang == "AR" else "Help Menu • FLEX"),
                text=text,
                buttons=buttons,
                description=("افتح قائمة الأقسام بأزرار تنقل" if lang == "AR" else "Open sections menu with navigation buttons"),
            )
        ], cache_time=0)

    @bot.on(events.CallbackQuery)
    async def inline_help_callback(event):
        data = event.data or b""
        if not data.startswith(b"inline_help:"):
            return
        parts = data.decode().split(":")
        if len(parts) < 3:
            return
        lang = parts[1]
        commands = COMMANDS_AR if lang == "AR" else COMMANDS_EN
        sections = list(commands.keys())

        action = parts[2]
        if action in {"MENU", "ALL"}:
            if action == "MENU":
                await event.edit(build_menu_text(lang), buttons=build_menu_buttons(lang, sections))
            elif action == "ALL":
                await event.edit("جارٍ عرض جميع الأقسام..." if lang == "AR" else "Showing all sections...")
                text = build_help_text(commands, HEADER_AR if lang == "AR" else HEADER_EN, FOOTER_AR if lang == "AR" else FOOTER_EN)
                await bot.send_message(event.chat_id, text)
                await event.answer("تم الإرسال." if lang == "AR" else "Sent.")
            return
        if action.startswith("idx"):
            try:
                index = int(parts[3])
            except ValueError:
                await event.answer("فهرس غير صالح." if lang == "AR" else "Invalid index.", alert=True)
                return
            if not (0 <= index < len(sections)):
                await event.answer("خارج النطاق." if lang == "AR" else "Out of range.", alert=True)
                return
            title = sections[index]
            text = (HEADER_AR if lang == "AR" else HEADER_EN) + build_section(title, commands.get(title, [])) + (FOOTER_AR if lang == "AR" else FOOTER_EN)
            await event.edit(text, buttons=build_section_buttons_by_index(index, lang, sections))
            await event.answer(("تم فتح قسم: " + title) if lang == "AR" else ("Opened section: " + title))lethon import events, Button
from core.bot_client import bot

# Inline-mode helper with Arabic and English menus

HEADER_AR = (
    "╔════════════════════════════════════════════════╗\n"
    "║   𓆩 قائمة أوامر FLEX – مميّزة وسهلة الاستخدام 𓆪   ║\n"
    "╚════════════════════════════════════════════════╝\n"
)
FOOTER_AR = "\n— مستند الأوامر • FLEX (Inline) —\n"

HEADER_EN = (
    "╔════════════════════════════════════════════════╗\n"
    "║   𓆩 FLEX Commands – Elegant & Easy to Use 𓆪   ║\n"
    "╚════════════════════════════════════════════════╝\n"
)
FOOTER_EN = "\n— Command Reference • FLEX (Inline) —\n"

SEPARATOR = "\n┄┄┄┄┄┄┄┄┄┄┄\n"

# Arabic sections
COMMANDS_AR = {
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
        (".ذكاء <نص/بالرد>", "رد ذكي مختصر—مثال: .ذكاء كيف حالك → 'بخير الحمد لله!'."),
        (".ترجم <لغة> [نص/بالرد]", "ترجمة ذكية عبر Google (gpytranslate/deep-translator)."),
        (".كشف_لغة [نص/بالرد]", "كشف لغة النص تلقائيًا."),
        (".تلخيص [عدد_الجمل] (بالرد)", "تلخيص سريع للنص إلى عدد جمل محدد."),
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
SECTIONS_AR = list(COMMANDS_AR.keys())

# English sections
COMMANDS_EN = {
    "Statistics": [
        (".stats", "Show account statistics: users, groups, channels, bots."),
        (".myinfo", "Detailed info: private chats, groups, channels, admins, unread."),
    ],
    "Storage": [
        (".enable_storage", "Create and enable a storage mega-group for private forwards."),
        (".disable_storage", "Disable storage and remove local group binding."),
    ],
    "Auto Replies": [
        (".add_reply + key + text", "Add an auto-reply for a specific key."),
        (".replies", "List all stored replies."),
        (".enable_here", "Enable auto replies in current group."),
        (".disable_here", "Disable auto replies in current group."),
    ],
    "AFK & Custom Replies": [
        (".afk_on", "Turn on automatic private replies."),
        (".custom_on", "Enable custom replies by triggers."),
        (".afk_off", "Disable both AFK and custom replies."),
        (".reply_template", "Set a template message (by replying)."),
        (".reply <text>", "Add a custom reply for a trigger (reply to trigger)."),
        (".del_reply", "Delete a custom reply (reply to the trigger message)."),
        (".allow", "Allow a private chat from AFK restrictions."),
        (".disallow", "Remove allowance for a private chat."),
    ],
    "Games": [
        (".dart [1-6] | 🎯", "Dart game."),
        (".dice [1-6] | 🎲", "Dice game."),
        (".basket [1-5] | 🏀", "Basketball."),
        (".ball [1-5] | ⚽️", "Football."),
        (".slot [1-64] | 🎰", "Slot machine."),
        (".gym", "Gym animation."),
        (".truth_dare", "Open Truth/Dare menu."),
        (".dare", "Get a random dare."),
        (".truth", "Get a random truth."),
    ],
    "Media & Tools": [
        (".youtube <query>", "Find the first matching YouTube video."),
        (".sticker", "Create a sticker from an image/sticker (reply)."),
        (".sticker_info", "Get sticker pack info."),
        (".tiktok <link>", "Download TikTok video without watermark."),
    ],
    "AI": [
        (".ai <text/reply>", "Smart short reply. Example: .ai how are you → 'Fine, thanks!'."),
        (".translate <lang> [text/reply]", "Smart translation via Google."),
        (".detect_lang [text/reply]", "Detect language."),
        (".summarize [n] (reply)", "Quick summarization to n sentences."),
    ],
    "Channels & Groups Tools": [
        (".list channels_all", "List all channels."),
        (".list channels_admin", "Channels you admin."),
        (".list channels_owner", "Your channels (owner)."),
        (".list groups_all", "All groups."),
        (".list groups_admin", "Groups you admin."),
        (".list groups_owner", "Groups you own."),
        (".inspect_group [reply/ID]", "Inspect group/channel info."),
    ],
    "Administration": [
        (".ban [reply/ID/@]", "Ban a user from group."),
        (".kick [reply/ID/@]", "Kick a user from group."),
        (".restrict [reply/ID/@]", "Restrict a user from sending messages."),
        (".unban [reply/ID/@]", "Unban user."),
        (".unrestrict [reply/ID/@]", "Remove restrictions."),
    ],
}
SECTIONS_EN = list(COMMANDS_EN.keys())

def build_menu_text_ar():
    return HEADER_AR + "اختر قسمًا من الأزرار أدناه لعرض أوامره مع الشرح.\n" + FOOTER_AR

def build_menu_text_en():
    return HEADER_EN + "Pick a section from the buttons below to view its commands and descriptions.\n" + FOOTER_EN

def build_buttons(prefix, sections, english=False):
    rows = []
    row = []
    for idx, title in enumerate(sections):
        row.append(Button.inline(title, data=f"{prefix}:idx:{idx}".encode()))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([Button.inline("Show All" if english else "عرض الكل", data=f"{prefix}:ALL".encode())])
    return rows

def build_section_text_ar(title):
    items = COMMANDS_AR.get(title, [])
    lines = "\n".join([f"• {cmd}\n  ⤷ {desc}" for cmd, desc in items])
    return HEADER_AR + f"【 {title} 】\n" + lines + FOOTER_AR

def build_section_text_en(title):
    items = COMMANDS_EN.get(title, [])
    lines = "\n".join([f"• {cmd}\n  ⤷ {desc}" for cmd, desc in items])
    return HEADER_EN + f"【 {title} 】\n" + lines + FOOTER_EN

# Only register if bot client exists
if bot is not None:
    @bot.on(events.InlineQuery)
    async def inline_query_handler(event):
        q = (event.query or "").strip().lower()
        if q in ("", "مساعدة", "الاوامر", "اوامر"):
            await event.answer([
                event.builder.article(
                    title="قائمة المساعدة • FLEX",
                    text=build_menu_text_ar(),
                    buttons=build_buttons("inline_help_ar", SECTIONS_AR, english=False),
                    description="أفتح قائمة الأقسام بأزرار تنقل",
                )
            ], cache_time=0)
        elif q in ("help", "commands", "assist"):
            await event.answer([
                event.builder.article(
                    title="Help Menu • FLEX",
                    text=build_menu_text_en(),
                    buttons=build_buttons("inline_help_en", SECTIONS_EN, english=True),
                    description="Open sectioned command menu with navigation buttons",
                )
            ], cache_time=0)

    @bot.on(events.CallbackQuery)
    async def inline_help_callback(event):
        data = (event.data or b"").decode()
        if data.startswith("inline_help_ar:"):
            parts = data.split(":")
            if len(parts) == 2 and parts[1] in {"MENU", "ALL"}:
                if parts[1] == "MENU":
                    await event.edit(build_menu_text_ar(), buttons=build_buttons("inline_help_ar", SECTIONS_AR, english=False))
                else:
                    await event.edit("جارٍ عرض جميع الأقسام...")
                    text = HEADER_AR + "\n".join(
                        ["\n".join([f"【 {title} 】", "\n".join([f"• {c}\n  ⤷ {d}" for c, d in COMMANDS_AR[title]]), SEPARATOR]) for title in SECTIONS_AR]
                    ) + FOOTER_AR
                    await bot.send_message(event.chat_id, text)
                    await event.answer("تم الإرسال.")
                return
            if len(parts) == 3 and parts[1] == "idx":
                idx = int(parts[2])
                if not (0 <= idx < len(SECTIONS_AR)):
                    await event.answer("خارج النطاق.", alert=True)
                    return
                title = SECTIONS_AR[idx]
                await event.edit(build_section_text_ar(title), buttons=build_buttons("inline_help_ar", SECTIONS_AR, english=False))
                await event.answer(f"تم فتح قسم: {title}")
        elif data.startswith("inline_help_en:"):
            parts = data.split(":")
            if len(parts) == 2 and parts[1] in {"MENU", "ALL"}:
                if parts[1] == "MENU":
                    await event.edit(build_menu_text_en(), buttons=build_buttons("inline_help_en", SECTIONS_EN, english=True))
                else:
                    await event.edit("Showing all sections...")
                    text = HEADER_EN + "\n".join(
                        ["\n".join([f"【 {title} 】", "\n".join([f"• {c}\n  ⤷ {d}" for c, d in COMMANDS_EN[title]]), SEPARATOR]) for title in SECTIONS_EN]
                    ) + FOOTER_EN
                    await bot.send_message(event.chat_id, text)
                    await event.answer("Sent.")
                return
            if len(parts) == 3 and parts[1] == "idx":
                idx = int(parts[2])
                if not (0 <= idx < len(SECTIONS_EN)):
                    await event.answer("Out of range.", alert=True)
                    return
                title = SECTIONS_EN[idx]
                await event.edit(build_section_text_en(title), buttons=build_buttons("inline_help_en", SECTIONS_EN, english=True))
                await event.answer(f"Opened: {title}")lethon import events, Button
from core.bot_client import bot

# Inline-mode helper with Arabic and English menus

HEADER_AR = (
    "╔════════════════════════════════════════════════╗\n"
    "║   𓆩 قائمة أوامر FLEX – مميّزة وسهلة الاستخدام 𓆪   ║\n"
    "╚════════════════════════════════════════════════╝\n"
)
FOOTER_AR = "\n— مستند الأوامر • FLEX (Inline) —\n"

HEADER_EN = (
    "╔════════════════════════════════════════════════╗\n"
    "║   𓆩 FLEX Commands – Elegant & Easy to Use 𓆪   ║\n"
    "╚════════════════════════════════════════════════╝\n"
)
FOOTER_EN = "\n— Command Reference • FLEX (Inline) —\n"

SEPARATOR = "\n┄┄┄┄┄┄┄┄┄┄┄\n"

# Import sections from help.py by duplicating maps (to avoid circular imports)
COMMANDS_AR = {
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
        (".ذكاء <نص/بالرد>", "رد ذكي مختصر—مثال: .ذكاء كيف حالك → 'بخير الحمد لله!'."),
        (".ترجم <لغة> [نص/بالرد]", "ترجمة ذكية عبر Google (gpytranslate/deep-translator)."),
        (".كشف_لغة [نص/بالرد]", "كشف لغة النص تلقائيًا."),
        (".تلخيص [عدد_الجمل] (بالرد)", "تلخيص سريع للنص إلى عدد جمل محدد."),
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
SECTIONS_AR = list(COMMANDS_AR.keys())

COMMANDS_EN = {
    "Statistics": [
        (".stats", "Show account statistics: users, groups, channels, bots."),
        (".myinfo", "Detailed info: private chats, groups, channels, admins, unread."),
    ],
    "Storage": [
        (".enable_storage", "Create and enable a storage mega-group for private forwards."),
        (".disable_storage", "Disable storage and remove local group binding."),
    ],
    "Auto Replies": [
        (".add_reply + key + text", "Add an auto-reply for a specific key."),
        (".replies", "List all stored replies."),
        (".enable_here", "Enable auto replies in current group."),
        (".disable_here", "Disable auto replies in current group."),
    ],
    "AFK & Custom Replies": [
        (".afk_on", "Turn on automatic private replies."),
        (".custom_on", "Enable custom replies by triggers."),
        (".afk_off", "Disable both AFK and custom replies."),
        (".reply_template", "Set a template message (by replying)."),
        (".reply <text>", "Add a custom reply for a trigger (reply to trigger)."),
        (".del_reply", "Delete a custom reply (reply to the trigger message)."),
        (".allow", "Allow a private chat from AFK restrictions."),
        (".disallow", "Remove allowance for a private chat."),
    ],
    "Games": [
        (".dart [1-6] | 🎯", "Dart game."),
        (".dice [1-6] | 🎲", "Dice game."),
        (".basket [1-5] | 🏀", "Basketball."),
        (".ball [1-5] | ⚽️", "Football."),
        (".slot [1-64] | 🎰", "Slot machine."),
        (".gym", "Gym animation."),
        (".truth_dare", "Open Truth/Dare menu."),
        (".dare", "Get a random dare."),
        (".truth", "Get a random truth."),
    ],
    "Media & Tools": [
        (".youtube <query>", "Find the first matching YouTube video."),
        (".sticker", "Create a sticker from an image/sticker (reply)."),
        (".sticker_info", "Get sticker pack info."),
        (".tiktok <link>", "Download TikTok video without watermark."),
    ],
    "AI": [
        (".ai <text/reply>", "Smart short reply. Example: .ai how are you → 'Fine, thanks!'."),
        (".translate <lang> [text/reply]", "Smart translation via Google."),
        (".detect_lang [text/reply]", "Detect language."),
        (".summarize [n] (reply)", "Quick summarization to n sentences."),
    ],
    "Channels & Groups Tools": [
        (".list channels_all", "List all channels."),
        (".list channels_admin", "Channels you admin."),
        (".list channels_owner", "Your channels (owner)."),
        (".list groups_all", "All groups."),
        (".list groups_admin", "Groups you admin."),
        (".list groups_owner", "Groups you own."),
        (".inspect_group [reply/ID]", "Inspect group/channel info."),
    ],
    "Administration": [
        (".ban [reply/ID/@]", "Ban a user from group."),
        (".kick [reply/ID/@]", "Kick a user from group."),
        (".restrict [reply/ID/@]", "Restrict a user from sending messages."),
        (".unban [reply/ID/@]", "Unban user."),
        (".unrestrict [reply/ID/@]", "Remove restrictions."),
    ],
}
SECTIONS_EN = list(COMMANDS_EN.keys())

def build_menu_text_ar():
    return HEADER_AR + "اختر قسمًا من الأزرار أدناه لعرض أوامره مع الشرح.\n" + FOOTER_AR

def build_menu_text_en():
    return HEADER_EN + "Pick a section from the buttons below to view its commands and descriptions.\n" + FOOTER_EN

def build_buttons(prefix, sections, english=False):
    rows = []
    row = []
    for idx, title in enumerate(sections):
        row.append(Button.inline(title, data=f"{prefix}:idx:{idx}".encode()))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([Button.inline("Show All" if english else "عرض الكل", data=f"{prefix}:ALL".encode())])
    return rows

def build_section_text_ar(title):
    items = COMMANDS_AR.get(title, [])
    lines = "\n".join([f"• {cmd}\n  ⤷ {desc}" for cmd, desc in items])
    return HEADER_AR + f"【 {title} 】\n" + lines + FOOTER_AR

def build_section_text_en(title):
    items = COMMANDS_EN.get(title, [])
    lines = "\n".join([f"• {cmd}\n  ⤷ {desc}" for cmd, desc in items])
    return HEADER_EN + f"【 {title} 】\n" + lines + FOOTER_EN

# Only register if bot client exists
if bot is not None:
    @bot.on(events.InlineQuery)
    async def inline_query_handler(event):
        q = (event.query or "").strip().lower()
        if q in ("", "مساعدة", "الاوامر", "اوامر"):
            await event.answer([
                event.builder.article(
                    title="قائمة المساعدة • FLEX",
                    text=build_menu_text_ar(),
                    buttons=build_buttons("inline_help_ar", SECTIONS_AR, english=False),
                    description="أفتح قائمة الأقسام بأزرار تنقل",
                )
            ], cache_time=0)
        elif q in ("help", "commands", "assist"):
            await event.answer([
                event.builder.article(
                    title="Help Menu • FLEX",
                    text=build_menu_text_en(),
                    buttons=build_buttons("inline_help_en", SECTIONS_EN, english=True),
                    description="Open sectioned command menu with navigation buttons",
                )
            ], cache_time=0)

    @bot.on(events.CallbackQuery)
    async def inline_help_callback(event):
        data = (event.data or b"").decode()
        if data.startswith("inline_help_ar:"):
            parts = data.split(":")
            if len(parts) == 2 and parts[1] in {"MENU", "ALL"}:
                if parts[1] == "MENU":
                    await event.edit(build_menu_text_ar(), buttons=build_buttons("inline_help_ar", SECTIONS_AR, english=False))
                else:
                    await event.edit("جارٍ عرض جميع الأقسام...")
                    text = HEADER_AR + "\n".join(
                        ["\n".join([f"【 {title} 】", "\n".join([f"• {c}\n  ⤷ {d}" for c, d in COMMANDS_AR[title]]), SEPARATOR]) for title in SECTIONS_AR]
                    ) + FOOTER_AR
                    await bot.send_message(event.chat_id, text)
                    await event.answer("تم الإرسال.")
                return
            if len(parts) == 3 and parts[1] == "idx":
                idx = int(parts[2])
                if not (0 <= idx < len(SECTIONS_AR)):
                    await event.answer("خارج النطاق.", alert=True)
                    return
                title = SECTIONS_AR[idx]
                await event.edit(build_section_text_ar(title), buttons=build_buttons("inline_help_ar", SECTIONS_AR, english=False))
                await event.answer(f"تم فتح قسم: {title}")
        elif data.startswith("inline_help_en:"):
            parts = data.split(":")
            if len(parts) == 2 and parts[1] in {"MENU", "ALL"}:
                if parts[1] == "MENU":
                    await event.edit(build_menu_text_en(), buttons=build_buttons("inline_help_en", SECTIONS_EN, english=True))
                else:
                    await event.edit("Showing all sections...")
                    text = HEADER_EN + "\n".join(
                        ["\n".join([f"【 {title} 】", "\n".join([f"• {c}\n  ⤷ {d}" for c, d in COMMANDS_EN[title]]), SEPARATOR]) for title in SECTIONS_EN]
                    ) + FOOTER_EN
                    await bot.send_message(event.chat_id, text)
                    await event.answer("Sent.")
                return
            if len(parts) == 3 and parts[1] == "idx":
                idx = int(parts[2])
                if not (0 <= idx < len(SECTIONS_EN)):
                    await event.answer("Out of range.", alert=True)
                    return
                title = SECTIONS_EN[idx]
                await event.edit(build_section_text_en(title), buttons=build_buttons("inline_help_en", SECTIONS_EN, english=True))
                await event.answer(f"Opened: {title}")