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


@client.on(events.NewMessage(from_users='me', pattern=r'^\.لوحة$'))
async def palette_main(event):
    text, buttons = _main_menu()
    await event.reply(text, buttons=buttons)


@client.on(events.CallbackQuery)
async def palette_callbacks(event):
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
        cat_name = ":".join(parts[2:])  # في حال الاسم يحوي نقطتين
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
                # flip the module-level variable
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
                    # disable by removing id file
                    if os.path.exists(GROUP_ID_FILE):
                        os.remove(GROUP_ID_FILE)
                    msg = "تم تعطيل التخزين وإزالة ربط المجموعة."
                else:
                    await _ensure_storage_group(event)
                    msg = "تم تفعيل التخزين وإنشاء/ربط المجموعة."

            else:
                msg = "أمر تبديل غير معروف."
        except Exception as e:
            msg = f"خطأ أثناء التبديل: {e}"

        # Refresh toggles menu after action
        text, buttons = _toggles_menu()
        text = f"{msg}\n\n" + text
        return await event.edit(text, buttons=buttons)