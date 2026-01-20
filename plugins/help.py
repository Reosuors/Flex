from telethon import events, Button
from core.client import client
from core.bot_client import bot

# زخرفة
HEADER_AR = (
    "╔════════════════════════════════════════════════════╗\n"
    "║       ✦ دليل أوامر FLEX — تصميم أنيق وخفيف ✦       ║\n"
    "╚════════════════════════════════════════════════════╝\n"
)
FOOTER_AR = "\n⟡ تلميح: لعرض قسم محدد اكتب .م1 — وللإنجليزية .c1 ⟡\n"

HEADER_EN = (
    "╔════════════════════════════════════════════════════╗\n"
    "║        ✦ FLEX Commands — Clean & Elegant ✦         ║\n"
    "╚════════════════════════════════════════════════════╝\n"
)
FOOTER_EN = "\n⟡ Tip: Show a specific section with .c1 — Arabic via .م1 ⟡\n"

SEPARATOR = "\n────────────────────────────────────────────────────\n"

# العربية
COMMANDS_AR = {
    "الإحصائيات": [
        (".احصائياتي", "يعرض إحصائيات الحساب: المستخدمين، المجموعات، القنوات، البوتات."),
        (".معلوماتي", "تفاصيل متقدمة عن الحساب: عدد المحادثات، البوتات، المجموعات والقنوات."),
    ],
    "التخزين": [
        (".تفعيل التخزين", "إنشاء/تفعيل كروب التخزين وإنشاء أقسامه."),
        (".تعطيل التخزين", "إيقاف التخزين وإلغاء ربط الكروب وإيقاف التحويل."),
        (".تعيين_تخزين", "تعيين كروب موجود كمخزن (بالرد على رسالة داخل الكروب)."),
        (".حالة التخزين", "عرض حالة التخزين، معرف الكروب/الأرشيف، وحالة التحويل."),
        (".تشغيل التحويل", "تشغيل التحويل التلقائي إلى كروب التخزين."),
        (".ايقاف التحويل", "إيقاف التحويل التلقائي إلى كروب التخزين."),
        (".اختبار التخزين", "إرسال رسالة اختبار إلى كروب التخزين."),
        (".تعيين_ارشيف <id> | بالرد", "تعيين محادثة الأرشيف بالمعرف أو بالرد."),
        (".أرشفة <أيام>", "نقل الوسائط الأقدم من عدد الأيام المحدد إلى الأرشيف."),
        (".storage_whitelist_add <chat_id>|بالرد", "إضافة مجموعة لقائمة السماح بالتحويل."),
        (".storage_whitelist_remove <chat_id>|بالرد", "إزالة مجموعة من قائمة السماح."),
        (".storage_whitelist_show", "عرض قائمة السماح الحالية."),
        (".storage_blacklist_add <chat_id>|بالرد", "إضافة مجموعة لقائمة الحظر (يتم تجاهلها)."),
        (".storage_blacklist_remove <chat_id>|بالرد", "إزالة مجموعة من قائمة الحظر."),
        (".storage_blacklist_show", "عرض قائمة الحظر الحالية."),
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
        (".انمي <وصف>", "اقتراح اسم أنمي من وصف/قصة قصيرة."),
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
    "الفحص": [
        (".فحص", "إرسال صورة الفحص العربية مع التعليق الافتراضي أو المخصص."),
        (".تعيين صورة فحص عربي <رابط> | بالرد على صورة", "تعيين/حفظ صورة الفحص العربية (من رابط أو بالرد على وسائط)."),
        (".تعيين صورة فحص انجليزي <رابط> | بالرد على صورة", "تعيين/حفظ صورة الفحص الإنجليزية (من رابط أو بالرد على وسائط)."),
        (".مسح صورة فحص عربي", "مسح إعداد صورة الفحص العربية والرجوع للوضع الافتراضي."),
        (".مسح صورة فحص انجليزي", "مسح إعداد صورة الفحص الإنجليزية والرجوع للوضع الافتراضي."),
    ],
    "البوت المساعد": [
        (".حالة_البوت | .bot_status", "عرض حالة البوت المساعد وهل الأزرار/الإنلاين مفعلة."),
        ("/start | /help (Bot)", "قائمة استخدام تفاعلية عبر أزرار، تعمل عند ضبط BOT_TOKEN."),
        ("Inline (ai: ...)", "ذكاء سريع: ai: سؤالك"),
        ("Inline (tr: <lang> text)", "ترجمة فورية."),
        ("Inline (sum:N text)", "تلخيص لنص إلى N جملة."),
        ("Inline (short: URL)", "تقصير رابط عبر TinyURL."),
        ("Inline (url: URL)", "جلب عنوان صفحة ويب."),
    ],
}

# الإنجليزية
COMMANDS_EN = {
    "Statistics": [
        (".stats", "Show account stats: users, groups, channels, bots."),
        (".meinfo", "Advanced details: dialogs, bots, groups and channels."),
    ],
    "Storage": [
        (".enable_storage", "Create/enable storage group and initialize sections."),
        (".disable_storage", "Disable storage, unbind group and stop forwarding."),
        (".bind_storage", "Bind an existing group as storage (reply inside that group)."),
        (".storage_status", "Show storage status, group/archive IDs, and forward state."),
        (".start_forward", "Enable auto-forwarding to storage."),
        (".stop_forward", "Disable auto-forwarding to storage."),
        (".storage_test", "Send a test message to storage group."),
        (".set_archive <id> | reply", "Set archive chat by ID or by replying."),
        (".archive <days>", "Move media older than N days from storage to archive."),
        (".storage_whitelist_add <chat_id>|reply", "Add a group to forwarding whitelist."),
        (".storage_whitelist_remove <chat_id)|reply", "Remove a group from whitelist."),
        (".storage_whitelist_show", "Show current whitelist."),
        (".storage_blacklist_add <chat_id)|reply", "Add a group to forwarding blacklist (ignored)."),
        (".storage_blacklist_remove <chat_id)|reply", "Remove a group from blacklist."),
        (".storage_blacklist_show", "Show current blacklist."),
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
        (".check", "Send English check image with default or custom caption."),
        (".set_check_image ar|en <url> | reply to image", "Set/save check image (Arabic or English) from a URL or by replying to media."),
        (".clear_check_image ar|en", "Clear the configured check image and revert to default."),
    ],
    "AI": [
        (".ai <text/reply>", "Smart brief answer — example: .ai how are you → 'I’m fine!'"),
        (".translate <lang> [text/reply]", "Smart translation via Google."),
        (".detect_lang [text/reply]", "Detect text language automatically."),
        (".summarize [sentences] (reply)", "Quick summary to N sentences."),
        (".anime <description>", "Suggest anime title from a brief description."),
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
    ],
    "Check": [
        (".check", "Send English check image with default or custom caption."),
        (".set_check_image ar|en <url> | reply to image", "Set/save check image (Arabic or English) from a URL or by replying to media."),
        (".clear_check_image ar|en", "Clear the configured check image and revert to default."),
    ],
    "Assistant Bot": [
        (".bot_status | .حالة_البوت", "Show assistant-bot status and whether inline/buttons are active."),
        ("/start | /help (Bot)", "Interactive usage menu with buttons (requires BOT_TOKEN)."),
        ("Inline (ai: ...)", "Quick AI: ai: your question"),
        ("Inline (tr: <lang> text)", "Instant translation."),
        ("Inline (sum:N text)", "Summarize text to N sentences."),
        ("Inline (short: URL)", "Shorten a URL via TinyURL."),
        ("Inline (url: URL)", "Fetch page title."),
    ],
}

def build_section(title, items):
    # اجعل كل أمر قابلاً للنسخ بوضعه داخل تنسيق أحادي `code`
    # Example:
    # `.<command>`
    #   ⤷ description
    lines = [f"`{cmd}`\n  ⤷ {desc}" for cmd, desc in items]
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
    prefix = f"help:{lang}:idx:"
    for idx, title in enumerate(sections):
        row.append(Button.inline(title, data=(prefix + str(idx)).encode()))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([Button.inline("عرض الكل" if lang == "AR" else "Show All", data=f"help:{lang}:ALL".encode())])
    return rows

def build_section_buttons_by_index(index, lang, sections):
    buttons = []
    nav = []
    if index > 0:
        nav.append(Button.inline("⟵ السابق" if lang == "AR" else "⟵ Prev", data=f"help:{lang}:idx:{index-1}".encode()))
    else:
        nav.append(Button.inline("⟵ القائمة" if lang == "AR" else "⟵ Menu", data=f"help:{lang}:MENU".encode()))
    if index < len(sections) - 1:
        nav.append(Button.inline("التالي ⟶" if lang == "AR" else "Next ⟶", data=f"help:{lang}:idx:{index+1}".encode()))
    else:
        nav.append(Button.inline("⟵ القائمة" if lang == "AR" else "⟵ Menu", data=f"help:{lang}:MENU".encode()))
    buttons.append(nav)
    buttons.append([
        Button.inline("القائمة الرئيسية" if lang == "AR" else "Main Menu", data=f"help:{lang}:MENU".encode()),
        Button.inline("عرض الكل" if lang == "AR" else "Show All", data=f"help:{lang}:ALL".encode())
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
    trigger = (event.pattern_match.group(0) or "").strip()
    lang = "AR" if "help" not in trigger else "EN"
    commands = COMMANDS_AR if lang == "AR" else COMMANDS_EN
    header = HEADER_AR if lang == "AR" else HEADER_EN
    footer = FOOTER_AR if lang == "AR" else FOOTER_EN

    # Check if bot is available for inline buttons
    if bot:
        try:
            sections = list(commands.keys())
            text = build_menu_text(lang)
            buttons = build_menu_buttons(lang, sections)
            await event.edit(text, buttons=buttons)
            return
        except Exception:
            pass

    # Fallback to text-only mode if bot is None or inline fails
    sections = list(commands.keys())
    if lang == "AR":
        numbered_lines = [
            f"┏ {idx+1}. {title}\n┗ ⟶ اكتب .م{idx+1} لعرض أوامر هذا القسم"
            for idx, title in enumerate(sections)
        ]
    else:
        numbered_lines = [
            f"┏ {idx+1}. {title}\n┗ ⟶ type .c{idx+1} to view this section"
            for idx, title in enumerate(sections)
        ]
    # مسافة فارغة بين كل قسم وآخر
    numbered_header = header + "\n\n".join(numbered_lines) + "\n\n" + SEPARATOR

    await event.edit("جارٍ إعداد قائمة الأوامر..." if lang == "AR" else "Preparing commands list...")
    # عرض الأقسام فقط بدون تفاصيل الأوامر
    # العربية: استخدم .م1 لعرض أوامر القسم المحدد
    # الإنجليزية: استخدم .c1 لعرض أوامر القسم المحدد
    summary_text = numbered_header + footer
    await send_chunked(event, summary_text)

# قائمة المساعدة التفاعلية
@client.on(events.NewMessage(outgoing=True, pattern=r"\.(?:المساعدة|مساعدة|assist)$"))
async def show_help_menu(event):
    trigger = (event.pattern_match.group(0) or "").strip()
    lang = "EN" if "assist" in trigger else "AR"
    commands = COMMANDS_AR if lang == "AR" else COMMANDS_EN
    sections = list(commands.keys())
    if bot is not None:
        await bot.send_message(event.chat_id, build_menu_text(lang), buttons=build_menu_buttons(lang, sections))
        await event.delete()
    else:
        await event.edit(build_menu_text(lang))
        await event.respond("BOT_TOKEN غير مضبوط؛ سيتم عرض القائمة بدون أزرار." if lang == "AR" else "BOT_TOKEN not set; showing menu without buttons.")

# أمر عرض قسم محدد عبر .م1 و .م٢ ... إلخ (يدعم الأرقام العربية والإنجليزية)
def eastern_to_western_digits(s: str) -> str:
    trans = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
    return s.translate(trans)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.م([0-9٠-٩]+)$"))
async def show_ar_section_by_number(event):
    num_str = event.pattern_match.group(1)
    num = int(eastern_to_western_digits(num_str))
    sections = list(COMMANDS_AR.keys())
    if not (1 <= num <= len(sections)):
        await event.edit("رقم القسم غير صالح.")
        return
    idx = num - 1
    title = sections[idx]
    text = HEADER_AR + build_section(title, COMMANDS_AR.get(title, [])) + FOOTER_AR
    await send_chunked(event, text)

# أمر عرض قسم إنجليزي عبر .c1 و .c2 ... إلخ
@client.on(events.NewMessage(outgoing=True, pattern=r"\.c([0-9]+)$"))
async def show_en_section_by_number(event):
    num_str = event.pattern_match.group(1)
    num = int(num_str)
    sections = list(COMMANDS_EN.keys())
    if not (1 <= num <= len(sections)):
        await event.edit("Invalid section number.")
        return
    idx = num - 1
    title = sections[idx]
    text = HEADER_EN + build_section(title, COMMANDS_EN.get(title, [])) + FOOTER_EN
    await send_chunked(event, text)

if bot is not None:
    @bot.on(events.CallbackQuery)
    async def help_callback(event):
        data = event.data or b""
        if not data.startswith(b"help:"):
            return
        parts = data.decode().split(":")
        # help:<lang>:(MENU|ALL|idx:N)
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
            except Exception:
                await event.answer("فهرس غير صالح." if lang == "AR" else "Invalid index.", alert=True)
                return
            if not (0 <= index < len(sections)):
                await event.answer("خارج النطاق." if lang == "AR" else "Out of range.", alert=True)
                return
            title = sections[index]
            header = HEADER_AR if lang == "AR" else HEADER_EN
            footer = FOOTER_AR if lang == "AR" else FOOTER_EN
            text = header + build_section(title, commands.get(title, [])) + footer
            await event.edit(text, buttons=build_section_buttons_by_index(index, lang, sections))
            await event.answer(("تم فتح قسم: " + title) if lang == "AR" else ("Opened section: " + title))lethon import events, Button
from core.client import client
from core.bot_client import bot

# Arabic header/footer
HEADER_AR = (
    "╔════════════════════════════════════════════════╗\n"
    "║   𓆩 قائمة أوامر FLEX – مميّزة وسهلة الاستخدام 𓆪   ║\n"
    "╚════════════════════════════════════════════════╝\n"
)
FOOTER_AR = "\n— مستند الأوامر • FLEX —\n"

# English header/footer
HEADER_EN = (
    "╔════════════════════════════════════════════════╗\n"
    "║   𓆩 FLEX Commands – Elegant & Easy to Use 𓆪   ║\n"
    "╚════════════════════════════════════════════════╝\n"
)
FOOTER_EN = "\n— Command Reference • FLEX —\n"

SEPARATOR = "\n┄┄┄┄┄┄┄┄┄┄┄\n"

# Arabic commands
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
        (".سجل_إداري", "عرض آخر 25 عملية إدارية مع السبب إن وُجد."),
        (".سجل_إداري_بحث <نص>", "بحث في السجل حسب الهدف/الإجراء/السبب."),
        (".مسح_سجل_إداري", "مسح كامل السجل الإداري."),
        (".تصدير_سجل_إداري", "تصدير السجل إلى ملف وإعطاء رابط تحميل."),
    ],
}
SECTIONS_AR = list(COMMANDS_AR.keys())

# English commands
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
    "Fake Interactions": [
        (".typing [seconds]", "Show typing without sending."),
        (".upload_photo [seconds]", "Show uploading a photo."),
        (".upload_file [seconds]", "Show uploading a file."),
        (".upload_video [seconds]", "Show uploading a video."),
        (".upload_audio [seconds]", "Show uploading an audio."),
        (".record_video [seconds]", "Show recording a video."),
        (".record_audio [seconds]", "Show recording an audio."),
        (".choose_sticker [seconds]", "Show choosing a sticker."),
        (".game_play [seconds]", "Show playing a game."),
    ],
    "Media & Tools": [
        (".youtube <query>", "Find the first matching YouTube video."),
        (".sticker", "Create a sticker from an image/sticker (reply)."),
        (".sticker_info", "Get sticker pack info."),
        (".tiktok <link>", "Download TikTok video without watermark."),
        (".check", "Send English check image with default or custom caption."),
        (".set_check_image ar|en <url> | reply to image", "Set/save check image (Arabic or English) from a URL or by replying to media."),
        (".clear_check_image ar|en", "Clear the configured check image and revert to default."),
    ],
    "AI": [
        (".ai <text/reply>", "Smart short reply. Example: .ai how are you → 'Fine, thanks!'."),
        (".translate <lang> [text/reply]", "Smart translation via Google."),
        (".detect_lang [text/reply]", "Detect language."),
        (".summarize [n] (reply)", "Quick summarization to n sentences."),
    ],
    "Hunting (Usernames)": [
        (".hunt <pattern>", "Start username hunting based on a pattern."),
        (".hunt_status", "Show hunting status and attempts."),
        (".hunt_stop", "Stop current hunting process."),
    ],
    "Monitoring": [
        (".watch <@user>", "Watch for user name/photo/bio changes."),
        (".unwatch <@user>", "Stop watching the user."),
    ],
    "Profile": [
        (".time_name_on", "Enable time in first name."),
        (".time_name_off", "Disable and remove time from name."),
        (".name (text)", "Set first name (with current time)."),
        (".impersonate", "Impersonate replied user (name/bio/photo)."),
        (".restore", "Restore original name/bio/photo."),
    ],
    "Private Protection & Warnings": [
        (".private_protect", "Toggle private protection from bad words."),
        (".accept", "Accept a user (reply) to skip warnings."),
        (".unaccept", "Remove acceptance (reply)."),
        (".clear_warnings", "Clear all warnings (reply)."),
        (".warnings", "Show your warning count."),
        (".set_warning_text", "Change warning message (reply)."),
        (".show_warning_text", "Show current warning message."),
        (".set_warning_limit <n>", "Set max warnings."),
        (".banned_list", "Show banned users list."),
        (".clear_banned", "Clear all banned users."),
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

def build_section(header, title, items):
    lines = [f"• {cmd}\n  ⤷ {desc}" for cmd, desc in items]
    return f"{header}【 {title} 】\n" + "\n".join(lines)

def build_help_text_ar():
    parts = []
    for title, items in COMMANDS_AR.items():
        parts.append(build_section(HEADER_AR, title, items))
        parts.append(SEPARATOR)
    parts.append(FOOTER_AR)
    return "\n".join(parts)

def build_help_text_en():
    parts = []
    for title, items in COMMANDS_EN.items():
        parts.append(build_section(HEADER_EN, title, items))
        parts.append(SEPARATOR)
    parts.append(FOOTER_EN)
    return "\n".join(parts)

def build_menu_text_ar():
    return HEADER_AR + "اختر قسمًا من الأزرار أدناه لعرض أوامره مع الشرح.\n" + FOOTER_AR

def build_menu_text_en():
    return HEADER_EN + "Pick a section from the buttons below to view its commands and descriptions.\n" + FOOTER_EN

def build_buttons(prefix, sections):
    rows = []
    row = []
    for idx, title in enumerate(sections):
        row.append(Button.inline(title, data=f"{prefix}:idx:{idx}".encode()))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([Button.inline("Show All" if prefix.endswith("en") else "عرض الكل", data=f"{prefix}:ALL".encode())])
    return rows

def build_section_buttons(prefix, index, sections):
    buttons = []
    nav = []
    if index > 0:
        nav.append(Button.inline("⟵ Prev" if prefix.endswith("en") else "⟵ السابق", data=f"{prefix}:idx:{index-1}".encode()))
    else:
        nav.append(Button.inline("⟵ Menu" if prefix.endswith("en") else "⟵ القائمة", data=f"{prefix}:MENU".encode()))
    if index < len(sections) - 1:
        nav.append(Button.inline("Next ⟶" if prefix.endswith("en") else "التالي ⟶", data=f"{prefix}:idx:{index+1}".encode()))
    else:
        nav.append(Button.inline("⟵ Menu" if prefix.endswith("en") else "⟵ القائمة", data=f"{prefix}:MENU".encode()))
    buttons.append(nav)
    buttons.append([
        Button.inline("Main Menu" if prefix.endswith("en") else "القائمة الرئيسية", data=f"{prefix}:MENU".encode()),
        Button.inline("Show All" if prefix.endswith("en") else "عرض الكل", data=f"{prefix}:ALL".encode()),
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

# Arabic textual help
@client.on(events.NewMessage(outgoing=True, pattern=r"\.(?:الاوامر|اوامر)$"))
async def show_commands_ar(event):
    await event.edit("جارٍ إعداد قائمة الأوامر...")
