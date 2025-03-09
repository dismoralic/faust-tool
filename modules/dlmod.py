from telethon import events
import os
import asyncio
import importlib.util
import sys

MODULES_DIR = "modules"

async def download_module(event):
    reply = await event.get_reply_message()
    
    if not reply or not reply.media:
        await event.reply("❌ Реплай на .py файл обязателен!")
        return
    
    file_name = reply.file.name if reply.file and reply.file.name else "module.py"
    
    if not file_name.endswith(".py"):
        await event.reply("❌ Это не Python файл!")
        return
    
    if not os.path.exists(MODULES_DIR):
        os.makedirs(MODULES_DIR)
    
    file_path = os.path.join(MODULES_DIR, file_name)
    await event.client.download_media(reply.media, file_path)
    
    module_name = file_name[:-3]
    module_path = os.path.abspath(file_path)
    
    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        if hasattr(module, "register"):
            module.register(event.client)
        await event.edit(f"✅ Модуль `{file_name}` загружен и активирован!")
    except Exception as e:
        await event.edit(f"❌ Ошибка при загрузке модуля `{file_name}`: {e}")

def register(client):
    client.add_event_handler(download_module, events.NewMessage(pattern=r"^\.dlmod$", outgoing=True))
