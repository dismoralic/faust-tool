import os
import asyncio
from telethon import events
from yt_dlp import YoutubeDL

VIDEO_DIR = "videos"
if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

def download_video(url):
    options = {
        'format': 'best',
        'outtmpl': f'{VIDEO_DIR}/%(title)s.%(ext)s',
        'quiet': True,
    }
    
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return os.path.join(VIDEO_DIR, f"{info['title']}.{info['ext']}")

async def video_handler(event):
    reply = await event.get_reply_message()
    if not reply or not reply.message:
        await event.edit("❌ Ответь на сообщение с ссылкой!")
        return
    
    url = reply.message.strip()
    if not ("youtube.com" in url or "youtu.be" in url or "instagram.com" in url):
        await event.edit("❌ Это не ссылка на YouTube или Instagram!")
        return
    
    await event.edit("📥 Скачиваю видео...")
    
    loop = asyncio.get_running_loop()
    file_path = await loop.run_in_executor(None, download_video, url)
    
    await event.reply("🎬 Вот твоё видео:", file=file_path)
    await event.delete()
    os.remove(file_path)  # Удаляем файл после отправки

def register(client):
    client.add_event_handler(video_handler, events.NewMessage(pattern=r'\.video', outgoing=True))
