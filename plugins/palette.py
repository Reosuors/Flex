import os
from telethon import events, Button
from core.client import client

# Import internal states to present/toggle quickly
from plugins.help import CATEGORIES, format_commands_for
from plugins.afk import afk_mode as _afk_mode_ref, custom_replies_enabled as _custom_enabled_ref, custom_replies as _custom_replies_ref
from plugins.protection import protection_data, save_protection
from plugins.storage import _load_group_id, _ensure_storage_group, GROUP_ID_FILE
from plugins.auto_reply import DATA as AUTO_REPLY_DATA
from plugins.timers_publish import active_publishing_tasks
from plugins.lang import t, get_lang

def _status_snapshot():
    # Read dynamic states
    afk = _afk_mode_ref
    custom = _custom_enabled_ref
    custom_count = len(_custom_replies_ref or {})
    protection = bool(protection_data.get("enabled", False))
    storage_id = _load_group_id()
    replies_enabled_groups = len(AUTO_REPLY_DATA.get("enabled_groups", []))
    replies_count = len(AUTO_REPLY_DATA.get("responses", {}))
    publishing_chats = len(active_publishing_tasks or {})
    return {
        "AFK": "مفعل" if afk else "معطل",
        "الردود المخصصة": f"{'مفعلة' if custom else 'معطلة'} ({custom_count} رد)",
        "حماية الخاص": "مفعلة" if protection else "معطلة",
        "مجموعة التخزين": f"موجودة ({storage_id})" if storage_id else "غير مفعلة",
        "الردود في مجموعات": f"{replies_enabled_groups} مجموعة / {replies_count} رد",
        "نشر تلقائي": f"{publishing_chats} محادثة نشطة",
    }

def _main_menu_text(lang):
    return t("panel_main", lang)

def _categories_menu():
    rows = []
    row = []
    for cat in CATEGORIES.keys():
        label = cat[:20]
        row.append(Button.inline(label, data=("palette:cat:" + cat).encode("utf-8")))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([Button.inline("رجوع ◀️", data=b"palette:home")])
    return "**لوحة التحكم — الأقسام**\nاختر قسمًا للاطلاع على أوامره:", rows

def _toggles_menu(lang):
    snap = _status_snapshot()
    text = t("panel_toggles_title", lang) + "\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    rows = [
        [
            Button.inline(f"AFK: {'تعطيل' if 'مفعل' in snap['AFK'] else 'تشغيل'}", data=b"palette:toggle:afk"),
            Button.inline(f"مخصص: {'تعطيل' if 'مفعلة' in snap['الردود المخصصة'] else 'تشغيل'}", data=b"palette:toggle:custom"),
        ],
        [
            Button.inline(f"حماية: {'تعطيل' if 'مفعلة' in snap['حماية الخاص'] else 'تشغيل'}", data=b"palette:toggle:protect"),
            Button.inline(f"التخزين: {'تعطيل' if 'موجودة' in snap['مجموعة التخزين'] else 'تفعيل'}", data=b"palette:toggle:storage"),
        ],
        [Button.inline("رجوع ◀️", data=b"palette:home")]
    ]
    return text, rows

@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحةs
from telethon import events, Button
from core.client import client

# Import internal states to present/toggle quickly
from plugins.help import CATEGORIES, format_commands_for
from plugins.afk import afk_mode as _afk_mode_ref, custom_replies_enabled as _custom_enabled_ref, custom_replies as _custom_replies_ref
from plugins.protection import protection_data, save_protection
from plugins.storage import _load_group_id, _ensure_storage_group, GROUP_ID_FILE
from plugins.auto_reply import DATA as AUTO_REPLY_DATA
from plugins.timers_publish import active_publishing_tasks


def _status_snapshot():
    # Read dynamic states
    afk = _afk_mode_ref
    custom = _custom_enabled_ref
    custom_count = len(_custom_replies_ref or {})
    protection = bool(protection_data.get("enabled", False))
    warn_max = int(protection_data.get("warnings", {}).get("max_warnings", 0)) if isinstance(protection_data.get("warnings"), dict) else None
    storage_id = _load_group_id()
    replies_enabled_groups = len(AUTO_REPLY_DATA.get("enabled_groups", []))
    replies_count = len(AUTO_REPLY_DATA.get("responses", {}))
    publishing_chats = len(active_publishing_tasks or {})
    return {
        "AFK": "مفعل" if afk else "معطل",
        "الردود المخصصة": f"{'مفعلة' if custom else 'معطلة'} ({custom_count} رد)",
        "حماية الخاص": "مفعلة" if protection else "معطلة",
        "مجموعة التخزين": f"موجودة ({storage_id})" if storage_id else "غير مفعلة",
        "الردود في مجموعات": f"{replies_enabled_groups} مجموعة / {replies_count} رد",
        "نشر تلقائي": f"{publishing_chats} محادثة نشطة",
    }


def _main_menu():
    return (
        "**لوحة التحكم — القائمة الرئيسية**\n"
        "اختر من الأزرار أدناه:\n"
        "• الأقسام: تصفح الأوامر حسب القسم.\n"
        "• الحالة: نظرة سريعة على وضع الميزات.\n"
        "• التبديل السريع: تفعيل/تعطيل ميزات شائعة."
    ), [
        [Button.inline("الأقسام 📚", data=b"palette:cats"), Button.inline("الحالة 📊", data=b"palette:status")],
        [Button.inline("التبديل السريع ⚙️", data=b"palette:toggles")]
    ]


def _categories_menu():
    rows = []
    row = []
    for cat in CATEGORIES.keys():
        label = cat[:20]
        row.append(Button.inline(label, data=("palette:cat:" + cat).encode("utf-8")))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([Button.inline("رجوع ◀️", data=b"palette:home")])
    return "**لوحة التحكم — الأقسام**\nاختر قسمًا للاطلاع على أوامره:", rows


def _toggles_menu():
    snap = _status_snapshot()
    text = "**لوحة التحكم — التبديل السريع**\n"
    text += "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    rows = [
        [
            Button.inline(f"AFK: {'تعطيل' if 'مفعل' in snap['AFK'] else 'تشغيل'}", data=b"palette:toggle:afk"),
            Button.inline(f"مخصص: {'تعطيل' if 'مفعلة' in snap['الردود المخصصة'] else 'تشغيل'}", data=b"palette:toggle:custom"),
        ],
        [
            Button.inline(f"حماية: {'تعطيل' if 'مفعلة' in snap['حماية الخاص'] else 'تشغيل'}", data=b"palette:toggle:protect"),
            Button.inline(f"التخزين: {'تعطيل' if 'موجودة' in snap['مجموعة التخزين'] else 'تفعيل'}", data=b"palette:toggle:storage"),
        ],
        [Button.inline("رجوع ◀️", data=b"palette:home")]
    ]
    return text, rows


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة))
async def palette_main(event):
    me = await client.get_me()
    if getattr(me, "bot", False):
        text, buttons = _main_menu()
        await event.reply(text, buttons=buttons)
    else:
        # User accounts لا تستقبل CallbackQuery. نعرض نسخة نصية مع أوامر مباشرة.
        msg = (
            "**لوحة التحكم (وضع المستخدم)**\n"
            "- الأقسام: اكتب `.لوحة اقسام`\n"
            "- الحالة: اكتب `.لوحة حالة`\n"
            "- التبديل السريع: اكتب `.لوحة تبديل`\n"
            "- أو لعرض قسم محدد: `.لوحة قسم <اسم القسم>`\n"
            "- للتبديل المباشر: `.لوحة تبديل afk|custom|protect|storage`"
        )
        await event.reply(msg)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة اقسام))
async def palette_text_categories(event):
    cats = "**الأقسام المتاحة:**\n" + "\n".join([f"- {c}" for c in CATEGORIES.keys()])
    cats += "\n\nاستخدم: `.لوحة قسم <اسم القسم>`"
    await event.edit(cats)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة حالة))
async def palette_text_status(event):
    snap = _status_snapshot()
    text = "**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    await event.edit(text)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة تبديل))
async def palette_text_toggles(event):
    snap = _status_snapshot()
    text = "**لوحة التحكم — التبديل السريع**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    text += "\n\nاستخدم: `.لوحة تبديل afk|custom|protect|storage`"
    await event.edit(text)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة قسم (.+)))
