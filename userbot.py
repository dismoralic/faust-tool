import asyncio
from telethon import TelegramClient, events
import os
import importlib
import json
import time
import subprocess
import sys

CONFIG_FILE = "config.json"
MODULES_DIR = "modules"
start_time = time.time()

def get_api_credentials():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    
    api_id = input("Введите API_ID: ")
    api_hash = input("Введите API_HASH: ")
    
    credentials = {"API_ID": int(api_id), "API_HASH": api_hash}
    with open(CONFIG_FILE, "w") as file:
        json.dump(credentials, file)
    
    return credentials

credentials = get_api_credentials()
client = TelegramClient("faust_tool_session", credentials["API_ID"], credentials["API_HASH"])

def load_modules(client):
    if not os.path.exists(MODULES_DIR):
        os.makedirs(MODULES_DIR)
    for filename in os.listdir(MODULES_DIR):
        if filename.endswith(".py"):
            module_name = f"{MODULES_DIR}.{filename[:-3]}"
            module = importlib.import_module(module_name)
            if hasattr(module, "register"):
                module.register(client)
                print(f"✅ Загружен модуль: {filename}")

@client.on(events.NewMessage(pattern=r"\.update", outgoing=True))
async def update(event):
    await event.edit("🔄 Обновляю faust tool...")
    process = subprocess.run(["git", "pull"], capture_output=True, text=True)   
    if "Already up to date." in process.stdout:
        await event.edit("✅ У вас уже последняя версия faust-tool!")
    else:
        await event.edit("✅ Обновление загружено! Идет перезапуск...")
        os.execl(sys.executable, sys.executable, *sys.argv)

@client.on(events.NewMessage(pattern=r"\.ping", outgoing=True))
async def ping(event):
    start_time_ping = time.time()
    await event.edit("testing...")
    ping_time = round((time.time() - start_time_ping) * 1000, 2)
    await event.edit(f"ping: {ping_time}ms")

@client.on(events.NewMessage(pattern=r"\.uptime", outgoing=True))
async def uptime(event):
    uptime_seconds = int(time.time() - start_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    await event.edit(f"⏳ faust tool работает уже {hours}ч {minutes}м {seconds}с")

@client.on(events.NewMessage(pattern=r"\.save", outgoing=True))
async def save_self_destructing_media(event):
    reply = await event.get_reply_message()
    if reply and reply.media and reply.media.ttl_seconds:
        await client.send_message("me", "Сохранено самоудаляющееся медиа:", file=reply.media)
        await event.edit("Медиа сохранено в избранное")
    else:
        await event.edit("Ответь на самоудаляющееся медиа")

@client.on(events.NewMessage(pattern=r"\.spam (\d+) (.+)", outgoing=True))
async def spam(event):
    count = int(event.pattern_match.group(1))
    message = event.pattern_match.group(2)
    for _ in range(count):
        await event.respond(message)
    await event.delete()

@client.on(events.NewMessage(pattern=r"\.phones", outgoing=True))
async def scan_numbers(event):
    chat = await event.get_chat()
    users = await client.get_participants(chat)
    phone_numbers = {}
    for user in users:
        if user.phone:
            phone_numbers[user.first_name or "Без имени"] = user.phone
    if phone_numbers:
        result = "Слитые номера:\n" + "\n".join(f"{name}: {phone}" for name, phone in phone_numbers.items())
        await client.send_message("me", result)
        await event.edit("Слитые номера отправлены в избранное")
    else:
        await event.edit("В чате нет номеров")

from telethon import events

@client.on(events.NewMessage(pattern=r"\.help", outgoing=True))
async def help_command(event):
    help_text = "🛠 **Доступные команды faust tool:**\n"
    help_text += "⚡️ **.ping** - Проверка пинга\n"
    help_text += "⚡️ **.uptime** - Время работы faust tool\n"
    help_text += "⚡️ **.info / .note** - Информация о пользователе (реплей, или без)\n"
    help_text += "⚡️ **.spam [кол-во] [текст]** - Спам\n"
    help_text += "⚡️ **.phones** - Сбор слитых номеров\n"
    help_text += "⚡️ **.sv** - Сохранение самоудаляющегося медиа\n"
    help_text += "⚡️ **.video** - Скачивание видео\n"
    help_text += "⚡️ **.help** - Список команд\n"
    help_text += "⚡️ **.admin help** - Команды администратора чата\n"
    help_text += "⚡️ **.trns help** - Перевод ваших сообщений в реальном времени\n"
    help_text += "⚡️ **.respond help** - Автоответчик\n"
    help_text += "⚡️ **.call** - Призывает первых 100 участников чата\n\n"
    help_text += "⚡️ **.dlmod** - Установка faust-модуля (ответом на сообщение)\n"
    help_text += "⚡️ **.update** - Полное обновление инструмента до последней версии\n\n"
    help_text += "Лишь только идущий осилит дорогу.. лишь тот, кто найдет в себе силу — шагнуть 🕊\n"
    help_text += "Creator: `angel_xranytel`\n"
    help_text += "`2.1.0v alpha`\n\n"
    await event.edit(help_text)

load_modules(client)
client.start()
print("✅ faust tool запущен!")
client.run_until_disconnected()
