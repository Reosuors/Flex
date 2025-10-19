import re
import os
import asyncio
import pickle
from datetime import datetime
import pytz
from telethon import events
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from core.client import client

time_update_status_file = 'time_pdate_status.pkl'  # keep original filename
account_name = None

# Load time update toggle
if os.path.exists(time_update_status_file):
    with open(time_update_status_file, 'rb') as f:
        time_update_status = pickle.load(f)
else:
    time_update_status = {'enabled': False}


def superscript_time(time_str):
    # visually similar to original
    trans = str.maketrans('0123456789', '𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟭𝟴𝟵')
    return time_str.translate(trans)


async def get_account_name():
    me = await client.get_me()
    return re.sub(r' - \d{2}:\d{2}', '', me.first_name or '')


@client.on(events.NewMessage(from_users='me', pattern=r'\.تفعيل الاسم الوقتي'))
async def enable_time_update(event):
    await event.delete()
    global time_update_status
    time_update_status['enabled'] = True
    with open(time_update_status_file, 'wb') as f:
        pickle.dump(time_update_status, f)
    reply = await event.reply("✓ تم تفعيل الاسم مع الوقت   ‌‎⎙.")
    await asyncio.sleep(1)
    await reply.delete()


@client.on(events.NewMessage(from_users='me', pattern=r'\.تعطيل الاسم الوقتي'))
async def disable_time_update(event):
    await event.delete()
    global time_update_status, account_name
    time_update_status['enabled'] = False
    with open(time_update_status_file, 'wb') as f:
        pickle.dump(time_update_status, f)

    if account_name:
        new_username = f"{re.sub(r' - \d{2}:\d{2}', '', account_name)}"
        try:
            await client(UpdateProfileRequest(first_name=new_username))
            reply = await event.reply("✓ تم تعطيل الاسم وإزالة الوقت من الاسم   ‌‎⎙.")
        except Exception as e:
            reply = await event.reply(f"⎙ حدث خطأ أثناء إزالة الوقت من الاسم: {e}")
    else:
        reply = await event.reply("⎙ لم يتم تعيين اسم الحساب.")
    await asyncio.sleep(1)
    await reply.delete()


@client.on(events.NewMessage(from_users='me', pattern=r'\.الاسم'))
async def set_account_name(event):
    await event.delete()
    global account_name
    try:
        _, text = event.raw_text.split(' ', 1)
        if '(' in text and ')' in text:
            account_name = text.split('(', 1)[1].split(')')[0].strip()
        else:
            await event.reply("⚠️ استخدم الصيغة: .الاسم (الاسم الجديد)")
            return

        iraq_tz = pytz.timezone('Asia/Baghdad')
        now = datetime.now(iraq_tz)
        current_time = superscript_time(now.strftime("%I:%M"))
        new_username = f"{account_name} - {current_time}"

        await client(UpdateProfileRequest(first_name=new_username))
        await event.reply(f"✓ تم تغيير اسم الحساب إلى {new_username}⎙")
    except Exception as e:
        await event.reply(f"⎙ حدث خطأ أثناء تغيير الاسم: {e}")


# Impersonate / restore
profile_saved = False


async def save_my_profile():
    user = await client.get_me()
    if not os.path.exists("imagee"):
        os.mkdir("imagee")
    current_name = user.first_name or ""
    full = await client(GetFullUserRequest(user.id))
    current_bio = full.full_user.about or ""

    with open("account_info.txt", "w", encoding="utf-8") as f:
        f.write(f"Name: {current_name}\nBio: {current_bio}")

    if user.photo:
        await client.download_profile_photo(user.id, file="imagee/my_profile.jpg")


@client.on(events.NewMessage(from_users='me', pattern=r'\.انتحال'))
async def handle_impersonate(event):
    global profile_saved
    if not profile_saved:
        await save_my_profile()
        profile_saved = True

    if event.is_reply:
        reply_message = await event.get_reply_message()
        full = await client(GetFullUserRequest(reply_message.sender_id))
        new_name = (full.users[0].first_name or "")
        new_bio = full.full_user.about or ""
        try:
            await client(UpdateProfileRequest(first_name=new_name, about=new_bio))
            await event.reply(f"⎙ تم تغيير الاسم إلى {new_name} والبايو إلى: {new_bio}")
        except Exception as e:
            await event.reply(f"⎙ حدث خطأ أثناء تحديث الاسم أو البايو: {e}")

        # photo
        if full.users[0].photo:
            if not os.path.exists("hh"):
                os.mkdir("hh")
            photo_path = await client.download_profile_photo(full.users[0].id, file=f"hh/{full.users[0].id}.jpg")
            try:
                await client(DeletePhotosRequest(await client.get_profile_photos('me')))
                uploaded = await client.upload_file(photo_path)
                await client(UploadProfilePhotoRequest(file=uploaded))
                await event.reply("⎙ تم تغيير صورة الحساب")
            except Exception as e:
                await event.reply(f"⎙ حدث خطأ أثناء تغيير صورة الحساب: {e}")
        else:
            await event.reply("⎙ لا يملك المستخدم صورة.")
    await event.delete()


@client.on(events.NewMessage(from_users='me', pattern=r'\.ارجاع'))
async def handle_restore(event):
    try:
        if os.path.exists("account_info.txt"):
            with open("account_info.txt", "r", encoding="utf-8") as f:
                data = f.readlines()
                restored_name = data[0].replace("Name: ", "").strip()
                restored_bio = data[1].replace("Bio: ", "").strip()
            await client(UpdateProfileRequest(first_name=restored_name, about=restored_bio))
            await event.reply(f"⎙ تم استرجاع الاسم إلى {restored_name} والبايو إلى: {restored_bio}")
        else:
            await event.reply("⎙ ملف الحساب غير موجود.")

        photo_path = "imagee/my_profile.jpg"
        if os.path.exists(photo_path):
            uploaded = await client.upload_file(photo_path)
            await client(DeletePhotosRequest(await client.get_profile_photos('me')))
            await client(UploadProfilePhotoRequest(file=uploaded))
            await event.reply("⎙ تم استرجاع صورة الحساب بنجاح.")
        else:
            await event.reply("⎙ تعذر العثور على الصورة المحفوظة.")
    except Exception as e:
        await event.reply(f"⎙ حدث خطأ أثناء استرجاع الحساب: {e}")
    await event.delete()