async def palette_text_category(event):
    cat = event.pattern_match.group(1).strip()
    await event.edit(format_commands_for(cat))


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة تبديل (afk|custom|protect|storage)))
async def palette_text_toggle(event):
    toggle_what = event.pattern_match.group(1)
    msg = ""
    try:
        if toggle_what == "afk":
            from plugins import afk as _afk
            _afk.afk_mode = not _afk.afk_mode
            msg = f"تم {'تشغيل' if _afk.afk_mode else 'تعطيل'} AFK."
        elif toggle_what == "custom":
            from plugins import afk as _afk
            _afk.custom_replies_enabled = not _afk.custom_replies_enabled
            msg = f"تم {'تشغيل' if _afk.custom_replies_enabled else 'تعطيل'} الردود المخصصة."
        elif toggle_what == "protect":
            protection_data['enabled'] = not protection_data.get('enabled', False)
            save_protection()
            msg = f"تم {'تفعيل' if protection_data['enabled'] else 'تعطيل'} حماية الخاص."
        elif toggle_what == "storage":
            gid = _load_group_id()
            if gid and os.path.exists(GROUP_ID_FILE):
                os.remove(GROUP_ID_FILE)
                msg = "تم تعطيل التخزين وإزالة ربط المجموعة."
            else:
                await _ensure_storage_group(event)
                msg = "تم تفعيل التخزين وإنشاء/ربط المجموعة."
    except Exception as e:
        msg = f"خطأ أثناء التبديل: {e}"

    snap = _status_snapshot()
    text = msg + "\n\n" + ("**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()]))
    await event.edit(text)


@client.on(events.CallbackQuery))
async def palette_callbacks(event):
    # وضع البوت فقط: يستقبل CallbackQuery
    me = await client.get_me()
    if not getattr(me, "bot", False):
        return
    if not event.data or not event.data.startswith(b"palette:"):
        return
    parts = event.data.decode("utf-8", errors="ignore").split(":")
    if len(parts) < 2:
        return
    action = parts[1]

    if action == "home":
        text, buttons = _main_menu()
        return await event.edit(text, buttons=buttons)

    if action == "cats":
        text, buttons = _categories_menu()
        return await event.edit(text, buttons=buttons)

    if action == "cat" and len(parts) >= 3:
        cat_name = ":".join(parts[2:])
        try:
            text = format_commands_for(cat_name)
        except Exception:
            text = f"تعذر تحميل أوامر القسم: {cat_name}"
        buttons = [[Button.inline("رجوع ◀️", data=b"palette:cats")]]
        return await event.edit(text, buttons=buttons)

    if action == "status":
        snap = _status_snapshot()
        text = "**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
        buttons = [[Button.inline("رجوع ◀️", data=b"palette:home")]]
        return await event.edit(text, buttons=buttons)

    if action == "toggles":
        text, buttons = _toggles_menu()
        return await event.edit(text, buttons=buttons)

    if action == "toggle" and len(parts) >= 3:
        toggle_what = parts[2]
        msg = ""
        try:
            if toggle_what == "afk":
                from plugins import afk as _afk
                _afk.afk_mode = not _afk.afk_mode
                msg = f"تم {'تشغيل' if _afk.afk_mode else 'تعطيل'} AFK."
            elif toggle_what == "custom":
                from plugins import afk as _afk
                _afk.custom_replies_enabled = not _afk.custom_replies_enabled
                msg = f"تم {'تشغيل' if _afk.custom_replies_enabled else 'تعطيل'} الردود المخصصة."
            elif toggle_what == "protect":
                protection_data['enabled'] = not protection_data.get('enabled', False)
                save_protection()
                msg = f"تم {'تفعيل' if protection_data['enabled'] else 'تعطيل'} حماية الخاص."
            elif toggle_what == "storage":
                gid = _load_group_id()
                if gid:
                    if os.path.exists(GROUP_ID_FILE):
                        os.remove(GROUP_ID_FILE)
                    msg = "تم تعطيل التخزين وإزالة ربط المجموعة."
                else:
                    await _ensure_storage_group(event)
                    msg = "تم تفعيل التخزين وإنشاء/ربط المجموعة."
        except Exception as e:
            msg = f"خطأ أثناء التبديل: {e}"

        text, buttons = _toggles_menu()
        text = f"{msg}\n\n" + text
        return await event.edit(text, buttons=buttons)))
async def palette_main(event):
    lang = get_lang(getattr(event.message, "id", 0))
    me = await client.get_me()
    if getattr(me, "bot", False):
        text = _main_menu_text(lang)
        buttons = [
            [Button.inline("الأقسام 📚", data=b"palette:cats"), Button.inline("الحالة 📊", data=b"palette:status")],
            [Button.inline("التبديل السريع ⚙️", data=b"palette:toggles")]
        ]
        await event.reply(text, buttons=buttons)
    else:
        await event.reply(t("panel_text_user", lang))

@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة اقسامs
from telethon import events, Button
from core.client import client

# Import internal states to present/toggle quickly
from plugins.help import CATEGORIES, format_commands_for
from plugins.afk import afk_mode as _afk_mode_ref, custom_replies_enabled as _custom_enabled_ref, custom_replies as _custom_replies_ref
from plugins.protection import protection_data, save_protection
from plugins.storage import _load_group_id, _ensure_storage_group, GROUP_ID_FILE
from plugins.auto_reply import DATA as AUTO_REPLY_DATA
from plugins.timers_publish import active_publishing_tasks


def _status_snapshot():
    # Read dynamic states
    afk = _afk_mode_ref
    custom = _custom_enabled_ref
    custom_count = len(_custom_replies_ref or {})
    protection = bool(protection_data.get("enabled", False))
    warn_max = int(protection_data.get("warnings", {}).get("max_warnings", 0)) if isinstance(protection_data.get("warnings"), dict) else None
    storage_id = _load_group_id()
    replies_enabled_groups = len(AUTO_REPLY_DATA.get("enabled_groups", []))
    replies_count = len(AUTO_REPLY_DATA.get("responses", {}))
    publishing_chats = len(active_publishing_tasks or {})
    return {
        "AFK": "مفعل" if afk else "معطل",
        "الردود المخصصة": f"{'مفعلة' if custom else 'معطلة'} ({custom_count} رد)",
        "حماية الخاص": "مفعلة" if protection else "معطلة",
        "مجموعة التخزين": f"موجودة ({storage_id})" if storage_id else "غير مفعلة",
        "الردود في مجموعات": f"{replies_enabled_groups} مجموعة / {replies_count} رد",
        "نشر تلقائي": f"{publishing_chats} محادثة نشطة",
    }


def _main_menu():
    return (
        "**لوحة التحكم — القائمة الرئيسية**\n"
        "اختر من الأزرار أدناه:\n"
        "• الأقسام: تصفح الأوامر حسب القسم.\n"
        "• الحالة: نظرة سريعة على وضع الميزات.\n"
        "• التبديل السريع: تفعيل/تعطيل ميزات شائعة."
    ), [
        [Button.inline("الأقسام 📚", data=b"palette:cats"), Button.inline("الحالة 📊", data=b"palette:status")],
        [Button.inline("التبديل السريع ⚙️", data=b"palette:toggles")]
    ]


def _categories_menu():
    rows = []
    row = []
    for cat in CATEGORIES.keys():
        label = cat[:20]
        row.append(Button.inline(label, data=("palette:cat:" + cat).encode("utf-8")))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([Button.inline("رجوع ◀️", data=b"palette:home")])
    return "**لوحة التحكم — الأقسام**\nاختر قسمًا للاطلاع على أوامره:", rows


def _toggles_menu():
    snap = _status_snapshot()
    text = "**لوحة التحكم — التبديل السريع**\n"
    text += "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    rows = [
        [
            Button.inline(f"AFK: {'تعطيل' if 'مفعل' in snap['AFK'] else 'تشغيل'}", data=b"palette:toggle:afk"),
            Button.inline(f"مخصص: {'تعطيل' if 'مفعلة' in snap['الردود المخصصة'] else 'تشغيل'}", data=b"palette:toggle:custom"),
        ],
        [
            Button.inline(f"حماية: {'تعطيل' if 'مفعلة' in snap['حماية الخاص'] else 'تشغيل'}", data=b"palette:toggle:protect"),
            Button.inline(f"التخزين: {'تعطيل' if 'موجودة' in snap['مجموعة التخزين'] else 'تفعيل'}", data=b"palette:toggle:storage"),
        ],
        [Button.inline("رجوع ◀️", data=b"palette:home")]
    ]
    return text, rows


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة))
async def palette_main(event):
    me = await client.get_me()
    if getattr(me, "bot", False):
        text, buttons = _main_menu()
        await event.reply(text, buttons=buttons)
    else:
        # User accounts لا تستقبل CallbackQuery. نعرض نسخة نصية مع أوامر مباشرة.
        msg = (
            "**لوحة التحكم (وضع المستخدم)**\n"
            "- الأقسام: اكتب `.لوحة اقسام`\n"
            "- الحالة: اكتب `.لوحة حالة`\n"
            "- التبديل السريع: اكتب `.لوحة تبديل`\n"
            "- أو لعرض قسم محدد: `.لوحة قسم <اسم القسم>`\n"
            "- للتبديل المباشر: `.لوحة تبديل afk|custom|protect|storage`"
        )
        await event.reply(msg)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة اقسام))
async def palette_text_categories(event):
    cats = "**الأقسام المتاحة:**\n" + "\n".join([f"- {c}" for c in CATEGORIES.keys()])
    cats += "\n\nاستخدم: `.لوحة قسم <اسم القسم>`"
    await event.edit(cats)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة حالة))
async def palette_text_status(event):
    snap = _status_snapshot()
    text = "**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    await event.edit(text)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة تبديل))
async def palette_text_toggles(event):
    snap = _status_snapshot()
    text = "**لوحة التحكم — التبديل السريع**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    text += "\n\nاستخدم: `.لوحة تبديل afk|custom|protect|storage`"
    await event.edit(text)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة قسم (.+)))
