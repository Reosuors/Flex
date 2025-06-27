import os
import asyncio
import pickle
import logging
import time
import random
import threading
import html
import json
import re
import string
import base64
import pybase64
import io
import requests
import aiohttp
import shutil
from datetime import datetime, timedelta
from math import sqrt
from queue import Queue
from threading import Thread

# إعداد التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# استيراد مكتبات Telethon
from telethon import TelegramClient, events, functions, sync, Button
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, MessageNotModifiedError, FloodWaitError
from telethon.errors import UserAdminInvalidError, ChatAdminRequiredError, ChannelInvalidError
from telethon.errors import MediaEmptyError, WebpageMediaEmptyError, WebpageCurlFailedError
from telethon.errors.rpcerrorlist import PeerIdInvalidError, MessageIdInvalidError
from telethon.errors.rpcerrorlist import StickerMimeInvalidError, PhotoExtInvalidError
from telethon.errors.rpcerrorlist import PhotoCropSizeSmallError, ImageProcessFailedError
from telethon.errors.rpcerrorlist import WebpageMediaEmptyError
from telethon.errors import RPCError, errors

# استيراد دوال Telethon
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import GetParticipantsRequest, InviteToChannelRequest
from telethon.tl.functions.channels import EditBannedRequest, GetParticipantRequest
from telethon.tl.functions.channels import CreateChannelRequest, EditPhotoRequest
from telethon.tl.functions.channels import JoinChannelRequest, EditTitleRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import ForwardMessagesRequest, EditMessageRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, DeleteHistoryRequest
from telethon.tl.functions.messages import GetHistoryRequest, ReportSpamRequest
from telethon.tl.functions.messages import GetFullChatRequest, DeleteMessagesRequest
from telethon.tl.functions.photos import GetUserPhotosRequest, UploadProfilePhotoRequest
from telethon.tl.functions.photos import DeletePhotosRequest
from telethon.tl.functions.users import GetFullUserRequest

# استيراد أنواع Telethon
from telethon.tl.types import ChannelParticipantCreator, ChannelParticipantAdmin
from telethon.tl.types import ChatBannedRights, User, InputWebDocument
from telethon.tl.types import InputMediaDice, InputMessagesFilterDocument
from telethon.tl.types import ChannelParticipantsAdmins, UserStatusEmpty
from telethon.tl.types import UserStatusLastMonth, UserStatusLastWeek
from telethon.tl.types import UserStatusRecently, UserStatusOnline
from telethon.tl.types import InputPeerUser, InputPeerChannel, InputPeerChat
from telethon.tl.types import MessageActionChannelMigrateFrom, PeerChannel, PeerUser
from telethon.tl.types import InputChatUploadedPhoto, InputChannel
from telethon.tl.types import ChannelParticipantsSearch, InputPhoto
from telethon.tl.types import InputMessagesFilterDocument, InputMessagesFilterPhotos
from telethon.tl.types import Channel, Chat, MessageMediaPhoto, MessageMediaDocument
from telethon.utils import get_input_photo

# استيراد مكتبات أخرى
from pySmartDL import SmartDL
from user_agent import generate_user_agent
from deep_translator import GoogleTranslator
from langdetect import detect
from gpytranslate import Translator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from emoji import emojize
from ping3 import ping
from PIL import Image
import pytz
import platform
import sys
import mention

# إزالة الطباعة الملونة للتوافق مع Render
logger.info("FLEX SOURCE - تم تشغيل اليوزر بوت")
logger.info("Dev: @nS_R_T")

# --- إعدادات البوت ---
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
SESSION_STRING = os.getenv('STRING_SESSION')

if not API_ID or not API_HASH or not SESSION_STRING:
    logger.error("متغيرات البيئة مفقودة: API_ID, API_HASH, STRING_SESSION")
    exit(1)

# إنشاء العميل
client = TelegramClient(StringSession(SESSION_STRING), int(API_ID), API_HASH)

