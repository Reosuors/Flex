from telethon import events
from core.client import client

# English -> Arabic command alias mapping
ALIASES = {
    # Statistics
    "stats": "احصائياتي",
    "meinfo": "معلوماتي",
    "dashboard": "لوحة",

    # Health check
    "check": "فحص",

    # Storage
    "enable_storage": "تفعيل التخزين",
    "disable_storage": "تعطيل التخزين",
    "set_archive": "تعيين_ارشيف",
    "archive": "أرشفة",

    # Auto Replies
    "add_reply": "اضف رد",
    "replies": "الردود",
    "enable_here": "تفعيل هنا",
    "disable_here": "تعطيل هنا",
    "set_reply_priority": "أولوية الرد",

    # AFK & Custom Replies
    "afk_on": "تشغيل الرد",
    "custom_on": "المخصص تشغيل",
    "afk_off": "تعطيل الرد",
    "reply_template": "كليشة الرد",
    "reply": "رد",
    "del_reply": "حذف رد",
    "allow": "سماح",
    "disallow": "الغاء السماح",
    "schedule_afk": "جدولة_الغياب",
    "unschedule_afk": "الغاء_الجدولة",

    # Games
    "dart": "سهم",
    "dice": "نرد",
    "basket": "سله",
    "ball": "كرة",
    "slot": "حظ",
    "truthdare": "احكام",
    "dare": "حكم",
    "truth": "حقيقة",
    "gym": "gym",  # same

    # Media & Tools
    "youtube": "يوتيوب",
    "sticker": "ملصق",
    "sticker_info": "معلومات الملصق",
    "tiktok": "تك",
    "compress_image": "ضغط_صوره",

    # AI
    "translate": "ترجم",
    "detect_lang": "كشف_لغة",
    "summarize": "تلخيص",
    # .ai exists natively; no alias needed

    # Hunting
    "hunt": "صيد",
    "hunt_status": "حالة الصيد",
    "hunt_stop": "ايقاف الصيد",

    # Monitoring
    "watch": "مراقبة",
    "unwatch": "ايقاف_المراقبة",
    "weekly_report": "تقرير_اسبوعي",

    # Profile
    "time_name_on": "تفعيل الاسم الوقتي",
    "time_name_off": "تعطيل الاسم الوقتي",
    "name": "الاسم",
    "impersonate": "انتحال",
    "restore": "ارجاع",
    "badge": "شارة",
    "clear_badge": "ازالة_شارة",

    # Private Protection & Warnings
    "private_protect": "حماية الخاص",
    "accept": "قبول",
    "unaccept": "الغاء القبول",
    "clear_warnings": "مسح التحذيرات",
    "my_warnings": "التحذيرات",
    "set_warning_template": "تعيين كليشة التحذير",
    "show_template": "عرض كليشة",
    "set_max_warnings": "عدد التحذيرات",
    "banned_list": "المحظورين",
    "clear_banned": "مسح المحظورين",
    "add_bad_word": "اضافة_كلمة_سيئة",
    "remove_bad_word": "ازالة_كلمة_سيئة",
    "list_bad_words": "قائمة_الكلمات_السيئة",

    # Shortcuts & Memes
    "shortcut": "اختصار",
    "del_shortcut": "حذف اختصار",
    "shortcuts": "الاختصارات",
    "memes": "ميمز",
    "memes_save": "ميمز حفظ",
    "memes_get": "ميمز جلب",
    "memes_show": "ميمز عرض",
    "memes_list": "قائمة الميمز",
    "remove": "ازالة",
    "memes_clear": "ازالة_البصمات",
    "tag_meme": "وسم_ميمز",
    "search_memes": "بحث_ميمز",

    # Auto Publishing
    "repeat": "تكرار",
    "rep": "تك",
    "publish": "نشر",
    "stop_auto_publish": "ايقاف النشر التلقائي",
    "save_publish_template": "حفظ_قالب_نشر",
    "list_publish_templates": "قوالب_النشر",
    "delete_publish_template": "حذف_قالب_نشر",
    "publish_with_template": "نشر_بقالب",

    # Channels & Groups Tools
    "list_all_channels": "قائمه جميع القنوات",
    "list_admin_channels": "قائمه القنوات المشرف عليها",
    "list_my_channels": "قائمه قنواتي",
    "list_all_groups": "قائمه جميع المجموعات",
    "list_admin_groups": "قائمه مجموعات اديرها",
    "list_my_groups": "قائمه كروباتي",
    "inspect_group": "كشف المجموعة",
    "my_rights": "صلاحياتي",

    # Administration
    "ban": "حظر",
    "kick": "طرد",
    "restrict": "تقييد",
    "unban": "الغاء الحظر",
    "unrestrict": "الغاء التقييد",
    "admin_log": "سجل_إداري",
    "admin_log_search": "سجل_إداري_بحث",
    "admin_log_clear": "مسح_سجل_إداري",
    "admin_log_export": "تصدير_سجل_إداري",
    "auto_badge": "شارة_تلقائية",
    "setup_activity_badge": "إعداد_شارة_نشاط",
    "anime": "انمي",

    # Fake interactions
    "typing": "يكتب",
    "upload_photo": "يرفع_صورة",
    "upload_file": "يرفع_ملف",
    "upload_video": "يرفع_فيديو",
    "upload_audio": "يرفع_صوت",
    "record_video": "يسجل_فيديو",
    "record_audio": "يسجل_صوت",
    "choose_sticker": "اختيار_ملصق",
    "game_play": "يلعب",
}

# Do not rewrite these (they drive bilingual help system)
EXCLUDE = {"help", "assist"}

def extract_command(text: str) -> tuple[str, str]:
    """
    Returns (command_name_without_dot, rest_of_text_including_space),
    or ("", "") if no dot-command.
    """
    t = (text or "").strip()
    if not t.startswith("."):
        return "", ""
    first = t.split(None, 1)[0]  # like ".stats" or ".memes"
    cmd = first[1:]  # remove dot
    rest = t[len(first):]  # includes leading space if any
    return cmd, rest

@client.on(events.NewMessage(outgoing=True))
async def english_alias_rewriter(event):
    raw = event.raw_text or ""
    cmd, rest = extract_command(raw)
    if not cmd:
        return
    # exact command name match only
    key = cmd.lower()
    if key in EXCLUDE:
        return
    alias = ALIASES.get(key)
    if not alias:
        return
    # Build the new Arabic command text, keeping parameters intact
    new_text = f".{alias}{rest}"
    # Preserve reply context
    reply_to = None
    if event.is_reply:
        try:
            reply_msg = await event.get_reply_message()
            reply_to = reply_msg.id
        except Exception:
            reply_to = None
    # Replace command by deleting original and sending new one
    try:
        await event.delete()
    except Exception:
        pass
    await client.send_message(event.chat_id, new_text, reply_to=reply_to)