async def palette_text_category(event):
    cat = event.pattern_match.group(1).strip()
    await event.edit(format_commands_for(cat))


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة تبديل (afk|custom|protect|storage)))
async def palette_text_toggle(event):
    toggle_what = event.pattern_match.group(1)
    msg = ""
    try:
        if toggle_what == "afk":
            from plugins import afk as _afk
            _afk.afk_mode = not _afk.afk_mode
            msg = f"تم {'تشغيل' if _afk.afk_mode else 'تعطيل'} AFK."
        elif toggle_what == "custom":
            from plugins import afk as _afk
            _afk.custom_replies_enabled = not _afk.custom_replies_enabled
            msg = f"تم {'تشغيل' if _afk.custom_replies_enabled else 'تعطيل'} الردود المخصصة."
        elif toggle_what == "protect":
            protection_data['enabled'] = not protection_data.get('enabled', False)
            save_protection()
            msg = f"تم {'تفعيل' if protection_data['enabled'] else 'تعطيل'} حماية الخاص."
        elif toggle_what == "storage":
            gid = _load_group_id()
            if gid and os.path.exists(GROUP_ID_FILE):
                os.remove(GROUP_ID_FILE)
                msg = "تم تعطيل التخزين وإزالة ربط المجموعة."
            else:
                await _ensure_storage_group(event)
                msg = "تم تفعيل التخزين وإنشاء/ربط المجموعة."
    except Exception as e:
        msg = f"خطأ أثناء التبديل: {e}"

    snap = _status_snapshot()
    text = msg + "\n\n" + ("**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()]))
    await event.edit(text)


@client.on(events.CallbackQuery))
async def palette_callbacks(event):
    # وضع البوت فقط: يستقبل CallbackQuery
    me = await client.get_me()
    if not getattr(me, "bot", False):
        return
    if not event.data or not event.data.startswith(b"palette:"):
        return
    parts = event.data.decode("utf-8", errors="ignore").split(":")
    if len(parts) < 2:
        return
    action = parts[1]

    if action == "home":
        text, buttons = _main_menu()
        return await event.edit(text, buttons=buttons)

    if action == "cats":
        text, buttons = _categories_menu()
        return await event.edit(text, buttons=buttons)

    if action == "cat" and len(parts) >= 3:
        cat_name = ":".join(parts[2:])
        try:
            text = format_commands_for(cat_name)
        except Exception:
            text = f"تعذر تحميل أوامر القسم: {cat_name}"
        buttons = [[Button.inline("رجوع ◀️", data=b"palette:cats")]]
        return await event.edit(text, buttons=buttons)

    if action == "status":
        snap = _status_snapshot()
        text = "**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
        buttons = [[Button.inline("رجوع ◀️", data=b"palette:home")]]
        return await event.edit(text, buttons=buttons)

    if action == "toggles":
        text, buttons = _toggles_menu()
        return await event.edit(text, buttons=buttons)

    if action == "toggle" and len(parts) >= 3:
        toggle_what = parts[2]
        msg = ""
        try:
            if toggle_what == "afk":
                from plugins import afk as _afk
                _afk.afk_mode = not _afk.afk_mode
                msg = f"تم {'تشغيل' if _afk.afk_mode else 'تعطيل'} AFK."
            elif toggle_what == "custom":
                from plugins import afk as _afk
                _afk.custom_replies_enabled = not _afk.custom_replies_enabled
                msg = f"تم {'تشغيل' if _afk.custom_replies_enabled else 'تعطيل'} الردود المخصصة."
            elif toggle_what == "protect":
                protection_data['enabled'] = not protection_data.get('enabled', False)
                save_protection()
                msg = f"تم {'تفعيل' if protection_data['enabled'] else 'تعطيل'} حماية الخاص."
            elif toggle_what == "storage":
                gid = _load_group_id()
                if gid:
                    if os.path.exists(GROUP_ID_FILE):
                        os.remove(GROUP_ID_FILE)
                    msg = "تم تعطيل التخزين وإزالة ربط المجموعة."
                else:
                    await _ensure_storage_group(event)
                    msg = "تم تفعيل التخزين وإنشاء/ربط المجموعة."
        except Exception as e:
            msg = f"خطأ أثناء التبديل: {e}"

        text, buttons = _toggles_menu()
        text = f"{msg}\n\n" + text
        return await event.edit(text, buttons=buttons)))
async def palette_text_categories(event):
    cats = "**الأقسام المتاحة:**\n" + "\n".join([f"- {c}" for c in CATEGORIES.keys()])
    cats += "\n\nاستخدم: `.لوحة قسم <اسم القسم>`"
    await event.edit(cats)

@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة حالةs
from telethon import events, Button
from core.client import client

# Import internal states to present/toggle quickly
from plugins.help import CATEGORIES, format_commands_for
from plugins.afk import afk_mode as _afk_mode_ref, custom_replies_enabled as _custom_enabled_ref, custom_replies as _custom_replies_ref
from plugins.protection import protection_data, save_protection
from plugins.storage import _load_group_id, _ensure_storage_group, GROUP_ID_FILE
from plugins.auto_reply import DATA as AUTO_REPLY_DATA
from plugins.timers_publish import active_publishing_tasks


def _status_snapshot():
    # Read dynamic states
    afk = _afk_mode_ref
    custom = _custom_enabled_ref
    custom_count = len(_custom_replies_ref or {})
    protection = bool(protection_data.get("enabled", False))
    warn_max = int(protection_data.get("warnings", {}).get("max_warnings", 0)) if isinstance(protection_data.get("warnings"), dict) else None
    storage_id = _load_group_id()
    replies_enabled_groups = len(AUTO_REPLY_DATA.get("enabled_groups", []))
    replies_count = len(AUTO_REPLY_DATA.get("responses", {}))
    publishing_chats = len(active_publishing_tasks or {})
    return {
        "AFK": "مفعل" if afk else "معطل",
        "الردود المخصصة": f"{'مفعلة' if custom else 'معطلة'} ({custom_count} رد)",
        "حماية الخاص": "مفعلة" if protection else "معطلة",
        "مجموعة التخزين": f"موجودة ({storage_id})" if storage_id else "غير مفعلة",
        "الردود في مجموعات": f"{replies_enabled_groups} مجموعة / {replies_count} رد",
        "نشر تلقائي": f"{publishing_chats} محادثة نشطة",
    }


def _main_menu():
    return (
        "**لوحة التحكم — القائمة الرئيسية**\n"
        "اختر من الأزرار أدناه:\n"
        "• الأقسام: تصفح الأوامر حسب القسم.\n"
        "• الحالة: نظرة سريعة على وضع الميزات.\n"
        "• التبديل السريع: تفعيل/تعطيل ميزات شائعة."
    ), [
        [Button.inline("الأقسام 📚", data=b"palette:cats"), Button.inline("الحالة 📊", data=b"palette:status")],
        [Button.inline("التبديل السريع ⚙️", data=b"palette:toggles")]
    ]


def _categories_menu():
    rows = []
    row = []
    for cat in CATEGORIES.keys():
        label = cat[:20]
        row.append(Button.inline(label, data=("palette:cat:" + cat).encode("utf-8")))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([Button.inline("رجوع ◀️", data=b"palette:home")])
    return "**لوحة التحكم — الأقسام**\nاختر قسمًا للاطلاع على أوامره:", rows


def _toggles_menu():
    snap = _status_snapshot()
    text = "**لوحة التحكم — التبديل السريع**\n"
    text += "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    rows = [
        [
            Button.inline(f"AFK: {'تعطيل' if 'مفعل' in snap['AFK'] else 'تشغيل'}", data=b"palette:toggle:afk"),
            Button.inline(f"مخصص: {'تعطيل' if 'مفعلة' in snap['الردود المخصصة'] else 'تشغيل'}", data=b"palette:toggle:custom"),
        ],
        [
            Button.inline(f"حماية: {'تعطيل' if 'مفعلة' in snap['حماية الخاص'] else 'تشغيل'}", data=b"palette:toggle:protect"),
            Button.inline(f"التخزين: {'تعطيل' if 'موجودة' in snap['مجموعة التخزين'] else 'تفعيل'}", data=b"palette:toggle:storage"),
        ],
        [Button.inline("رجوع ◀️", data=b"palette:home")]
    ]
    return text, rows


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة))
async def palette_main(event):
    me = await client.get_me()
    if getattr(me, "bot", False):
        text, buttons = _main_menu()
        await event.reply(text, buttons=buttons)
    else:
        # User accounts لا تستقبل CallbackQuery. نعرض نسخة نصية مع أوامر مباشرة.
        msg = (
            "**لوحة التحكم (وضع المستخدم)**\n"
            "- الأقسام: اكتب `.لوحة اقسام`\n"
            "- الحالة: اكتب `.لوحة حالة`\n"
            "- التبديل السريع: اكتب `.لوحة تبديل`\n"
            "- أو لعرض قسم محدد: `.لوحة قسم <اسم القسم>`\n"
            "- للتبديل المباشر: `.لوحة تبديل afk|custom|protect|storage`"
        )
        await event.reply(msg)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة اقسام))
async def palette_text_categories(event):
    cats = "**الأقسام المتاحة:**\n" + "\n".join([f"- {c}" for c in CATEGORIES.keys()])
    cats += "\n\nاستخدم: `.لوحة قسم <اسم القسم>`"
    await event.edit(cats)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة حالة))
async def palette_text_status(event):
    snap = _status_snapshot()
    text = "**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    await event.edit(text)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة تبديل))
async def palette_text_toggles(event):
    snap = _status_snapshot()
    text = "**لوحة التحكم — التبديل السريع**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    text += "\n\nاستخدم: `.لوحة تبديل afk|custom|protect|storage`"
    await event.edit(text)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة قسم (.+)))
