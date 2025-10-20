from telethon import events
from core.client import client

# Lightweight bilingual bridge:
# Intercepts common English commands, rewrites them to the equivalent Arabic commands,
# and edits the message so that existing Arabic handlers trigger without code duplication.

ALIASES = {
    # Help
    r'^\.commands$': '.الاوامر',
    r'^\.help$': '.الاوامر',
    r'^\.help (.+)$': '.اوامر \\1',
    r'^\.search cmd (.+)$': '.بحث امر \\1',

    # Storage
    r'^\.enable storage$': '.تفعيل التخزين',
    r'^\.disable storage$': '.تعطيل التخزين',

    # Auto replies
    r'^\.add reply \+ (.+) \+ (.+)$': '.اضف رد + \\1 + \\2',
    r'^\.replies$': '.الردود',
    r'^\.enable here$': '.تفعيل هنا',
    r'^\.disable here$': '.تعطيل هنا',

    # AFK / custom
    r'^\.afk on$': '.تشغيل الرد',
    r'^\.afk off$': '.تعطيل الرد',
    r'^\.custom on$': '.المخصص تشغيل',
    r'^\.reply (.+)$': '.رد \\1',
    r'^\.delete reply$': '.حذف رد',
    r'^\.set template$': '.كليشة الرد',
    r'^\.allow$': '.سماح',
    r'^\.disallow$': '.الغاء السماح',

    # Profile
    r'^\.time name on$': '.تفعيل الاسم الوقتي',
    r'^\.time name off$': '.تعطيل الاسم الوقتي',
    r'^\.name \((.+)\)$': '.الاسم (\\1)',
    r'^\.impersonate$': '.انتحال',
    r'^\.restore$': '.ارجاع',

    # Timers / publish
    r'^\.repeat (\d+) (\d+)(.*)$': '.تكرار \\1 \\2\\3',
    r'^\.pub (\d+) (\d+)(.*)$': '.نشر \\1 \\2\\3',
    r'^\.stop publishing$': '.ايقاف النشر التلقائي',

    # Protection
    r'^\.protect pm$': '.حماية الخاص',
    r'^\.accept$': '.قبول',
    r'^\.unaccept$': '.الغاء القبول',
    r'^\.clear warns$': '.مسح التحذيرات',
    r'^\.warns$': '.التحذيرات',
    r'^\.set warn template$': '.تعيين كليشة التحذير',
    r'^\.show template$': '.عرض كليشة',
    r'^\.set warn limit (\d+)$': '.عدد التحذيرات \\1',
    r'^\.banned$': '.المحظورين',
    r'^\.clear banned$': '.مسح المحظورين',

    # Games
    r'^\.dart(?: (.+))?$': '.سهم \\1',
    r'^\.dice(?: (.+))?$': '.نرد \\1',
    r'^\.basket(?: (.+))?$': '.سله \\1',
    r'^\.ball(?: (.+))?$': '.كرة \\1',
    r'^\.slot(?: (.+))?$': '.حظ \\1',
    r'^\.gym$': '.gym',

    # Shortcuts/memes
    r'^\.shortcut \+ (\S+)$': '.اختصار + \\1',
    r'^\.del shortcut \+ (\S+)$': '.حذف اختصار + \\1',
    r'^\.shortcuts$': '.الاختصارات',
    r'^\.meme (\S+) (.+)$': '.ميمز \\1 \\2',
    r'^\.memes$': '.قائمة الميمز',
    r'^\.remove (\S+)$': 'ازالة \\1',
    r'^\.clear_memes$': '.ازالة_البصمات',

    # User tools
    r'^\.list channels$': '.قائمه جميع القنوات',
    r'^\.list admin channels$': '.قائمه القنوات المشرف عليها',
    r'^\.my channels$': '.قائمه قنواتي',
    r'^\.list groups$': '.قائمه جميع المجموعات',
    r'^\.groups I admin$': '.قائمه مجموعات اديرها',
    r'^\.my groups$': '.قائمه كروباتي',
    r'^\.inspect group(?: (.*))?$': '.كشف المجموعة \\1',

    # Media
    r'^\.youtube (.+)$': '.يوتيوب \\1',
    r'^\.sticker$': '.ملصق',
    r'^\.sticker info$': '.معلومات الملصق',
    r'^\.tiktok (.+)$': '.تك \\1',

    # Hunter
    r'^\.hunt (.+)$': '.صيد \\1',
    r'^\.stop hunt$': '.ايقاف الصيد',
    r'^\.hunt status$': '.حالة الصيد',

    # Monitor
    r'^\.watch (.+)$': '.مراقبة \\1',
    r'^\.unwatch (.+)$': '.ايقاف_المراقبة \\1',

    # Admin
    r'^\.ban$': '.حظر',
    r'^\.kick$': '.طرد',
    r'^\.restrict$': '.تقييد',
    r'^\.unban$': '.الغاء الحظر',
    r'^\.unrestrict$': '.الغاء التقييد',

    # Panel (text mode)
    r'^\.panel$': '.لوحة',
    r'^\.panel sections$': '.لوحة اقسام',
    r'^\.panel status$': '.لوحة حالة',
    r'^\.panel toggle$': '.لوحة تبديل',
    r'^\.panel section (.+)$': '.لوحة قسم \\1',
    r'^\.panel toggle (afk|custom|protect|storage)$': '.لوحة تبديل \\1',
}

import re

@client.on(events.NewMessage(outgoing=True))  # from self
async def i18n_bridge(event):
    text = event.raw_text or ""
    for pattern, replacement in ALIASES.items():
        m = re.match(pattern, text, flags=re.IGNORECASE)
        if m:
            new = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
            await event.edit(new.strip())
            break