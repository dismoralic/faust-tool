import asyncio
from telethon import TelegramClient, events
import os
import importlib
import json
import time

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

@client.on(events.NewMessage(pattern=r"\.ping", outgoing=True))
async def ping(event):
    start_time_ping = time.time()
    await event.edit("testing...")
    ping_time = round((time.time() - start_time_ping) * 1000, 2)
    await event.edit(f"ping: {ping_time}ms")

@client.on(events.NewMessage(pattern=r"\.start", outgoing=True))
async def start(event):
    await event.edit("Персональный помощник faust'a готов к службе")

@client.on(events.NewMessage(pattern=r"\.uptime", outgoing=True))
async def uptime(event):
    uptime_seconds = int(time.time() - start_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    await event.edit(f"⏳ faust tool работает уже {hours}ч {minutes}м {seconds}с")

@client.on(events.NewMessage(pattern=r"\.info", outgoing=True))
async def info(event):
    user = await event.client.get_me()
    info_text = (f"**Информация о пользователе**\n"
                 f"ID: {user.id}\n"
                 f"Username: @{user.username if user.username else 'Нет'}\n"
                 f"Имя: {user.first_name} {user.last_name if user.last_name else ''}\n")
    await event.edit(info_text)

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
        result = "📞 Слитые номера:\n" + "\n".join(f"{name}: {phone}" for name, phone in phone_numbers.items())
        await client.send_message("me", result)
        await event.edit("✅ Слитые номера отправлены в избранное")
    else:
        await event.edit("❌ В чате нет номеров")

@client.on(events.NewMessage(pattern=r"\.you", outgoing=True))
async def get_user_info(event):
    reply = await event.get_reply_message()
    if reply and reply.sender_id:
        user = await client.get_entity(reply.sender_id)
        info_text = f"**Информация о пользователе**\n"
        info_text += f"ID: {user.id}\n"
        info_text += f"Username: @{user.username if user.username else 'Нет'}\n"
        info_text += f"Имя: {user.first_name} {user.last_name if user.last_name else ''}\n"
        if user.phone:
            info_text += f"📞 Номер: {user.phone}\n"
        await event.edit(info_text)
    else:
        await event.edit("❌ Ответь на сообщение пользователя")

@client.on(events.NewMessage(pattern=r"\.save", outgoing=True))
async def save_self_destructing_media(event):
    reply = await event.get_reply_message()
    if reply and reply.media and reply.media.ttl_seconds:
        await client.send_message("me", "📥 Сохранено самоудаляющееся медиа:", file=reply.media)
        await event.edit("✅ Медиа сохранено в избранное")
    else:
        await event.edit("❌ Ответь на самоудаляющееся медиа")

@client.on(events.NewMessage(pattern=r"\.help", outgoing=True))
async def help_command(event):
    help_text = "🛠 **Доступные команды faust tool:**\n"
    help_text += "⚡️ **.ping** - Проверка пинга\n"
    help_text += "⚡️ **.start** - Запуск faust tool\n"
    help_text += "⚡️ **.uptime** - Время работы faust tool\n"
    help_text += "⚡️ **.info** - Информация о владельце\n"
    help_text += "⚡️ **.spam [кол-во] [текст]** - Спам\n"
    help_text += "⚡️ **.phones** - Сбор слитых номеров\n"
    help_text += "⚡️ **.you** - Информация о пользователе\n"
    help_text += "⚡️ **.sv** - Сохранение самоудаляющегося медиа\n"
    help_text += "⚡️ **.video** - Скачивание видео\n"
    help_text += "⚡️ **.help** - Список команд\n"
    help_text += "⚡️ **.ban** - Бан (минуты) (причина)\n"
    help_text += "⚡️ **.mute** - Мут (минуты) (причина)\n"
    help_text += "⚡️ **.kick** - Кик (минуты) (причина)\n"
    help_text += "⚡️ **.trns on <код>** - Перевод ваших сообщений в реальном времени\n"
    help_text += "⚡️ **.trns off** - Перевод ваших сообщений в реальном времени (откл)\n"
    help_text += "⚡️ **.trns list** - Список доступных кодов переводчика\n"
    help_text += "⚡️ **.dlmod** - Установка faust-модуля (ответом на сообщение)\n"
    help_text += "Автор: angel_xranytel\n"
    help_text += "1.0.0v alpha\n"
    await event.edit(help_text)

@client.on(events.NewMessage(pattern=r"\.nazira", outgoing=True))
async def nazira(event):
    message = await event.edit("<3")
    animation_sequence = [
        "💘", "💖", "💗", "💙", "💚", "💛", "🧡", "❤️", "░", "Н░", "На░", "Нази░", "Назир░", "Назира░",
        "Назира,░", "Назира, я░", "Назира, я л░", "Назира, я лю░", "Назира, я люб░", "Назира, я любл░",
        "Назира, я люблю░", "Назира, я люблю т░", "Назира, я люблю те░", "Назира, я люблю теб░", "Назира, я люблю тебя░",
        "Назира, я люблю тебя!", "Назира, я люблю тебя!💘", "Назира, я люблю тебя!💖", "Назира, я люблю тебя!💗", "Назира, я люблю тебя!🤍"
    ]
    
    for text in animation_sequence:
        await message.edit(text)
        await asyncio.sleep(0.5)

    await event.delete()

@client.on(events.NewMessage(pattern=r"\.albina", outgoing=True))
async def albina(event):
    message = await event.edit("<3")
    animation_sequence = [
        "💘", "💖", "💗", "💙", "💚", "💛", "🧡", "❤️", "░", "А░", "Ал░", "Аль░", "Альб░", "Альби░", "Альбин░",
        "Альбина, я░", "Альбина, я л░", "Альбина, я лю░", "Альбина, я люб░", "Альбина, я любл░", "Альбина, я люблю░",
        "Альбина, я люблю т░", "Альбина, я люблю те░", "Альбина, я люблю теб░", "Альбина, я люблю тебя░", "Альбина, я люблю тебя!░",
        "Альбина, я люблю тебя!💘", "Альбина, я люблю тебя!💖", "Альбина, я люблю тебя!💗", "Альбина, я люблю тебя!🤍",
        "░льбина, я люблю теб░", "░ьбина, я люблю те░", "░бина, я люблю т░", "░ина, я люблю░", "░на, я любл░", "░а, я люб░",
        "░я лю░", "░л░", "░", "░В░", "░Воз░", "░Возвр░", "░Возвращ░", "░Возвращай░", "░Возвращайся░",
        "░Возвращайся..░", "░Возвращайся...░", "░Возвращайся....░", "░Возвращай░", "░Возвращ░", "░Возвр░", "░Воз░", "░В░",
        "░..░", "░...░", "░Я░", "░Я не░", "░Я не мо░", "░Я не могу░", "░Я не могу бе░", "░Я не могу без т░",
        "░Я не могу без теб░", "░Я не могу без тебя░", "░Я не могу без тебя.░", "░Я не могу без тебя..░", "░Я не могу без тебя...░"
    ]
    for text in animation_sequence:
        await message.edit(text)
        await asyncio.sleep(0.5)
    await event.delete()

load_modules(client)
client.start()
print("✅ faust tool запущен!")
client.run_until_disconnected()