async def palette_text_category(event):
    cat = event.pattern_match.group(1).strip()
    await event.edit(format_commands_for(cat))


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة تبديل (afk|custom|protect|storage)))
async def palette_text_toggle(event):
    toggle_what = event.pattern_match.group(1)
    msg = ""
    try:
        if toggle_what == "afk":
            from plugins import afk as _afk
            _afk.afk_mode = not _afk.afk_mode
            msg = f"تم {'تشغيل' if _afk.afk_mode else 'تعطيل'} AFK."
        elif toggle_what == "custom":
            from plugins import afk as _afk
            _afk.custom_replies_enabled = not _afk.custom_replies_enabled
            msg = f"تم {'تشغيل' if _afk.custom_replies_enabled else 'تعطيل'} الردود المخصصة."
        elif toggle_what == "protect":
            protection_data['enabled'] = not protection_data.get('enabled', False)
            save_protection()
            msg = f"تم {'تفعيل' if protection_data['enabled'] else 'تعطيل'} حماية الخاص."
        elif toggle_what == "storage":
            gid = _load_group_id()
            if gid and os.path.exists(GROUP_ID_FILE):
                os.remove(GROUP_ID_FILE)
                msg = "تم تعطيل التخزين وإزالة ربط المجموعة."
            else:
                await _ensure_storage_group(event)
                msg = "تم تفعيل التخزين وإنشاء/ربط المجموعة."
    except Exception as e:
        msg = f"خطأ أثناء التبديل: {e}"

    snap = _status_snapshot()
    text = msg + "\n\n" + ("**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()]))
    await event.edit(text)


@client.on(events.CallbackQuery))
async def palette_callbacks(event):
    # وضع البوت فقط: يستقبل CallbackQuery
    me = await client.get_me()
    if not getattr(me, "bot", False):
        return
    if not event.data or not event.data.startswith(b"palette:"):
        return
    parts = event.data.decode("utf-8", errors="ignore").split(":")
    if len(parts) < 2:
        return
    action = parts[1]

    if action == "home":
        text, buttons = _main_menu()
        return await event.edit(text, buttons=buttons)

    if action == "cats":
        text, buttons = _categories_menu()
        return await event.edit(text, buttons=buttons)

    if action == "cat" and len(parts) >= 3:
        cat_name = ":".join(parts[2:])
        try:
            text = format_commands_for(cat_name)
        except Exception:
            text = f"تعذر تحميل أوامر القسم: {cat_name}"
        buttons = [[Button.inline("رجوع ◀️", data=b"palette:cats")]]
        return await event.edit(text, buttons=buttons)

    if action == "status":
        snap = _status_snapshot()
        text = "**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
        buttons = [[Button.inline("رجوع ◀️", data=b"palette:home")]]
        return await event.edit(text, buttons=buttons)

    if action == "toggles":
        text, buttons = _toggles_menu()
        return await event.edit(text, buttons=buttons)

    if action == "toggle" and len(parts) >= 3:
        toggle_what = parts[2]
        msg = ""
        try:
            if toggle_what == "afk":
                from plugins import afk as _afk
                _afk.afk_mode = not _afk.afk_mode
                msg = f"تم {'تشغيل' if _afk.afk_mode else 'تعطيل'} AFK."
            elif toggle_what == "custom":
                from plugins import afk as _afk
                _afk.custom_replies_enabled = not _afk.custom_replies_enabled
                msg = f"تم {'تشغيل' if _afk.custom_replies_enabled else 'تعطيل'} الردود المخصصة."
            elif toggle_what == "protect":
                protection_data['enabled'] = not protection_data.get('enabled', False)
                save_protection()
                msg = f"تم {'تفعيل' if protection_data['enabled'] else 'تعطيل'} حماية الخاص."
            elif toggle_what == "storage":
                gid = _load_group_id()
                if gid:
                    if os.path.exists(GROUP_ID_FILE):
                        os.remove(GROUP_ID_FILE)
                    msg = "تم تعطيل التخزين وإزالة ربط المجموعة."
                else:
                    await _ensure_storage_group(event)
                    msg = "تم تفعيل التخزين وإنشاء/ربط المجموعة."
        except Exception as e:
            msg = f"خطأ أثناء التبديل: {e}"

        text, buttons = _toggles_menu()
        text = f"{msg}\n\n" + text
        return await event.edit(text, buttons=buttons)))
async def palette_text_status(event):
    lang = get_lang(getattr(event.message, "id", 0))
    snap = _status_snapshot()
    text = t("panel_status_title", lang) + "\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    await event.edit(text)

@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة تبديلs
from telethon import events, Button
from core.client import client

# Import internal states to present/toggle quickly
from plugins.help import CATEGORIES, format_commands_for
from plugins.afk import afk_mode as _afk_mode_ref, custom_replies_enabled as _custom_enabled_ref, custom_replies as _custom_replies_ref
from plugins.protection import protection_data, save_protection
from plugins.storage import _load_group_id, _ensure_storage_group, GROUP_ID_FILE
from plugins.auto_reply import DATA as AUTO_REPLY_DATA
from plugins.timers_publish import active_publishing_tasks


def _status_snapshot():
    # Read dynamic states
    afk = _afk_mode_ref
    custom = _custom_enabled_ref
    custom_count = len(_custom_replies_ref or {})
    protection = bool(protection_data.get("enabled", False))
    warn_max = int(protection_data.get("warnings", {}).get("max_warnings", 0)) if isinstance(protection_data.get("warnings"), dict) else None
    storage_id = _load_group_id()
    replies_enabled_groups = len(AUTO_REPLY_DATA.get("enabled_groups", []))
    replies_count = len(AUTO_REPLY_DATA.get("responses", {}))
    publishing_chats = len(active_publishing_tasks or {})
    return {
        "AFK": "مفعل" if afk else "معطل",
        "الردود المخصصة": f"{'مفعلة' if custom else 'معطلة'} ({custom_count} رد)",
        "حماية الخاص": "مفعلة" if protection else "معطلة",
        "مجموعة التخزين": f"موجودة ({storage_id})" if storage_id else "غير مفعلة",
        "الردود في مجموعات": f"{replies_enabled_groups} مجموعة / {replies_count} رد",
        "نشر تلقائي": f"{publishing_chats} محادثة نشطة",
    }


def _main_menu():
    return (
        "**لوحة التحكم — القائمة الرئيسية**\n"
        "اختر من الأزرار أدناه:\n"
        "• الأقسام: تصفح الأوامر حسب القسم.\n"
        "• الحالة: نظرة سريعة على وضع الميزات.\n"
        "• التبديل السريع: تفعيل/تعطيل ميزات شائعة."
    ), [
        [Button.inline("الأقسام 📚", data=b"palette:cats"), Button.inline("الحالة 📊", data=b"palette:status")],
        [Button.inline("التبديل السريع ⚙️", data=b"palette:toggles")]
    ]


def _categories_menu():
    rows = []
    row = []
    for cat in CATEGORIES.keys():
        label = cat[:20]
        row.append(Button.inline(label, data=("palette:cat:" + cat).encode("utf-8")))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([Button.inline("رجوع ◀️", data=b"palette:home")])
    return "**لوحة التحكم — الأقسام**\nاختر قسمًا للاطلاع على أوامره:", rows


def _toggles_menu():
    snap = _status_snapshot()
    text = "**لوحة التحكم — التبديل السريع**\n"
    text += "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    rows = [
        [
            Button.inline(f"AFK: {'تعطيل' if 'مفعل' in snap['AFK'] else 'تشغيل'}", data=b"palette:toggle:afk"),
            Button.inline(f"مخصص: {'تعطيل' if 'مفعلة' in snap['الردود المخصصة'] else 'تشغيل'}", data=b"palette:toggle:custom"),
        ],
        [
            Button.inline(f"حماية: {'تعطيل' if 'مفعلة' in snap['حماية الخاص'] else 'تشغيل'}", data=b"palette:toggle:protect"),
            Button.inline(f"التخزين: {'تعطيل' if 'موجودة' in snap['مجموعة التخزين'] else 'تفعيل'}", data=b"palette:toggle:storage"),
        ],
        [Button.inline("رجوع ◀️", data=b"palette:home")]
    ]
    return text, rows


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة))
async def palette_main(event):
    me = await client.get_me()
    if getattr(me, "bot", False):
        text, buttons = _main_menu()
        await event.reply(text, buttons=buttons)
    else:
        # User accounts لا تستقبل CallbackQuery. نعرض نسخة نصية مع أوامر مباشرة.
        msg = (
            "**لوحة التحكم (وضع المستخدم)**\n"
            "- الأقسام: اكتب `.لوحة اقسام`\n"
            "- الحالة: اكتب `.لوحة حالة`\n"
            "- التبديل السريع: اكتب `.لوحة تبديل`\n"
            "- أو لعرض قسم محدد: `.لوحة قسم <اسم القسم>`\n"
            "- للتبديل المباشر: `.لوحة تبديل afk|custom|protect|storage`"
        )
        await event.reply(msg)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة اقسام))
async def palette_text_categories(event):
    cats = "**الأقسام المتاحة:**\n" + "\n".join([f"- {c}" for c in CATEGORIES.keys()])
    cats += "\n\nاستخدم: `.لوحة قسم <اسم القسم>`"
    await event.edit(cats)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة حالة))
async def palette_text_status(event):
    snap = _status_snapshot()
    text = "**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    await event.edit(text)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة تبديل))
async def palette_text_toggles(event):
    snap = _status_snapshot()
    text = "**لوحة التحكم — التبديل السريع**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    text += "\n\nاستخدم: `.لوحة تبديل afk|custom|protect|storage`"
    await event.edit(text)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة قسم (.+)))
