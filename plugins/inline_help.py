from telethon import events, Button
from core.bot_client import bot

# Clean bilingual inline help (AR/EN) with updated sections

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

COMMANDS_AR = {
    "الإحصائيات": [
        (".احصائياتي", "يعرض إحصائيات الحساب: المستخدمين، المجموعات، القنوات، البوتات."),
        (".معلوماتي", "تفاصيل متقدمة عن الحساب: عدد المحادثات، البوتات، المجموعات والقنوات."),
    ],
    "التخزين": [
        (".تفعيل التخزين", "إنشاء/تفعيل كروب التخزين وإنشاء أقسامه."),
        (".تعطيل التخزين", "إيقاف التخزين وإلغاء الربط وإيقاف التحويل."),
        (".تعيين_تخزين", "تعيين كروب موجود كمخزن (بالرد داخل الكروب)."),
        (".حالة التخزين", "عرض حالة التخزين ومعلوماته."),
        (".تشغيل التحويل", "تشغيل التحويل التلقائي إلى كروب التخزين."),
        (".ايقاف التحويل", "إيقاف التحويل التلقائي إلى كروب التخزين."),
        (".اختبار التخزين", "إرسال رسالة اختبار إلى كروب التخزين."),
        (".تعيين_ارشيف <id> | بالرد", "تعيين محادثة الأرشيف بالمعرف أو بالرد."),
        (".أرشفة <أيام>", "نقل الوسائط الأقدم من عدد الأيام المحدد إلى الأرشيف."),
        (".storage_whitelist_add <chat_id>|بالرد", "إضافة مجموعة لقائمة السماح."),
        (".storage_whitelist_remove <chat_id>|بالرد", "إزالة مجموعة من قائمة السماح."),
        (".storage_whitelist_show", "عرض قائمة السماح."),
        (".storage_blacklist_add <chat_id>|بالرد", "إضافة مجموعة لقائمة الحظر."),
        (".storage_blacklist_remove <chat_id>|بالرد", "إزالة مجموعة من قائمة الحظر."),
        (".storage_blacklist_show", "عرض قائمة الحظر."),
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
        (".ترجم <لغة> [نص/بالرد]", "ترجمة ذكية عبر Google."),
        (".كشف_لغة [نص/بالرد]", "كشف لغة النص تلقائيًا."),
        (".تلخيص [عدد_الجمل] (بالرد)", "تلخيص سريع للنص."),
    ],
    "أدوات القنوات والمجموعات": [
        (".قائمه جميع القنوات", "عرض قائمة القنوات."),
        (".قائمه القنوات المشرف عليها", "القنوات التي أنت مشرف فيها."),
        (".قائمه قنواتي", "قنواتك (مالك)."),
        (".قائمه جميع المجموعات", "عرض جميع المجموعات."),
        (".قائمه مجموعات اديرها", "المجموعات التي أنت مشرف فيها."),
        (".قائمه كروباتي", "المجموعات التي أنت مالكها."),
        (".كشف المجموعة [reply/ID]", "معلومات متقدمة عن مجموعة/قناة."),
    ],
    "الإدارة": [
        (".حظر [reply/ID/@]", "حظر مستخدم."),
        (".طرد [reply/ID/@]", "طرد مستخدم."),
        (".تقييد [reply/ID/@]", "تقييد مستخدم."),
        (".الغاء الحظر [reply/ID/@]", "إلغاء الحظر."),
        (".الغاء التقييد [reply/ID/@]", "إلغاء التقييد."),
    ],
}

SECTIONS_AR = list(COMMANDS_AR.keys())

