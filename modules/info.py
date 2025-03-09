from telethon import events
import json

NOTES_FILE = "notes.txt"

try:
    with open(NOTES_FILE, "r") as f:
        notes = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    notes = {}

def save_notes():
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f)

def register(client):
    @client.on(events.NewMessage(pattern=r"\.(note|info)", outgoing=True))
    async def note_info_handler(event):
        command = event.pattern_match.group(1)
        reply = await event.get_reply_message()
        user = await event.client.get_me() if not reply else await event.client.get_entity(reply.sender_id)
        user_id = str(user.id)
        user_mention = f"[{user.first_name}](tg://user?id={user.id})"

        if command == "note":
            args = event.message.text.split(maxsplit=1)
            if not reply or len(args) < 2:
                await event.edit("Ответь на сообщение пользователя и укажи заметку!")
                return
            note_text = args[1]
            notes[user_id] = note_text
            save_notes()
            await event.edit(f"Заметка сохранена для {user_mention}.")
        
        elif command == "info":
            note_text = notes.get(user_id, "Нет заметок.")
            info_text = (f"**Информация о пользователе**\n"
                         f"Имя: {user_mention}\n"
                         f"ID: `{user.id}`\n"
                         f"Username: @{user.username if user.username else 'Нет'}\n"
                         f"Заметка: {note_text}")
            await event.edit(info_text)