async def palette_text_category(event):
    cat = event.pattern_match.group(1).strip()
    await event.edit(format_commands_for(cat))


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة تبديل (afk|custom|protect|storage)))
async def palette_text_toggle(event):
    toggle_what = event.pattern_match.group(1)
    msg = ""
    try:
        if toggle_what == "afk":
            from plugins import afk as _afk
            _afk.afk_mode = not _afk.afk_mode
            msg = f"تم {'تشغيل' if _afk.afk_mode else 'تعطيل'} AFK."
        elif toggle_what == "custom":
            from plugins import afk as _afk
            _afk.custom_replies_enabled = not _afk.custom_replies_enabled
            msg = f"تم {'تشغيل' if _afk.custom_replies_enabled else 'تعطيل'} الردود المخصصة."
        elif toggle_what == "protect":
            protection_data['enabled'] = not protection_data.get('enabled', False)
            save_protection()
            msg = f"تم {'تفعيل' if protection_data['enabled'] else 'تعطيل'} حماية الخاص."
        elif toggle_what == "storage":
            gid = _load_group_id()
            if gid and os.path.exists(GROUP_ID_FILE):
                os.remove(GROUP_ID_FILE)
                msg = "تم تعطيل التخزين وإزالة ربط المجموعة."
            else:
                await _ensure_storage_group(event)
                msg = "تم تفعيل التخزين وإنشاء/ربط المجموعة."
    except Exception as e:
        msg = f"خطأ أثناء التبديل: {e}"

    snap = _status_snapshot()
    text = msg + "\n\n" + ("**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()]))
    await event.edit(text)


@client.on(events.CallbackQuery))
async def palette_callbacks(event):
    # وضع البوت فقط: يستقبل CallbackQuery
    me = await client.get_me()
    if not getattr(me, "bot", False):
        return
    if not event.data or not event.data.startswith(b"palette:"):
        return
    parts = event.data.decode("utf-8", errors="ignore").split(":")
    if len(parts) < 2:
        return
    action = parts[1]

    if action == "home":
        text, buttons = _main_menu()
        return await event.edit(text, buttons=buttons)

    if action == "cats":
        text, buttons = _categories_menu()
        return await event.edit(text, buttons=buttons)

    if action == "cat" and len(parts) >= 3:
        cat_name = ":".join(parts[2:])
        try:
            text = format_commands_for(cat_name)
        except Exception:
            text = f"تعذر تحميل أوامر القسم: {cat_name}"
        buttons = [[Button.inline("رجوع ◀️", data=b"palette:cats")]]
        return await event.edit(text, buttons=buttons)

    if action == "status":
        snap = _status_snapshot()
        text = "**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
        buttons = [[Button.inline("رجوع ◀️", data=b"palette:home")]]
        return await event.edit(text, buttons=buttons)

    if action == "toggles":
        text, buttons = _toggles_menu()
        return await event.edit(text, buttons=buttons)

    if action == "toggle" and len(parts) >= 3:
        toggle_what = parts[2]
        msg = ""
        try:
            if toggle_what == "afk":
                from plugins import afk as _afk
                _afk.afk_mode = not _afk.afk_mode
                msg = f"تم {'تشغيل' if _afk.afk_mode else 'تعطيل'} AFK."
            elif toggle_what == "custom":
                from plugins import afk as _afk
                _afk.custom_replies_enabled = not _afk.custom_replies_enabled
                msg = f"تم {'تشغيل' if _afk.custom_replies_enabled else 'تعطيل'} الردود المخصصة."
            elif toggle_what == "protect":
                protection_data['enabled'] = not protection_data.get('enabled', False)
                save_protection()
                msg = f"تم {'تفعيل' if protection_data['enabled'] else 'تعطيل'} حماية الخاص."
            elif toggle_what == "storage":
                gid = _load_group_id()
                if gid:
                    if os.path.exists(GROUP_ID_FILE):
                        os.remove(GROUP_ID_FILE)
                    msg = "تم تعطيل التخزين وإزالة ربط المجموعة."
                else:
                    await _ensure_storage_group(event)
                    msg = "تم تفعيل التخزين وإنشاء/ربط المجموعة."
        except Exception as e:
            msg = f"خطأ أثناء التبديل: {e}"

        text, buttons = _toggles_menu()
        text = f"{msg}\n\n" + text
        return await event.edit(text, buttons=buttons)))
async def palette_text_toggles(event):
    lang = get_lang(getattr(event.message, "id", 0))
    snap = _status_snapshot()
    text = t("panel_toggles_title", lang) + "\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    text += "\n\nاستخدم: `.لوحة تبديل afk|custom|protect|storage`"
    await event.edit(text)

@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة قسم (.+)s
from telethon import events, Button
from core.client import client

# Import internal states to present/toggle quickly
from plugins.help import CATEGORIES, format_commands_for
from plugins.afk import afk_mode as _afk_mode_ref, custom_replies_enabled as _custom_enabled_ref, custom_replies as _custom_replies_ref
from plugins.protection import protection_data, save_protection
from plugins.storage import _load_group_id, _ensure_storage_group, GROUP_ID_FILE
from plugins.auto_reply import DATA as AUTO_REPLY_DATA
from plugins.timers_publish import active_publishing_tasks


def _status_snapshot():
    # Read dynamic states
    afk = _afk_mode_ref
    custom = _custom_enabled_ref
    custom_count = len(_custom_replies_ref or {})
    protection = bool(protection_data.get("enabled", False))
    warn_max = int(protection_data.get("warnings", {}).get("max_warnings", 0)) if isinstance(protection_data.get("warnings"), dict) else None
    storage_id = _load_group_id()
    replies_enabled_groups = len(AUTO_REPLY_DATA.get("enabled_groups", []))
    replies_count = len(AUTO_REPLY_DATA.get("responses", {}))
    publishing_chats = len(active_publishing_tasks or {})
    return {
        "AFK": "مفعل" if afk else "معطل",
        "الردود المخصصة": f"{'مفعلة' if custom else 'معطلة'} ({custom_count} رد)",
        "حماية الخاص": "مفعلة" if protection else "معطلة",
        "مجموعة التخزين": f"موجودة ({storage_id})" if storage_id else "غير مفعلة",
        "الردود في مجموعات": f"{replies_enabled_groups} مجموعة / {replies_count} رد",
        "نشر تلقائي": f"{publishing_chats} محادثة نشطة",
    }


def _main_menu():
    return (
        "**لوحة التحكم — القائمة الرئيسية**\n"
        "اختر من الأزرار أدناه:\n"
        "• الأقسام: تصفح الأوامر حسب القسم.\n"
        "• الحالة: نظرة سريعة على وضع الميزات.\n"
        "• التبديل السريع: تفعيل/تعطيل ميزات شائعة."
    ), [
        [Button.inline("الأقسام 📚", data=b"palette:cats"), Button.inline("الحالة 📊", data=b"palette:status")],
        [Button.inline("التبديل السريع ⚙️", data=b"palette:toggles")]
    ]


def _categories_menu():
    rows = []
    row = []
    for cat in CATEGORIES.keys():
        label = cat[:20]
        row.append(Button.inline(label, data=("palette:cat:" + cat).encode("utf-8")))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([Button.inline("رجوع ◀️", data=b"palette:home")])
    return "**لوحة التحكم — الأقسام**\nاختر قسمًا للاطلاع على أوامره:", rows


def _toggles_menu():
    snap = _status_snapshot()
    text = "**لوحة التحكم — التبديل السريع**\n"
    text += "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    rows = [
        [
            Button.inline(f"AFK: {'تعطيل' if 'مفعل' in snap['AFK'] else 'تشغيل'}", data=b"palette:toggle:afk"),
            Button.inline(f"مخصص: {'تعطيل' if 'مفعلة' in snap['الردود المخصصة'] else 'تشغيل'}", data=b"palette:toggle:custom"),
        ],
        [
            Button.inline(f"حماية: {'تعطيل' if 'مفعلة' in snap['حماية الخاص'] else 'تشغيل'}", data=b"palette:toggle:protect"),
            Button.inline(f"التخزين: {'تعطيل' if 'موجودة' in snap['مجموعة التخزين'] else 'تفعيل'}", data=b"palette:toggle:storage"),
        ],
        [Button.inline("رجوع ◀️", data=b"palette:home")]
    ]
    return text, rows


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة))
async def palette_main(event):
    me = await client.get_me()
    if getattr(me, "bot", False):
        text, buttons = _main_menu()
        await event.reply(text, buttons=buttons)
    else:
        # User accounts لا تستقبل CallbackQuery. نعرض نسخة نصية مع أوامر مباشرة.
        msg = (
            "**لوحة التحكم (وضع المستخدم)**\n"
            "- الأقسام: اكتب `.لوحة اقسام`\n"
            "- الحالة: اكتب `.لوحة حالة`\n"
            "- التبديل السريع: اكتب `.لوحة تبديل`\n"
            "- أو لعرض قسم محدد: `.لوحة قسم <اسم القسم>`\n"
            "- للتبديل المباشر: `.لوحة تبديل afk|custom|protect|storage`"
        )
        await event.reply(msg)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة اقسام))
async def palette_text_categories(event):
    cats = "**الأقسام المتاحة:**\n" + "\n".join([f"- {c}" for c in CATEGORIES.keys()])
    cats += "\n\nاستخدم: `.لوحة قسم <اسم القسم>`"
    await event.edit(cats)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة حالة))
async def palette_text_status(event):
    snap = _status_snapshot()
    text = "**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    await event.edit(text)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة تبديل))
