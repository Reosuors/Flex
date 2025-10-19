import os
import shutil
import time
import asyncio
from telethon import events
from core.client import client

# repeating publisher state
active_publishing_tasks = {}
base_images_dir = os.path.join(os.getcwd(), 'images')


@client.on(events.NewMessage(from_users='me', pattern=r'.تكرار (\d+) (\d+) ?([\s\S]*)'))
@client.on(events.NewMessage(from_users='me', pattern=r'.تك (\d+) (\d+) ?([\s\S]*)'))
@client.on(events.NewMessage(from_users='me', pattern=r'.نشر (\d+) (\d+) ?([\s\S]*)'))
async def start_repeating_process(event):
    await event.delete()
    try:
        seconds = int(event.pattern_match.group(1))
        repeat_count = int(event.pattern_match.group(2))
        custom_text = event.pattern_match.group(3)

        if seconds < 40:
            await event.reply("**⎙ يجب أن يكون الوقت المحدد لا يقل عن 40 ثانية.**")
            return

        process_images_dir = None
        media_files = []

        if event.is_reply:
            message = await event.get_reply_message()

            process_id = int(time.time())
            process_images_dir = os.path.join(base_images_dir, str(process_id))
            os.makedirs(process_images_dir, exist_ok=True)

            if message.media:
                if message.grouped_id:
                    messages = await client.get_messages(event.chat_id, min_id=message.id - 10, max_id=message.id + 10)
                    for msg in messages:
                        if msg.grouped_id == message.grouped_id and msg.photo:
                            file_path = os.path.join(process_images_dir, f"image_{msg.id}.jpg")
                            await msg.download_media(file=file_path)
                            media_files.append(file_path)
                else:
                    if message.photo:
                        file_path = os.path.join(process_images_dir, f"image_{message.id}.jpg")
                        await message.download_media(file=file_path)
                        media_files.append(file_path)

            if not media_files and not custom_text:
                await event.reply("**⎙ يجب تحديد نص مخصص أو الرد على صورة.**")
                return

        async def task():
            for _ in range(repeat_count):
                if media_files:
                    await client.send_file(event.chat_id, media_files, caption=custom_text)
                else:
                    await client.send_message(event.chat_id, custom_text)
                await asyncio.sleep(seconds)

            if process_images_dir and os.path.exists(process_images_dir):
                shutil.rmtree(process_images_dir)

            active_publishing_tasks.pop(event.chat_id, None)

        t = asyncio.create_task(task())

        if event.chat_id not in active_publishing_tasks:
            active_publishing_tasks[event.chat_id] = []
        active_publishing_tasks[event.chat_id].append((t, process_images_dir))

        await asyncio.sleep(2)
        confirmation_message = await event.reply(f"سيتم إرسال الرسالة كل {seconds} ثانية لـ {repeat_count} مرات.")

        await asyncio.sleep(1)
        await event.delete()
        await confirmation_message.delete()

    except Exception as e:
        await event.reply(f"⎙ حدث خطأ: {e}")


@client.on(events.NewMessage(from_users='me', pattern=r'.ايقاف النشر التلقائي'))
async def stop_sending(event):
    await event.delete()
    try:
        if event.chat_id in active_publishing_tasks:
            for task, process_images_dir in active_publishing_tasks[event.chat_id]:
                task.cancel()
                if process_images_dir and os.path.exists(process_images_dir):
                    shutil.rmtree(process_images_dir)
            del active_publishing_tasks[event.chat_id]

            reply = await event.reply("   ‌‎✓ تم إيقاف جميع عمليات النشر المفعله   ‌‎⎙.")
            await asyncio.sleep(1)
            await event.delete()
            await asyncio.sleep(3)
            await reply.delete()
        else:
            await event.reply("   ‌‎⎙ لا توجد عمليات نشر فعّالة لإيقافها.")
    except Exception as e:
        await event.reply(f"⎙ حدث خطأ: {e}")