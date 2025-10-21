import json
import re
from telethon import events, functions
from telethon.tl.functions.contacts import BlockRequest
from core.client import client

# Private protection (bad words + warnings/ban)
PROTECTION_FILE = "private_protection.json"
WARNINGS_FILE = "warnings.json"
OWNER_ID = 6383191007  # يمكن تعديله لاحقًا من الإعدادات


def _load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# initialize protection data
protection_data = _load_json(
    PROTECTION_FILE,
    {
        "enabled": True,
        "banned_words": [
            "كسمك", "انيك امك", "قحبة", "شرموطة", "زبي", "متناك", "خول", "عاهرة",
            "زب", "عرص", "قواد", "حيوان", "زبالة", "ملعون", "تف عليك", "كحبة", "كلب",
            "يلعن شكلك", "يا ابن الكلب", "ابن المتناكه", "ابن الوسخة", "تفو عليك",
            "يلعن دينك", "عرص ابن عرص", "متناك ابن المتناك", "قحب", "زناخة", "وسخ",
            "منيك", "بنت القحبة", "ابن الشرموطة", "خنزير", "قذارة", "نتن", "نجس",
            "عديم الشرف", "عبيط", "غبي", "حمار", "بغل", "قليل الأدب", "سافل",
            "وسخ ابن وسخة", "حثالة", "وضيع", "ملعون الوالدين", "ابن الزنا", "ديوث",
            "الكلب ابن الكلب", "المنايك", "ابن العاهرة", "قليل الحياء", "سافل منحط",
            "فاسق", "كافر", "خنيث", "واطي", "منحط", "حثالة المجتمع", "حقير", "تيس",
            "تافه", "ما عندك رجولة", "مسخرة", "وضيع", "زفت", "معفن", "انجس الناس",
            "اخس البشر", "انت ولا شي", "خنزير قذر", "ملعون أبوك", "انعل ابو شكلك"
        ],
        "warnings": {}
    }
)

warnings_data = _load_json(
    WARNINGS_FILE,
    {
        "warnings": {},
        "whitelist": [],
        "max_warnings": 5,
        "warnings_enabled": True,
        "warning_message": "⎙ تحذير {warnings}/{max_warnings}\n⎙ يرجى عدم الإزعاج وإلا سيتم حظرك تلقائيًا!"
    }
)


def save_protection():
    _save_json(PROTECTION_FILE, protection_data)


def save_warnings():
    _save_json(WARNINGS_FILE, warnings_data)


@client.on(events.NewMessage(pattern=r"^\.حماية الخاص$"))
async def toggle_private_protection(event):
    protection_data["enabled"] = not protection_data["enabled"]
    save_protection()
    status = "⎙ مفعلة" if protection_data["enabled"] else "⎙ معطلة"
    await event.edit(f"**⎙ تم تغيير وضع حماية الخاص إلى:** {status}")


@client.on(events.NewMessage(pattern=r"^\.اضافة_كلمة_سيئة (.+)$"))
async def add_bad_word(event):
    word = event.pattern_match.group(1).strip().lower()
    if word and word not in protection_data["banned_words"]:
        protection_data["banned_words"].append(word)
        save_protection()
        await event.edit(f"✓ تم إضافة الكلمة إلى القائمة السوداء: {word}")
    else:
        await event.edit("الكلمة موجودة بالفعل أو غير صالحة.")

@client.on(events.NewMessage(pattern=r"^\.ازالة_كلمة_سيئة (.+)$"))
async def remove_bad_word(event):
    word = event.pattern_match.group(1).strip().lower()
    if word in protection_data["banned_words"]:
        protection_data["banned_words"].remove(word)
        save_protection()
        await event.edit(f"✓ تم إزالة الكلمة: {word}")
    else:
        await event.edit("الكلمة غير موجودة في القائمة.")

@client.on(events.NewMessage(pattern=r"^\.قائمة_الكلمات_السيئة$"))
async def list_bad_words(event):
    words = protection_data.get("banned_words", [])
    if not words:
        await event.edit("لا توجد كلمات سيئة محددة.")
        return
    await event.edit("القائمة السوداء:\n- " + "\n- ".join(words))


@client.on(events.NewMessage)
async def delete_bad_words(event):
    if not protection_data["enabled"]:
        return
    if event.is_private and event.text:
        text_lower = (event.text or "").lower()
        for word in protection_data["banned_words"]:
            if re.search(rf"\b{re.escape(word)}\b", text_lower):
                try:
                    await event.delete()
                except Exception:
                    pass
                # Warnings increment
                uid = str(event.sender_id)
                protection_data["warnings"][uid] = protection_data["warnings"].get(uid, 0) + 1
                save_protection()

                count = protection_data["warnings"][uid]
                if count >= 3:
                    try:
                        await event.respond("**⎙ تم حظرك بسبب استخدامك كلمات غير لائقة!**")
                        await client(BlockRequest(event.sender_id))
                    except Exception:
                        pass
                    # reset warnings after ban
                    protection_data["warnings"].pop(uid, None)
                    save_protection()
                else:
                    left = 3 - count
                    await event.respond(f"⎙ تحذير {count}/3 ⚠️\n⎙ لا تغلط لانك راح تنهان {left} تحذير{'ات' if left > 1 else ''}!")
                break