async def palette_text_toggles(event):
    snap = _status_snapshot()
    text = "**لوحة التحكم — التبديل السريع**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    text += "\n\nاستخدم: `.لوحة تبديل afk|custom|protect|storage`"
    await event.edit(text)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة قسم (.+)))
async def palette_text_category(event):
    cat = event.pattern_match.group(1).strip()
    await event.edit(format_commands_for(cat))


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة تبديل (afk|custom|protect|storage)))
async def palette_text_toggle(event):
    toggle_what = event.pattern_match.group(1)
    msg = ""
    try:
        if toggle_what == "afk":
            from plugins import afk as _afk
            _afk.afk_mode = not _afk.afk_mode
            msg = f"تم {'تشغيل' if _afk.afk_mode else 'تعطيل'} AFK."
        elif toggle_what == "custom":
            from plugins import afk as _afk
            _afk.custom_replies_enabled = not _afk.custom_replies_enabled
            msg = f"تم {'تشغيل' if _afk.custom_replies_enabled else 'تعطيل'} الردود المخصصة."
        elif toggle_what == "protect":
            protection_data['enabled'] = not protection_data.get('enabled', False)
            save_protection()
            msg = f"تم {'تفعيل' if protection_data['enabled'] else 'تعطيل'} حماية الخاص."
        elif toggle_what == "storage":
            gid = _load_group_id()
            if gid and os.path.exists(GROUP_ID_FILE):
                os.remove(GROUP_ID_FILE)
                msg = "تم تعطيل التخزين وإزالة ربط المجموعة."
            else:
                await _ensure_storage_group(event)
                msg = "تم تفعيل التخزين وإنشاء/ربط المجموعة."
    except Exception as e:
        msg = f"خطأ أثناء التبديل: {e}"

    snap = _status_snapshot()
    text = msg + "\n\n" + ("**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()]))
    await event.edit(text)


@client.on(events.CallbackQuery))
async def palette_callbacks(event):
    # وضع البوت فقط: يستقبل CallbackQuery
    me = await client.get_me()
    if not getattr(me, "bot", False):
        return
    if not event.data or not event.data.startswith(b"palette:"):
        return
    parts = event.data.decode("utf-8", errors="ignore").split(":")
    if len(parts) < 2:
        return
    action = parts[1]

    if action == "home":
        text, buttons = _main_menu()
        return await event.edit(text, buttons=buttons)

    if action == "cats":
        text, buttons = _categories_menu()
        return await event.edit(text, buttons=buttons)

    if action == "cat" and len(parts) >= 3:
        cat_name = ":".join(parts[2:])
        try:
            text = format_commands_for(cat_name)
        except Exception:
            text = f"تعذر تحميل أوامر القسم: {cat_name}"
        buttons = [[Button.inline("رجوع ◀️", data=b"palette:cats")]]
        return await event.edit(text, buttons=buttons)

    if action == "status":
        snap = _status_snapshot()
        text = "**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
        buttons = [[Button.inline("رجوع ◀️", data=b"palette:home")]]
        return await event.edit(text, buttons=buttons)

    if action == "toggles":
        text, buttons = _toggles_menu()
        return await event.edit(text, buttons=buttons)

    if action == "toggle" and len(parts) >= 3:
        toggle_what = parts[2]
        msg = ""
        try:
            if toggle_what == "afk":
                from plugins import afk as _afk
                _afk.afk_mode = not _afk.afk_mode
                msg = f"تم {'تشغيل' if _afk.afk_mode else 'تعطيل'} AFK."
            elif toggle_what == "custom":
                from plugins import afk as _afk
                _afk.custom_replies_enabled = not _afk.custom_replies_enabled
                msg = f"تم {'تشغيل' if _afk.custom_replies_enabled else 'تعطيل'} الردود المخصصة."
            elif toggle_what == "protect":
                protection_data['enabled'] = not protection_data.get('enabled', False)
                save_protection()
                msg = f"تم {'تفعيل' if protection_data['enabled'] else 'تعطيل'} حماية الخاص."
            elif toggle_what == "storage":
                gid = _load_group_id()
                if gid:
                    if os.path.exists(GROUP_ID_FILE):
                        os.remove(GROUP_ID_FILE)
                    msg = "تم تعطيل التخزين وإزالة ربط المجموعة."
                else:
                    await _ensure_storage_group(event)
                    msg = "تم تفعيل التخزين وإنشاء/ربط المجموعة."
        except Exception as e:
            msg = f"خطأ أثناء التبديل: {e}"

        text, buttons = _toggles_menu()
        text = f"{msg}\n\n" + text
        return await event.edit(text, buttons=buttons)))
async def palette_text_category(event):
    cat = event.pattern_match.group(1).strip()
    await event.edit(format_commands_for(cat))

@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة تبديل (afk|custom|protect|storage)s
from telethon import events, Button
from core.client import client

# Import internal states to present/toggle quickly
from plugins.help import CATEGORIES, format_commands_for
from plugins.afk import afk_mode as _afk_mode_ref, custom_replies_enabled as _custom_enabled_ref, custom_replies as _custom_replies_ref
from plugins.protection import protection_data, save_protection
from plugins.storage import _load_group_id, _ensure_storage_group, GROUP_ID_FILE
from plugins.auto_reply import DATA as AUTO_REPLY_DATA
from plugins.timers_publish import active_publishing_tasks


def _status_snapshot():
    # Read dynamic states
    afk = _afk_mode_ref
    custom = _custom_enabled_ref
    custom_count = len(_custom_replies_ref or {})
    protection = bool(protection_data.get("enabled", False))
    warn_max = int(protection_data.get("warnings", {}).get("max_warnings", 0)) if isinstance(protection_data.get("warnings"), dict) else None
    storage_id = _load_group_id()
    replies_enabled_groups = len(AUTO_REPLY_DATA.get("enabled_groups", []))
    replies_count = len(AUTO_REPLY_DATA.get("responses", {}))
    publishing_chats = len(active_publishing_tasks or {})
    return {
        "AFK": "مفعل" if afk else "معطل",
        "الردود المخصصة": f"{'مفعلة' if custom else 'معطلة'} ({custom_count} رد)",
        "حماية الخاص": "مفعلة" if protection else "معطلة",
        "مجموعة التخزين": f"موجودة ({storage_id})" if storage_id else "غير مفعلة",
        "الردود في مجموعات": f"{replies_enabled_groups} مجموعة / {replies_count} رد",
        "نشر تلقائي": f"{publishing_chats} محادثة نشطة",
    }


def _main_menu():
    return (
        "**لوحة التحكم — القائمة الرئيسية**\n"
        "اختر من الأزرار أدناه:\n"
        "• الأقسام: تصفح الأوامر حسب القسم.\n"
        "• الحالة: نظرة سريعة على وضع الميزات.\n"
        "• التبديل السريع: تفعيل/تعطيل ميزات شائعة."
    ), [
        [Button.inline("الأقسام 📚", data=b"palette:cats"), Button.inline("الحالة 📊", data=b"palette:status")],
        [Button.inline("التبديل السريع ⚙️", data=b"palette:toggles")]
    ]


def _categories_menu():
    rows = []
    row = []
    for cat in CATEGORIES.keys():
        label = cat[:20]
        row.append(Button.inline(label, data=("palette:cat:" + cat).encode("utf-8")))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([Button.inline("رجوع ◀️", data=b"palette:home")])
    return "**لوحة التحكم — الأقسام**\nاختر قسمًا للاطلاع على أوامره:", rows


def _toggles_menu():
    snap = _status_snapshot()
    text = "**لوحة التحكم — التبديل السريع**\n"
    text += "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    rows = [
        [
            Button.inline(f"AFK: {'تعطيل' if 'مفعل' in snap['AFK'] else 'تشغيل'}", data=b"palette:toggle:afk"),
            Button.inline(f"مخصص: {'تعطيل' if 'مفعلة' in snap['الردود المخصصة'] else 'تشغيل'}", data=b"palette:toggle:custom"),
        ],
        [
            Button.inline(f"حماية: {'تعطيل' if 'مفعلة' in snap['حماية الخاص'] else 'تشغيل'}", data=b"palette:toggle:protect"),
            Button.inline(f"التخزين: {'تعطيل' if 'موجودة' in snap['مجموعة التخزين'] else 'تفعيل'}", data=b"palette:toggle:storage"),
        ],
        [Button.inline("رجوع ◀️", data=b"palette:home")]
    ]
    return text, rows


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة))
async def palette_main(event):
    me = await client.get_me()
    if getattr(me, "bot", False):
        text, buttons = _main_menu()
        await event.reply(text, buttons=buttons)
    else:
        # User accounts لا تستقبل CallbackQuery. نعرض نسخة نصية مع أوامر مباشرة.
        msg = (
            "**لوحة التحكم (وضع المستخدم)**\n"
            "- الأقسام: اكتب `.لوحة اقسام`\n"
            "- الحالة: اكتب `.لوحة حالة`\n"
            "- التبديل السريع: اكتب `.لوحة تبديل`\n"
            "- أو لعرض قسم محدد: `.لوحة قسم <اسم القسم>`\n"
            "- للتبديل المباشر: `.لوحة تبديل afk|custom|protect|storage`"
        )
        await event.reply(msg)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة اقسام))
async def palette_text_categories(event):
    cats = "**الأقسام المتاحة:**\n" + "\n".join([f"- {c}" for c in CATEGORIES.keys()])
    cats += "\n\nاستخدم: `.لوحة قسم <اسم القسم>`"
    await event.edit(cats)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة حالة))
