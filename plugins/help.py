from telethon import events
from core.client import client

# Arabic catalog
CATEGORIES = {
    "الاساسية": [
        (".احصائياتي", "احصائيات حسابك"),
        (".معلوماتي", "معلومات عامة عن الحساب"),
        (".الاوامر / .اوامر <قسم>", "عرض الأقسام أو أوامر قسم"),
        (".بحث امر <كلمة>", "البحث عن أمر"),
    ],
    "التخزين": [
        (".تفعيل التخزين", "إنشاء/تفعيل كروب التخزين"),
        (".تعطيل التخزين", "تعطيل التخزين"),
    ],
    "الردود": [
        (".اضف رد + الكلمة + الرد", "إضافة رد تلقائي"),
        (".الردود", "عرض الردود"),
        (".تفعيل هنا", "تفعيل الردود في المجموعة"),
        (".تعطيل هنا", "تعطيل الردود في المجموعة"),
    ],
    "AFK والمخصص": [
        (".تشغيل الرد", "تفعيل الرد التلقائي"),
        (".تعطيل الرد", "تعطيل الرد التلقائي"),
        (".المخصص تشغيل", "تفعيل الردود المخصصة"),
        (".رد <النص> (بالرد)", "إضافة رد مخصص"),
        (".حذف رد (بالرد)", "حذف الرد المخصص"),
        (".كليشة الرد (بالرد)", "تعيين رسالة كليشة"),
        (".سماح / .الغاء السماح", "سماح/إلغاء السماح للخاص"),
    ],
    "الملف الشخصي": [
        (".الاسم (الاسم)", "تغيير الاسم مع الوقت"),
        (".تفعيل الاسم الوقتي / .تعطيل الاسم الوقتي", "إضافة/إزالة الوقت من الاسم"),
        (".انتحال (بالرد) / .ارجاع", "انتحال/استرجاع"),
    ],
    "النشر والمؤقتات": [
        (".تكرار <ثواني> <عدد> [نص]", "نشر متكرر"),
        (".تك <ثواني> <عدد> [نص] / .نشر ...", "اختصار/نشر"),
        (".ايقاف النشر التلقائي", "إيقاف كل النشر"),
    ],
    "الحماية والتحذير": [
        (".حماية الخاص", "تفعيل/تعطيل فلتر الخاص"),
        (".قبول / .الغاء القبول (بالرد)", "إدارة القبول"),
        (".مسح التحذيرات (بالرد)", "مسح تحذيرات شخص"),
        (".التحذيرات", "عرض تحذيراتك"),
        (".تعيين كليشة التحذير / .عرض كليشة", "تعديل/عرض الكليشة"),
        (".عدد التحذيرات <n>", "ضبط الحد"),
        (".المحظورين / .مسح المحظورين", "عرض/مسح المحظورين"),
    ],
    "العاب": [
        (".سهم [1..6]", "لعبة السهم"),
        (".نرد [1..6]", "لعبة النرد"),
        (".سله [1..5] / .كرة [1..5]", "سلة/قدم"),
        (".حظ [1..64] / .gym", "حظ/انميشن"),
    ],
    "اختصارات/ميمز": [
        (".اختصار + KEY (بالرد)", "حفظ اختصار"),
        (".حذف اختصار + KEY / .الاختصارات", "حذف/عرض"),
        (".ميمز KEY URL / .قائمة الميمز / ازالة KEY / .ازالة_البصمات", "إدارة الميمز"),
    ],
    "أدوات المستخدم": [
        (".قائمه جميع القنوات | القنوات المشرف عليها | قنواتي", "قنوات"),
        (".قائمه جميع المجموعات | مجموعات اديرها | كروباتي", "مجموعات"),
        (".كشف المجموعة [اختياري]", "معلومات مجموعة/قناة"),
    ],
    "ميديا": [
        (".يوتيوب <نص>", "بحث يوتيوب"),
        (".ملصق (بالرد على صورة) / .معلومات الملصق (بالرد)", "ملصقات"),
        (".تك <رابط تيك توك>", "تنزيل تيك توك"),
    ],
    "صيد اليوزرات": [
        (".صيد <نمط/نوع> / .ايقاف الصيد / .حالة الصيد", "إدارة الصيد"),
    ],
    "مراقبة": [
        (".مراقبة <@user> / .ايقاف_المراقبة <@user>", "إدارة المراقبة"),
    ],
    "إدارة": [
        (".حظر / .طرد / .تقييد / .الغاء الحظر / .الغاء التقييد", "أوامر إدارية"),
    ],
}

