import io
import os
import re
import random
import aiohttp
from PIL import Image
from telethon import events
from telethon.errors import YouBlockedUserError
from telethon.tl.types import MessageMediaPhoto, InputStickerSetID
from telethon.tl.functions.messages import GetStickerSetRequest
from core.client import client

# YouTube simple search (uses official API as in original)
YOUTUBE_API_KEY = 'AIzaSyBfb8a-Ug_YQFrpWKeTc88zuI6PmHVdzV0'
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/search'


@client.on(events.NewMessage(from_users='me', pattern=r'\.يوتيوب (.+)'))
async def youtube_search(event):
    await event.delete()
    query = event.pattern_match.group(1)
    async with aiohttp.ClientSession() as session:
        async with session.get(YOUTUBE_API_URL, params={
            'part': 'snippet',
            'q': query,
            'key': YOUTUBE_API_KEY,
            'type': 'video',
            'maxResults': 1
        }) as response:
            data = await response.json()
            if data.get('items'):
                video_id = data['items'][0]['id']['videoId']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                await event.reply(f"📹 هنا رابط الفيديو الذي تم العثور عليه:\n{video_url}")
            else:
                await event.reply("⎙ لم يتم العثور على فيديو يتطابق مع العنوان المطلوب.")


# Sticker creation via @Stickers (simplified, one-shot pack publish)
STICKER_BOT = "@Stickers"
KANGING_STR = [
    "⪼ جاري صنع الملصق...",
    "⪼ جاري التعديل على الملصق...",
    "⪼ جاري حفظ الملصق بحقوقك..."
]


@client.on(events.NewMessage(pattern=r'\.ملصق(?:\s|$)([\s\S]*)'))
async def create_sticker(event):
    try:
        reply = await event.get_reply_message()
        if not reply or not reply.media:
            await event.edit("⪼ بالرد على صورة أو ملصق")
            return

        await event.edit(random.choice(KANGING_STR))

        # download photo or image document
        if isinstance(reply.media, MessageMediaPhoto):
            photo = io.BytesIO()
            photo = await client.download_media(reply.photo, photo)
        elif reply.document and 'image' in reply.document.mime_type:
            photo = io.BytesIO()
            await client.download_media(reply.document, photo)
        else:
            await event.edit("⪼ نوع الملف غير مدعوم")
            return

        # resize to 512
        image = Image.open(photo)
        image.thumbnail((512, 512))
        output = io.BytesIO()
        output.name = "sticker.webp"
        image.save(output, "WEBP")
        output.seek(0)

        async with client.conversation(STICKER_BOT) as conv:
            try:
                await conv.send_message('/newpack')
            except YouBlockedUserError:
                await event.client(functions.contacts.UnblockRequest(STICKER_BOT))
                await conv.send_message('/newpack')

            await conv.get_response()
            await conv.send_message("حزمة جديدة")
            await conv.get_response()
            await client.send_file(conv.chat_id, output)
            await conv.get_response()
            await conv.send_message('😂')
            await conv.get_response()
            await conv.send_message('/publish')
            await conv.get_response()
            await conv.send_message('/skip')
            await conv.get_response()
            await conv.send_message("اسم الحزمة")
            await conv.get_response()

        await event.edit("✓ تم إنشاء الملصق بنجاح!")
    except Exception as e:
        await event.edit(f"⪼ حدث خطأ: {str(e)}")


@client.on(events.NewMessage(pattern=r'\.معلومات الملصق$'))
async def sticker_info(event):
    try:
        reply = await event.get_reply_message()
        if not reply or not reply.sticker:
            await event.edit("⪼ بالرد على ملصق")
            return

        stickerset = await client(GetStickerSetRequest(
            InputStickerSetID(
                id=reply.sticker.id,
                access_hash=reply.sticker.access_hash
            )
        ))

        await event.edit(
            f"معلومات الملصق:\n"
            f"- اسم الحزمة: {stickerset.set.title}\n"
            f"- الرابط: t.me/addstickers/{stickerset.set.short_name}\n"
            f"- عدد الملصقات: {stickerset.set.count}\n"
            f"- الإيموجي: {reply.sticker.emoji or '❌'}"
        )
    except Exception as e:
        await event.edit(f"⪼ حدث خطأ: {str(e)}")


# TikTok downloader (best-effort, as original relied on external API)
@client.on(events.NewMessage(pattern=r'\.تك ?(.+)?'))
async def tiktok_dl(event):
    ms = (event.pattern_match.group(1) or "").strip()
    if not (("https://tiktok.com/" in ms) or ("https://vm.tiktok.com/" in ms)):
        return
    await event.delete()
    status = await event.respond('يجري البحث عن الملف..')
    link = ms
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://godownloader.com/api/tiktok-no-watermark-free?url={link}&key=godownloader.com") as resp:
                data = await resp.json()
                video_link = data.get("video_no_watermark")
                if not video_link:
                    await status.edit("الرابط غير صحيح تأكد منه!")
                    return
                async with session.get(video_link) as v:
                    if v.status == 200:
                        video_data = await v.read()
                        directory = str(int(random.random() * 1e9))
                        os.mkdir(directory)
                        filename = f"{directory}/{int(random.random()*1e9)}.mp4"
                        with open(filename, "wb") as f:
                            f.write(video_data)
                        await event.client.send_file(
                            event.chat_id,
                            filename,
                            caption="تم التحميل من تيك توك",
                        )
                        os.remove(filename)
                        os.rmdir(directory)
                        await status.delete()
                    else:
                        await status.edit("⎙ فشل تحميل الفيديو")
    except Exception as er:
        await status.edit(f"حدث خطأ: {er}")