async def palette_text_status(event):
    snap = _status_snapshot()
    text = "**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    await event.edit(text)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة تبديل))
async def palette_text_toggles(event):
    snap = _status_snapshot()
    text = "**لوحة التحكم — التبديل السريع**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    text += "\n\nاستخدم: `.لوحة تبديل afk|custom|protect|storage`"
    await event.edit(text)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة قسم (.+)))
async def palette_text_category(event):
    cat = event.pattern_match.group(1).strip()
    await event.edit(format_commands_for(cat))


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة تبديل (afk|custom|protect|storage)))
async def palette_text_toggle(event):
    toggle_what = event.pattern_match.group(1)
    msg = ""
    try:
        if toggle_what == "afk":
            from plugins import afk as _afk
            _afk.afk_mode = not _afk.afk_mode
            msg = f"تم {'تشغيل' if _afk.afk_mode else 'تعطيل'} AFK."
        elif toggle_what == "custom":
            from plugins import afk as _afk
            _afk.custom_replies_enabled = not _afk.custom_replies_enabled
            msg = f"تم {'تشغيل' if _afk.custom_replies_enabled else 'تعطيل'} الردود المخصصة."
        elif toggle_what == "protect":
            protection_data['enabled'] = not protection_data.get('enabled', False)
            save_protection()
            msg = f"تم {'تفعيل' if protection_data['enabled'] else 'تعطيل'} حماية الخاص."
        elif toggle_what == "storage":
            gid = _load_group_id()
            if gid and os.path.exists(GROUP_ID_FILE):
                os.remove(GROUP_ID_FILE)
                msg = "تم تعطيل التخزين وإزالة ربط المجموعة."
            else:
                await _ensure_storage_group(event)
                msg = "تم تفعيل التخزين وإنشاء/ربط المجموعة."
    except Exception as e:
        msg = f"خطأ أثناء التبديل: {e}"

    snap = _status_snapshot()
    text = msg + "\n\n" + ("**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()]))
    await event.edit(text)


@client.on(events.CallbackQuery))
async def palette_callbacks(event):
    # وضع البوت فقط: يستقبل CallbackQuery
    me = await client.get_me()
    if not getattr(me, "bot", False):
        return
    if not event.data or not event.data.startswith(b"palette:"):
        return
    parts = event.data.decode("utf-8", errors="ignore").split(":")
    if len(parts) < 2:
        return
    action = parts[1]

    if action == "home":
        text, buttons = _main_menu()
        return await event.edit(text, buttons=buttons)

    if action == "cats":
        text, buttons = _categories_menu()
        return await event.edit(text, buttons=buttons)

    if action == "cat" and len(parts) >= 3:
        cat_name = ":".join(parts[2:])
        try:
            text = format_commands_for(cat_name)
        except Exception:
            text = f"تعذر تحميل أوامر القسم: {cat_name}"
        buttons = [[Button.inline("رجوع ◀️", data=b"palette:cats")]]
        return await event.edit(text, buttons=buttons)

    if action == "status":
        snap = _status_snapshot()
        text = "**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
        buttons = [[Button.inline("رجوع ◀️", data=b"palette:home")]]
        return await event.edit(text, buttons=buttons)

    if action == "toggles":
        text, buttons = _toggles_menu()
        return await event.edit(text, buttons=buttons)

    if action == "toggle" and len(parts) >= 3:
        toggle_what = parts[2]
        msg = ""
        try:
            if toggle_what == "afk":
                from plugins import afk as _afk
                _afk.afk_mode = not _afk.afk_mode
                msg = f"تم {'تشغيل' if _afk.afk_mode else 'تعطيل'} AFK."
            elif toggle_what == "custom":
                from plugins import afk as _afk
                _afk.custom_replies_enabled = not _afk.custom_replies_enabled
                msg = f"تم {'تشغيل' if _afk.custom_replies_enabled else 'تعطيل'} الردود المخصصة."
            elif toggle_what == "protect":
                protection_data['enabled'] = not protection_data.get('enabled', False)
                save_protection()
                msg = f"تم {'تفعيل' if protection_data['enabled'] else 'تعطيل'} حماية الخاص."
            elif toggle_what == "storage":
                gid = _load_group_id()
                if gid:
                    if os.path.exists(GROUP_ID_FILE):
                        os.remove(GROUP_ID_FILE)
                    msg = "تم تعطيل التخزين وإزالة ربط المجموعة."
                else:
                    await _ensure_storage_group(event)
                    msg = "تم تفعيل التخزين وإنشاء/ربط المجموعة."
        except Exception as e:
            msg = f"خطأ أثناء التبديل: {e}"

        text, buttons = _toggles_menu()
        text = f"{msg}\n\n" + text
        return await event.edit(text, buttons=buttons)))
async def palette_text_toggle(event):
    lang = get_lang(getattr(event.message, "id", 0))
    toggle_what = event.pattern_match.group(1)
    msg = ""
    try:
        if toggle_what == "afk":
            from plugins import afk as _afk
            _afk.afk_mode = not _afk.afk_mode
            msg = f"تم {'تشغيل' if _afk.afk_mode else 'تعطيل'} AFK."
        elif toggle_what == "custom":
            from plugins import afk as _afk
            _afk.custom_replies_enabled = not _afk.custom_replies_enabled
            msg = f"تم {'تشغيل' if _afk.custom_replies_enabled else 'تعطيل'} الردود المخصصة."
        elif toggle_what == "protect":
            protection_data['enabled'] = not protection_data.get('enabled', False)
            save_protection()
            msg = f"تم {'تفعيل' if protection_data['enabled'] else 'تعطيل'} حماية الخاص."
        elif toggle_what == "storage":
            gid = _load_group_id()
            if gid and os.path.exists(GROUP_ID_FILE):
                os.remove(GROUP_ID_FILE)
                msg = "تم تعطيل التخزين وإزالة ربط المجموعة."
            else:
                await _ensure_storage_group(event)
                msg = "تم تفعيل التخزين وإنشاء/ربط المجموعة."
    except Exception as e:
        msg = f"خطأ أثناء التبديل: {e}"

    snap = _status_snapshot()
    text = msg + "\n\n" + (t("panel_status_title", lang) + "\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()]))
    await event.edit(text)

# Callback (bot mode) — keep Arabic labels by default
try:
    from core.bot_client import bot_client
except Exception:
    bot_client = None

if bot_client:
    @bot_client.on(events.CallbackQuery)
    async def palette_callbacks(event):
        if not event.data or not event.data.startswith(b"palette:"):
            return
        parts = event.data.decode("utf-8", errors="ignore").split(":")
        if len(parts) < 2:
            return
        action = parts[1]

        if action == "home":
            text = _main_menu_text('ar')
            buttons = [
                [Button.inline("الأقسام 📚", data=b"palette:cats"), Button.inline("الحالة 📊", data=b"palette:status")],
                [Button.inline("التبديل السريع ⚙️", data=b"palette:toggles")]
            ]
            return await event.edit(text, buttons=buttons)

        if action == "cats":
            text, buttons = _categories_menu()
            return await event.edit(text, buttons=buttons)

        if action == "cat" and len(parts) >= 3:
            cat_name = ":".join(parts[2:])
            try:
                text = format_commands_for(cat_name)
            except Exception:
                text = f"تعذر تحميل أوامر القسم: {cat_name}"
            buttons = [[Button.inline("رجوع ◀️", data=b"palette:cats")]]
            return await event.edit(text, buttons=buttons)

        if action == "status":
            snap = _status_snapshot()
            text = "**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
            buttons = [[Button.inline("رجوع ◀️", data=b"palette:home")]]
            return await event.edit(text, buttons=buttons)

        if action == "toggles":
            text, buttons = _toggles_menu('ar')
            return await event.edit(text, buttons=buttons)

        if action == "toggle" and len(parts) >= 3:
            toggle_what = parts[2]
            msg = ""
            try:
                if toggle_what == "afk":
                    from plugins import afk as _afk
                    _afk.afk_mode = not _afk.afk_mode
                    msg = f"تم {'تشغيل' if _afk.afk_mode else 'تعطيل'} AFK."
                elif toggle_what == "custom":
                    from plugins import afk as _afk
                    _afk.custom_replies_enabled = not _afk.custom_replies_enabled
                    msg = f"تم {'تشغيل' if _afk.custom_replies_enabled else 'تعطيل'} الردود المخصصة."
                elif toggle_what == "protect":
                    protection_data['enabled'] = not protection_data.get('enabled', False)
                    save_protection()
                    msg = f"تم {'تفعيل' if protection_data['enabled'] else 'تعطيل'} حماية الخاص."
                elif toggle_what == "storage":
                    gid = _load_group_id()
                    if gid:
                        if os.path.exists(GROUP_ID_FILE):
                            os.remove(GROUP_ID_FILE)
                        msg = "تم تعطيل التخزين وإزالة ربط المجموعة."
                    else:
                        await _ensure_storage_group(event)
                        msg = "تم تفعيل التخزين وإنشاء/ربط المجموعة."
            except Exception as e:
                msg = f"خطأ أثناء التبديل: {e}"

            text, buttons = _toggles_menu('ar')
            text = f"{msg}\n\n" + text
            return await event.edit(text, buttons=buttons)s
from telethon import events, Button
from core.client import client

# Import internal states to present/toggle quickly
from plugins.help import CATEGORIES, format_commands_for
from plugins.afk import afk_mode as _afk_mode_ref, custom_replies_enabled as _custom_enabled_ref, custom_replies as _custom_replies_ref
from plugins.protection import protection_data, save_protection
from plugins.storage import _load_group_id, _ensure_storage_group, GROUP_ID_FILE
from plugins.auto_reply import DATA as AUTO_REPLY_DATA
from plugins.timers_publish import active_publishing_tasks


def _status_snapshot():
    # Read dynamic states
    afk = _afk_mode_ref
    custom = _custom_enabled_ref
    custom_count = len(_custom_replies_ref or {})
    protection = bool(protection_data.get("enabled", False))
    warn_max = int(protection_data.get("warnings", {}).get("max_warnings", 0)) if isinstance(protection_data.get("warnings"), dict) else None
    storage_id = _load_group_id()
    replies_enabled_groups = len(AUTO_REPLY_DATA.get("enabled_groups", []))
    replies_count = len(AUTO_REPLY_DATA.get("responses", {}))
    publishing_chats = len(active_publishing_tasks or {})
    return {
        "AFK": "مفعل" if afk else "معطل",
        "الردود المخصصة": f"{'مفعلة' if custom else 'معطلة'} ({custom_count} رد)",
        "حماية الخاص": "مفعلة" if protection else "معطلة",
        "مجموعة التخزين": f"موجودة ({storage_id})" if storage_id else "غير مفعلة",
        "الردود في مجموعات": f"{replies_enabled_groups} مجموعة / {replies_count} رد",
        "نشر تلقائي": f"{publishing_chats} محادثة نشطة",
    }


def _main_menu():
    return (
        "**لوحة التحكم — القائمة الرئيسية**\n"
        "اختر من الأزرار أدناه:\n"
        "• الأقسام: تصفح الأوامر حسب القسم.\n"
        "• الحالة: نظرة سريعة على وضع الميزات.\n"
        "• التبديل السريع: تفعيل/تعطيل ميزات شائعة."
    ), [
        [Button.inline("الأقسام 📚", data=b"palette:cats"), Button.inline("الحالة 📊", data=b"palette:status")],
        [Button.inline("التبديل السريع ⚙️", data=b"palette:toggles")]
    ]


def _categories_menu():
    rows = []
    row = []
    for cat in CATEGORIES.keys():
        label = cat[:20]
        row.append(Button.inline(label, data=("palette:cat:" + cat).encode("utf-8")))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([Button.inline("رجوع ◀️", data=b"palette:home")])
    return "**لوحة التحكم — الأقسام**\nاختر قسمًا للاطلاع على أوامره:", rows


def _toggles_menu():
    snap = _status_snapshot()
    text = "**لوحة التحكم — التبديل السريع**\n"
    text += "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    rows = [
        [
            Button.inline(f"AFK: {'تعطيل' if 'مفعل' in snap['AFK'] else 'تشغيل'}", data=b"palette:toggle:afk"),
            Button.inline(f"مخصص: {'تعطيل' if 'مفعلة' in snap['الردود المخصصة'] else 'تشغيل'}", data=b"palette:toggle:custom"),
        ],
        [
            Button.inline(f"حماية: {'تعطيل' if 'مفعلة' in snap['حماية الخاص'] else 'تشغيل'}", data=b"palette:toggle:protect"),
            Button.inline(f"التخزين: {'تعطيل' if 'موجودة' in snap['مجموعة التخزين'] else 'تفعيل'}", data=b"palette:toggle:storage"),
        ],
        [Button.inline("رجوع ◀️", data=b"palette:home")]
    ]
    return text, rows


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة))
async def palette_main(event):
    me = await client.get_me()
    if getattr(me, "bot", False):
        text, buttons = _main_menu()
        await event.reply(text, buttons=buttons)
    else:
        # User accounts لا تستقبل CallbackQuery. نعرض نسخة نصية مع أوامر مباشرة.
        msg = (
            "**لوحة التحكم (وضع المستخدم)**\n"
            "- الأقسام: اكتب `.لوحة اقسام`\n"
            "- الحالة: اكتب `.لوحة حالة`\n"
            "- التبديل السريع: اكتب `.لوحة تبديل`\n"
            "- أو لعرض قسم محدد: `.لوحة قسم <اسم القسم>`\n"
            "- للتبديل المباشر: `.لوحة تبديل afk|custom|protect|storage`"
        )
        await event.reply(msg)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة اقسام))