COMMANDS_EN = {
    "Statistics": [
        (".stats", "Show account stats: users, groups, channels, bots."),
        (".myinfo", "Advanced details: dialogs, bots, groups and channels."),
    ],
    "Storage": [
        (".enable_storage", "Create/enable storage group and initialize sections."),
        (".disable_storage", "Disable storage, unbind group and stop forwarding."),
        (".bind_storage", "Bind existing group as storage (reply inside)."),
        (".storage_status", "Show storage status, IDs, and forwarding state."),
        (".start_forward", "Turn on auto-forwarding."),
        (".stop_forward", "Turn off auto-forwarding."),
        (".storage_test", "Send a test message to storage."),
        (".set_archive <id> | reply", "Set archive chat by ID or by replying."),
        (".archive <days>", "Move media older than N days to archive."),
        (".storage_whitelist_add <chat_id>|reply", "Add a group to whitelist."),
        (".storage_whitelist_remove <chat_id>|reply", "Remove a group from whitelist."),
        (".storage_whitelist_show", "Show whitelist."),
        (".storage_blacklist_add <chat_id>|reply", "Add a group to blacklist."),
        (".storage_blacklist_remove <chat_id>|reply", "Remove a group from blacklist."),
        (".storage_blacklist_show", "Show blacklist."),
    ],
    "Auto Replies": [
        (".add_reply + KEY + VALUE", "Add an auto reply."),
        (".replies", "List saved replies."),
        (".enable_here", "Enable auto replies here."),
        (".disable_here", "Disable auto replies here."),
    ],
    "AFK & Custom Replies": [
        (".afk_on", "Enable AFK."),
        (".custom_on", "Enable custom replies."),
        (".afk_off", "Disable AFK/custom."),
        (".reply_template", "Set reply template (reply)."),
        (".reply <text>", "Add a custom reply (reply to trigger)."),
        (".del_reply", "Delete a custom reply (reply)."),
        (".allow", "Allow a private chat."),
        (".disallow", "Remove allowance."),
    ],
    "Games": [
        (".dart [1-6] | 🎯", "Dart game."),
        (".dice [1-6] | 🎲", "Dice game."),
        (".basket [1-5] | 🏀", "Basketball."),
        (".ball [1-5] | ⚽️", "Football."),
        (".slot [1-64] | 🎰", "Slot machine."),
        (".gym", "Gym animation."),
        (".truthdare", "Truth/Dare menu."),
        (".dare", "Random dare."),
        (".truth", "Random truth."),
    ],
    "Media & Tools": [
        (".youtube <query>", "Find first YouTube match."),
        (".sticker", "Create a sticker (reply)."),
        (".sticker_info", "Sticker pack info."),
        (".tiktok <url>", "TikTok video without watermark."),
    ],
    "AI": [
        (".ai <text/reply>", "Smart brief answer."),
        (".translate <lang> [text/reply]", "Smart translation."),
        (".detect_lang [text/reply]", "Detect language."),
        (".summarize [n] (reply)", "Summarize to N sentences."),
        (".anime <description>", "Suggest anime title."),
    ],
    "Channels & Groups Tools": [
        (".list_all_channels", "List channels."),
        (".list_admin_channels", "Channels you admin."),
        (".list_my_channels", "Channels you own."),
        (".list_all_groups", "List groups."),
        (".list_admin_groups", "Groups you admin."),
        (".list_my_groups", "Groups you own."),
        (".inspect_group [reply/ID]", "Inspect group/channel."),
    ],
    "Administration": [
        (".ban [reply/ID/@]", "Ban user."),
        (".kick [reply/ID/@]", "Kick user."),
        (".restrict [reply/ID/@]", "Restrict user."),
        (".unban [reply/ID/@]", "Unban user."),
        (".unrestrict [reply/ID/@]", "Unrestrict user."),
        (".admin_log", "Last 25 admin actions."),
    ],
}

SECTIONS_EN = list(COMMANDS_EN.keys())

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
    header = HEADER_AR if lang == "AR" else HEADER_EN
    footer = FOOTER_AR if lang == "AR" else FOOTER_EN
    intro = "اختر قسمًا من الأزرار أدناه لعرض أوامره مع الشرح.\n" if lang == "AR" else "Choose a section from the buttons below to view its commands and descriptions.\n"
    return header + intro + footer

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

# Register only if bot exists
if bot is not None:
    @bot.on(events.InlineQuery)
    async def inline_query_handler(event):
        q = (event.query or "").strip().lower()
        if q in ("", "مساعدة", "الاوامر", "اوامر"):
            lang = "AR"
        elif q in ("help", "commands", "assist"):
            lang = "EN"
        elif q in ("english", "en"):
            lang = "EN"
        else:
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
            else:
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