# English catalog
EN_CATEGORIES = {
    "Basics": [
        (".myStats", "Show your account statistics"),
        (".meInfo", "Show basic account info"),
        (".help / .help <section>", "Show sections or commands in a section"),
        (".search cmd <text>", "Search a command"),
    ],
    "Storage": [
        (".enable storage", "Create/enable storage group"),
        (".disable storage", "Disable storage group"),
    ],
    "Replies": [
        (".add reply + key + value", "Add auto-reply"),
        (".replies", "List replies"),
        (".enable here / .disable here", "Enable/disable in group"),
    ],
    "AFK & Custom": [
        (".afk on / .afk off", "Enable/disable AFK"),
        (".custom on", "Enable custom replies"),
        (".reply <text> (reply)", "Add custom reply"),
        (".delete reply (reply)", "Delete custom reply"),
        (".set template (reply)", "Set template message"),
        (".allow / .disallow", "Allow/disallow this private chat"),
    ],
    "Profile": [
        (".name (text)", "Change name with time"),
        (".time name on / .time name off", "Toggle time in name"),
        (".impersonate (reply) / .restore", "Impersonate/restore"),
    ],
    "Publish & Timers": [
        (".repeat <sec> <count> [text]", "Repeated publishing"),
        (".pub <sec> <count> [text]", "Alias for repeat"),
        (".stop publishing", "Stop all publishing"),
    ],
    "Protection & Warnings": [
        (".protect pm", "Toggle private protection"),
        (".accept (reply) / .unaccept (reply)", "Manage acceptance"),
        (".clear warns (reply)", "Clear warns"),
        (".warns", "Show your warns"),
        (".set warn template (reply) / .show template", "Edit/show template"),
        (".set warn limit <n>", "Set warn limit"),
        (".banned / .clear banned", "List/clear banned"),
    ],
    "Games": [
        (".dart [1..6] / .dice [1..6]", "Games"),
        (".basket [1..5] / .ball [1..5]", "Games"),
        (".slot [1..64] / .gym", "Games"),
    ],
    "Shortcuts/Memes": [
        (".shortcut + KEY (reply)", "Save shortcut"),
        (".del shortcut + KEY / .shortcuts", "Delete/list"),
        (".meme KEY URL / .memes / remove KEY / .clear_memes", "Manage memes"),
    ],
    "User Tools": [
        (".list channels / .list admin channels / .my channels", "Channels"),
        (".list groups / .groups I admin / .my groups", "Groups"),
        (".inspect group [optional]", "Group/channel info"),
    ],
    "Media": [
        (".youtube <text>", "YouTube search"),
        (".sticker (reply) / .sticker info (reply)", "Stickers"),
        (".tiktok <url>", "Download TikTok"),
    ],
    "Username Hunter": [
        (".hunt <pattern> / .stop hunt / .hunt status", "Hunter"),
    ],
    "Monitoring": [
        (".watch <@user> / .unwatch <@user>", "Monitoring"),
    ],
    "Admin": [
        (".ban / .kick / .restrict / .unban / .unrestrict", "Admin tools"),
    ],
}

SECTION_ALIASES = {
    "احصائيات": "الاساسية",
    "التخزين": "التخزين",
    "ردود": "الردود",
    "afk": "AFK والمخصص",
    "المخصص": "AFK والمخصص",
    "بروفايل": "الملف الشخصي",
    "الاسم": "الملف الشخصي",
    "نشر": "النشر والمؤقتات",
    "تايمر": "النشر والمؤقتات",
    "حماية": "الحماية والتحذير",
    "تحذير": "الحماية والتحذير",
    "العاب": "العاب",
    "اختصارات": "اختصارات/ميمز",
    "ميمز": "اختصارات/ميمز",
    "مستخدم": "أدوات المستخدم",
    "ميديا": "ميديا",
    "صيد": "صيد اليوزرات",
    "مراقبة": "مراقبة",
    "ادارة": "إدارة",
}

