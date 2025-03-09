from datetime import datetime, timedelta
from telethon import events

last_response = {}
response_text = ""

def register(client):
    @client.on(events.NewMessage(pattern=r"^\.respond (on|off)(?:\s+(.*))?", outgoing=True))
    async def toggle_responder(event):
        global response_text
        command = event.pattern_match.group(1)
        text = event.pattern_match.group(2)
        
        if command == "on" and text:
            response_text = text
            await event.edit("Автоответчик включен.")
        elif command == "off":
            response_text = ""
            await event.edit("Автоответчик отключен.")
        else:
            await event.edit("Использование: \n.respond on <текст>\n.respond off")
    
    @client.on(events.NewMessage(pattern=r"^\.respond help", outgoing=True))
    async def respond_help(event):
        help_text = (
            "Команды автоответчика:\n"
            ".respond on <текст> - Включает автоответчик с указанным текстом.\n"
            ".respond off - Выключает автоответчик.\n"
            ".respond help - Показывает это сообщение."
        )
        await event.edit(help_text)
    
    @client.on(events.NewMessage(incoming=True))
    async def auto_respond(event):
        global last_response, response_text
        if not response_text:
            return
        if event.is_private:
            user_id = event.sender_id
            now = datetime.now()
            
            sender = await event.get_sender()
            if sender and not sender.bot:
                if user_id not in last_response or now - last_response[user_id] >= timedelta(days=1):
                    last_response[user_id] = now
                    await event.reply(response_text)