# Full warnings system (private)
@client.on(events.NewMessage(incoming=True))
async def handle_private_messages(event):
    if not event.is_private or not warnings_data.get("warnings_enabled", False):
        return

    sender = await event.get_sender()
    user_id = sender.id

    me = await client.get_me()
    if user_id in (me.id, OWNER_ID) or sender.bot:
        return
    if user_id in warnings_data.get("whitelist", []):
        return

    key = str(user_id)
    warnings_data["warnings"].setdefault(key, 0)
    warnings_data["warnings"][key] += 1
    save_warnings()

    warnings = warnings_data["warnings"][key]
    max_warnings = warnings_data.get("max_warnings", 5)

    if warnings >= max_warnings:
        await event.respond(f"**⎙ تم حظرك بسبب تجاوز التحذيرات ({max_warnings})!**")
        try:
            await client(BlockRequest(user_id))
        except Exception:
            pass
    else:
        msg = warnings_data.get("warning_message", "⎙ تحذير {warnings}/{max_warnings}").format(
            warnings=warnings, max_warnings=max_warnings
        )
        await event.reply(msg)


@client.on(events.NewMessage(pattern=r"^\.قبول$"))
async def accept_user(event):
    if event.is_group or event.is_channel:
        return
    reply = await event.get_reply_message()
    if not reply:
        await event.edit("**⎙ يجب الرد على رسالة المستخدم لقبوله.**")
        return
    sender = await reply.get_sender()
    user_id = sender.id
    if user_id not in warnings_data["whitelist"]:
        warnings_data["whitelist"].append(user_id)
        save_warnings()
    await event.edit("**⎙ تم قبول المستخدم، لن يتلقى تحذيرات بعد الآن.**")


@client.on(events.NewMessage(pattern=r"^\.الغاء القبول$"))
async def remove_acceptance(event):
    if event.is_group or event.is_channel:
        return
    reply = await event.get_reply_message()
    if not reply:
        await event.edit("**⎙ يجب الرد على رسالة المستخدم لإلغاء قبوله.**")
        return
    sender = await reply.get_sender()
    user_id = sender.id
    if user_id in warnings_data["whitelist"]:
        warnings_data["whitelist"].remove(user_id)
        save_warnings()
    await event.edit("**⎙ تم إلغاء قبول المستخدم، سيتلقى تحذيرات عند المراسلة.**")


@client.on(events.NewMessage(pattern=r"^\.مسح التحذيرات$"))
async def clear_warnings(event):
    if event.is_group or event.is_channel:
        return
    reply = await event.get_reply_message()
    if not reply:
        await event.edit("**⎙ يجب الرد على رسالة المستخدم لمسح تحذيراته.**")
        return
    sender = await reply.get_sender()
    user_id = sender.id
    if str(user_id) in warnings_data["warnings"]:
        del warnings_data["warnings"][str(user_id)]
        save_warnings()
    await event.edit("**⎙ تم مسح جميع تحذيرات المستخدم.**")


@client.on(events.NewMessage(pattern=r"^\.التحذيرات$"))
async def show_warnings(event):
    if event.is_group or event.is_channel:
        return
    sender = await event.get_sender()
    user_id = sender.id
    warnings = warnings_data["warnings"].get(str(user_id), 0)
    max_warnings = warnings_data["max_warnings"]
    await event.edit(f"**⎙ لديك {warnings} من {max_warnings} تحذيرات.**")


@client.on(events.NewMessage(pattern=r"^\.تعيين كليشة التحذير$"))
async def change_warning_message(event):
    reply = await event.get_reply_message()
    if not reply:
        await event.edit("**⎙ يجب الرد على رسالة تحتوي على الكليشة الجديدة.**")
        return
    warnings_data["warning_message"] = reply.text
    save_warnings()
    await event.edit("**⎙ تم تغيير كليشة التحذير بنجاح!**")


@client.on(events.NewMessage(pattern=r"^\.عرض كليشة$"))
async def show_warning_message(event):
    if event.is_group or event.is_channel:
        return
    await event.edit(f"**⎙ رسالة التحذير الحالية:\n\n{warnings_data['warning_message']}**")


@client.on(events.NewMessage(pattern=r"^\.عدد التحذيرات (\d+)$"))
async def change_max_warnings(event):
    if event.is_group or event.is_channel:
        return
    new_limit = int(event.pattern_match.group(1))
    if new_limit <= 0:
        await event.edit("**⎙ الحد الأقصى للتحذيرات يجب أن يكون أكبر من صفر.**")
        return
    warnings_data["max_warnings"] = new_limit
    save_warnings()
    await event.edit(f"**⎙ تم تعديل الحد الأقصى للتحذيرات إلى {new_limit}.**")


@client.on(events.NewMessage(pattern=r"^\.المحظورين$"))
async def show_banned_users(event):
    if event.is_group or event.is_channel:
        return
    banned_users = [uid for uid, count in warnings_data["warnings"].items() if count >= warnings_data["max_warnings"]]
    if not banned_users:
        await event.edit("**⎙ لا يوجد مستخدمون محظورون حاليًا.**")
    else:
        banned_list = "\n".join(f"⎙ {uid}" for uid in banned_users)
        await event.edit(f"⎙ قائمة المحظورين:\n{banned_list}")


@client.on(events.NewMessage(pattern=r"^\.مسح المحظورين$"))
async def clear_banned_users(event):
    if event.is_group or event.is_channel:
        return
    warnings_data["warnings"] = {uid: cnt for uid, cnt in warnings_data["warnings"].items() if cnt < warnings_data["max_warnings"]}
    save_warnings()
    await event.edit("**⎙ تم مسح جميع المحظورين.**")