def build_categories_text_ar():
    lines = ["**قائمة الأوامر — الأقسام المتاحة:**\n"]
    for i, name in enumerate(CATEGORIES.keys(), start=1):
        lines.append(f"{i}. {name}")
    lines.append("\nاستخدم: `.اوامر <القسم>` لعرض أوامر قسم محدد.\nمثال: `.اوامر الاساسية`")
    return "\n".join(lines)

def build_section_text_ar(section_name):
    pairs = CATEGORIES.get(section_name)
    if not pairs:
        return "⎙ القسم غير معروف. اكتب `.الاوامر` لعرض الأقسام."
    header = f"**أوامر قسم: {section_name}**\n"
    body = "\n".join(f"- `{cmd}` — {desc}" for cmd, desc in pairs)
    return f"{header}\n{body}"

def build_categories_text_en():
    lines = ["**Command List — Available Sections:**\n"]
    for i, name in enumerate(EN_CATEGORIES.keys(), start=1):
        lines.append(f"{i}. {name}")
    lines.append("\nUse: `.help <section>` to show commands of a section.\nExample: `.help Basics`")
    return "\n".join(lines)

def build_section_text_en(section_name):
    pairs = EN_CATEGORIES.get(section_name)
    if not pairs:
        return "Section not found. Type `.help` to list available sections."
    header = f"**Section: {section_name}**\n"
    body = "\n".join(f"- `{cmd}` — {desc}" for cmd, desc in pairs)
    return f"{header}\n{body}"

def search_commands_ar(q):
    q = q.strip()
    res = []
    for cat, pairs in CATEGORIES.items():
        for cmd, desc in pairs:
            if q in cmd or q in desc:
                res.append((cat, cmd, desc))
    if not res:
        return f"⎙ لا توجد نتائج للبحث: {q}"
    lines = [f"**نتائج البحث عن:** {q}\n"]
    for cat, cmd, desc in res[:50]:
        lines.append(f"[{cat}] `{cmd}` — {desc}")
    if len(res) > 50:
        lines.append(f"\n… المزيد: {len(res)-50} نتيجة.")
    return "\n".join(lines)

def search_commands_en(q):
    q = q.strip().lower()
    res = []
    for cat, pairs in EN_CATEGORIES.items():
        for cmd, desc in pairs:
            if q in cmd.lower() or q in desc.lower():
                res.append((cat, cmd, desc))
    if not res:
        return f"No results for: {q}"
    lines = [f"**Search results for:** {q}\n"]
    for cat, cmd, desc in res[:50]:
        lines.append(f"[{cat}] `{cmd}` — {desc}")
    if len(res) > 50:
        lines.append(f"\n… more: {len(res)-50} results.")
    return "\n".join(lines)

# Arabic handlers
@client.on(events.NewMessage(from_users='me', pattern=r'^\.الاوامر))
async def show_categories_ar(event):
    await event.edit(build_categories_text_ar())

@client.on(events.NewMessage(from_users='me', pattern=r'^\.اوامر (.+)))
async def show_section_ar(event):
    name = event.pattern_match.group(1).strip()
    name = SECTION_ALIASES.get(name, name)
    await event.edit(build_section_text_ar(name))

@client.on(events.NewMessage(from_users='me', pattern=r'^\.بحث امر (.+)))
async def search_ar(event):
    q = event.pattern_match.group(1)
    await event.edit(search_commands_ar(q))

# English handlers
@client.on(events.NewMessage(from_users='me', pattern=r'^\.help))
async def show_categories_en(event):
    await event.edit(build_categories_text_en())

@client.on(events.NewMessage(from_users='me', pattern=r'^\.help (.+)))
async def show_section_en(event):
    name = event.pattern_match.group(1).strip()
    await event.edit(build_section_text_en(name))

@client.on(events.NewMessage(from_users='me', pattern=r'^\.search cmd (.+)))
async def search_en(event):
    q = event.pattern_match.group(1)
    await event.edit(search_commands_en(q))