# --- مسارات الملفات ---
response_file = 'responss.pkl'
published_messages_file = 'publihed_messages.pkl'
muted_users_file = 'mute_usrs.pkl'
time_update_status_file = 'time_pdate_status.pkl'
channel_link_file = 'channel_lnk.pkl'
image_folder = 'iage'
last_message_time_file = 'path_to_last_esage_time_file'
last_message_id_file = 'path_to_last_mesage_id_file'

# إنشاء مجلد الصور
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# --- دوال مساعدة ---
def load_data(file, default):
    if os.path.exists(file):
        try:
            with open(file, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            logger.error(f"خطأ في تحميل {file}: {e}")
            return default
    return default

def save_data(file, data):
    try:
        with open(file, 'wb') as f:
            pickle.dump(data, f)
    except Exception as e:
        logger.error(f"خطأ في حفظ {file}: {e}")

# تحميل البيانات
responses = load_data(response_file, {})
published_messages = load_data(published_messages_file, [])
muted_users = load_data(muted_users_file, {})
time_update_status = load_data(time_update_status_file, {'enabled': False})
channel_link = load_data(channel_link_file, None)

# متغيرات عامة
user_last_message_time = {}
user_last_message_id = {}
user_last_message_time_sent = {}
active_publishing_tasks = {}
active_timers = {}
countdown_messages = {}
mimic_user_id = None
account_name = None
image_path = 'local_image.jpg'

# --- دالة إدراج الإيموجي ---
def insert_emojis(message, emojis):
    random.shuffle(emojis)
    message_list = list(message)
    emoji_positions = []
    
    for emoji in emojis:
        pos = random.choice(range(len(message_list)))
        while pos in emoji_positions:
            pos = random.choice(range(len(message_list)))
        
        emoji_positions.append(pos)
        message_list[pos] = emoji
    
    return ''.join(message_list)

# --- أوامر البوت ---

@client.on(events.NewMessage(from_users='me', pattern='.متت'))
async def update_message(event):
    await event.delete()
    message_text = ' ' * 6
    emojis = ['🤣', '😂', '😹', '🤣', '😂', '😹']
    
    message = await event.respond('🤣😂😹🤣😂😹')
    
    last_message = ""
    start_time = asyncio.get_event_loop().time()
    duration = 5  
    
    while True:
        try:
            current_time = asyncio.get_event_loop().time()
            if current_time - start_time > duration:
                break
            
            emoji_string = insert_emojis(message_text, emojis)
            while emoji_string == last_message:
                emoji_string = insert_emojis(message_text, emojis)
            
            last_message = emoji_string
            await message.edit(emoji_string)
            
            await asyncio.sleep(0.1)

        except Exception as e:
            logger.error(f"خطأ في تحديث الرسالة: {e}")
            break

@client.on(events.NewMessage(from_users='me', pattern='.تقليد'))
async def set_mimic_user(event):
    global mimic_user_id
    if event.is_reply:
        reply_message = await event.get_reply_message()
        mimic_user_id = reply_message.sender_id
        await event.edit(f"**⎙ سيتم تقليد المستخدم {mimic_user_id}.**")
        await asyncio.sleep(2)
        await event.delete()
    else:
        await event.edit("**⎙ يرجى الرد على رسالة الشخص الذي تريد تقليده.**")

@client.on(events.NewMessage())
async def mimic_user(event):
    global mimic_user_id
    if mimic_user_id and event.sender_id == mimic_user_id and event.text:
        try:
            await client.send_message(event.chat_id, event.text)
        except Exception as e:
            logger.error(f"خطأ في التقليد: {e}")

@client.on(events.NewMessage(from_users='me', pattern='.ايقاف التقليد'))
async def stop_mimic(event):
    global mimic_user_id
    mimic_user_id = None
    await event.edit("**⎉╎تم ايـقـاف الـتـقـلـيـد .. بنجـاح ☑️.**")
    await asyncio.sleep(2)
    await event.delete()

@client.on(events.NewMessage(from_users='me', pattern='.انتحار'))
async def suicide_message(event):
    await event.delete()
    
    message = await event.respond("**جاري الانتحار .....**")
    
    await asyncio.sleep(3)
    
    final_message = (
        "تم الانتحار بنجاح😂...\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　　　　　|\n"
        "　／￣￣＼| \n"
        "＜ ´･ 　　 |＼ \n"
        "　|　３　 | 丶＼ \n"
        "＜ 、･　　|　　＼ \n"
        "　＼＿＿／∪ _ ∪) \n"
        "　　　　　 Ｕ Ｕ"
    )
    
    await message.edit(final_message)

@client.on(events.NewMessage(from_users='me', pattern='.شرير'))
async def evil_message(event):
    await event.delete()
    message_text = ' ' * 6
    emojis = ['😈', '💀', '👿', '🔪', '☠️', '👹']
    
    message = await event.respond('👿💀👹👿🔪☠️')
    
    last_message = ""
    start_time = asyncio.get_event_loop().time()
    duration = 5  
    
    while True:
        try:
            current_time = asyncio.get_event_loop().time()
            if current_time - start_time > duration:
                break
            
            emoji_string = insert_emojis(message_text, emojis)
            while emoji_string == last_message:
                emoji_string = insert_emojis(message_text, emojis)
            
            last_message = emoji_string
            await message.edit(emoji_string)
            
            await asyncio.sleep(0.1)

        except Exception as e:
            logger.error(f"خطأ في تحديث الرسالة: {e}")
            break

@client.on(events.NewMessage(from_users='me', pattern='.تفعيل التخزين'))
async def add_group(event):
    await event.delete()
    try:
        if event.is_group:
            await event.reply(f"**⎙ الكروب موجود بالفعل. سيتم تفعيل الكود في الكروب السابق.**")
        elif event.is_private:
            if os.path.exists('group_id.pkl'):
                group_id = load_data('group_id.pkl', None)
                if group_id:
                    try:
                        await client.get_entity(group_id)
                        await event.reply(f"**⎙ الكروب موجود بالفعل. سيتم تفعيل الكود في الكروب السابق.**")
                    except ValueError:
                        os.remove('group_id.pkl')
                        await create_storage_group(event)
                else:
                    await create_storage_group(event)
            else:
                await create_storage_group(event)
    except Exception as e:
        await event.reply(f"⎙ حدث خطأ: {str(e)}")

async def create_storage_group(event):
    try:
        group_name = "كروب التخزين"
        group_bio = "كروب التخزين المخصص من سورس flex"
        group = await client(CreateChannelRequest(
            title=group_name,
            about=group_bio,
            megagroup=True
        ))
        group_id = group.chats[0].id
        save_data('group_id.pkl', group_id)
        await event.reply(f"**⎙ تم إنشاء كروب جديد وتعيينه لتخزين الرسائل الخاصة**")
    except Exception as e:
        logger.error(f"خطأ في إنشاء كروب التخزين: {e}")
        await event.reply(f"⎙ حدث خطأ في إنشاء الكروب: {str(e)}")

# --- دالة إبقاء البوت نشطاً ---
async def keep_alive():
    """دالة لإبقاء البوت نشطاً على Render"""
    while True:
        try:
            await asyncio.sleep(300)  # 5 دقائق
            logger.info("البوت نشط ويعمل...")
        except Exception as e:
            logger.error(f"خطأ في keep_alive: {e}")

# --- الدالة الرئيسية ---
async def main():
    try:
        await client.start()
        logger.info("✅ تم تسجيل الدخول بنجاح")
        
        # الحصول على معلومات المستخدم
        me = await client.get_me()
        logger.info(f"تم تسجيل الدخول باسم: {me.first_name}")
        
        # بدء دالة إبقاء البوت نشطاً
        asyncio.create_task(keep_alive())
        
        logger.info("✅ اليوزر بوت يعمل الآن...")
        
        # إبقاء البوت يعمل
        await client.run_until_disconnected()
        
    except Exception as e:
        logger.error(f"❌ خطأ في تشغيل البوت: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("تم إيقاف البوت بواسطة المستخدم")
    except Exception as e:
        logger.error(f"خطأ عام: {e}")

