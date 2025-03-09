from telethon import events, functions, errors, types
import asyncio

async def add_contacts(event):
    chat = await event.get_chat()
    messages = await event.client.get_messages(chat, limit=500)
    
    try:
        participants = await event.client.get_participants(chat)
    except Exception as e:
        print(f"Ошибка получения участников: {e}")
        participants = []
    
    added_count = 0
    added_users = set()

    await event.edit("0")
    
    async def add_user(user):
        nonlocal added_count
        if isinstance(user, (types.User, types.UserEmpty)) and user.id not in added_users:
            try:
                await event.client(functions.contacts.AddContactRequest(
                    id=user.id,
                    first_name="user",
                    last_name="",
                    phone=""
                ))
                added_users.add(user.id)
                added_count += 1
                await event.edit(f"{added_count}")
                await asyncio.sleep(1)
            except errors.FloodWaitError as e:
                print(f"Флуд-контроль: ждем {e.seconds} секунд")
                await asyncio.sleep(e.seconds)
            except errors.UserPrivacyRestrictedError:
                print(f"Приватность запрещает добавление {user.id}")
            except Exception as e:
                print(f"Ошибка при добавлении {user.id}: {e}")
    
    for msg in messages:
        await add_user(msg.sender)
    
    for participant in participants:
        await add_user(participant)
    
    await event.edit("готово")

def register(client):
    client.add_event_handler(add_contacts, events.NewMessage(pattern=r"\.addcontacts", outgoing=True))
