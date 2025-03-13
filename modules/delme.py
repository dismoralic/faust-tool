from telethon import events

async def delete_self_messages(event):
    chat = await event.get_chat()
    messages = await event.client.get_messages(chat, from_user='me', limit=500)
    
    for msg in messages:
        try:
            await msg.delete()
        except Exception as e:
            print(f"Ошибка при удалении {msg.id}: {e}")
    
    await event.delete()

def register(client):
    client.add_event_handler(delete_self_messages, events.NewMessage(pattern=r"\.delme", outgoing=True))