async def palette_text_categories(event):
    cats = "**الأقسام المتاحة:**\n" + "\n".join([f"- {c}" for c in CATEGORIES.keys()])
    cats += "\n\nاستخدم: `.لوحة قسم <اسم القسم>`"
    await event.edit(cats)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة حالة))
async def palette_text_status(event):
    snap = _status_snapshot()
    text = "**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    await event.edit(text)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة تبديل))
async def palette_text_toggles(event):
    snap = _status_snapshot()
    text = "**لوحة التحكم — التبديل السريع**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
    text += "\n\nاستخدم: `.لوحة تبديل afk|custom|protect|storage`"
    await event.edit(text)


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة قسم (.+)))
async def palette_text_category(event):
    cat = event.pattern_match.group(1).strip()
    await event.edit(format_commands_for(cat))


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة تبديل (afk|custom|protect|storage)))
async def palette_text_toggle(event):
    toggle_what = event.pattern_match.group(1)
    msg = ""
    try:
        if toggle_what == "afk":
            from plugins import afk as _afk
            _afk.afk_mode = not _afk.afk_mode
            msg = f"تم {'تشغيل' if _afk.afk_mode else 'تعطيل'} AFK."
        elif toggle_what == "custom":
            from plugins import afk as _afk
            _afk.custom_replies_enabled = not _afk.custom_replies_enabled
            msg = f"تم {'تشغيل' if _afk.custom_replies_enabled else 'تعطيل'} الردود المخصصة."
        elif toggle_what == "protect":
            protection_data['enabled'] = not protection_data.get('enabled', False)
            save_protection()
            msg = f"تم {'تفعيل' if protection_data['enabled'] else 'تعطيل'} حماية الخاص."
        elif toggle_what == "storage":
            gid = _load_group_id()
            if gid and os.path.exists(GROUP_ID_FILE):
                os.remove(GROUP_ID_FILE)
                msg = "تم تعطيل التخزين وإزالة ربط المجموعة."
            else:
                await _ensure_storage_group(event)
                msg = "تم تفعيل التخزين وإنشاء/ربط المجموعة."
    except Exception as e:
        msg = f"خطأ أثناء التبديل: {e}"

    snap = _status_snapshot()
    text = msg + "\n\n" + ("**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()]))
    await event.edit(text)


@client.on(events.CallbackQuery))
async def palette_callbacks(event):
    # وضع البوت فقط: يستقبل CallbackQuery
    me = await client.get_me()
    if not getattr(me, "bot", False):
        return
    if not event.data or not event.data.startswith(b"palette:"):
        return
    parts = event.data.decode("utf-8", errors="ignore").split(":")
    if len(parts) < 2:
        return
    action = parts[1]

    if action == "home":
        text, buttons = _main_menu()
        return await event.edit(text, buttons=buttons)

    if action == "cats":
        text, buttons = _categories_menu()
        return await event.edit(text, buttons=buttons)

    if action == "cat" and len(parts) >= 3:
        cat_name = ":".join(parts[2:])
        try:
            text = format_commands_for(cat_name)
        except Exception:
            text = f"تعذر تحميل أوامر القسم: {cat_name}"
        buttons = [[Button.inline("رجوع ◀️", data=b"palette:cats")]]
        return await event.edit(text, buttons=buttons)

    if action == "status":
        snap = _status_snapshot()
        text = "**لوحة التحكم — الحالة**\n" + "\n".join([f"- {k}: {v}" for k, v in snap.items()])
        buttons = [[Button.inline("رجوع ◀️", data=b"palette:home")]]
        return await event.edit(text, buttons=buttons)

    if action == "toggles":
        text, buttons = _toggles_menu()
        return await event.edit(text, buttons=buttons)

    if action == "toggle" and len(parts) >= 3:
        toggle_what = parts[2]
        msg = ""
        try:
            if toggle_what == "afk":
                from plugins import afk as _afk
                _afk.afk_mode = not _afk.afk_mode
                msg = f"تم {'تشغيل' if _afk.afk_mode else 'تعطيل'} AFK."
            elif toggle_what == "custom":
                from plugins import afk as _afk
                _afk.custom_replies_enabled = not _afk.custom_replies_enabled
                msg = f"تم {'تشغيل' if _afk.custom_replies_enabled else 'تعطيل'} الردود المخصصة."
            elif toggle_what == "protect":
                protection_data['enabled'] = not protection_data.get('enabled', False)
                save_protection()
                msg = f"تم {'تفعيل' if protection_data['enabled'] else 'تعطيل'} حماية الخاص."
            elif toggle_what == "storage":
                gid = _load_group_id()
                if gid:
                    if os.path.exists(GROUP_ID_FILE):
                        os.remove(GROUP_ID_FILE)
                    msg = "تم تعطيل التخزين وإزالة ربط المجموعة."
                else:
                    await _ensure_storage_group(event)
                    msg = "تم تفعيل التخزين وإنشاء/ربط المجموعة."
        except Exception as e:
            msg = f"خطأ أثناء التبديل: {e}"

        text, buttons = _toggles_menu()
        text = f"{msg}\n\n" + text
        return await event.edit(text, buttons=buttons)