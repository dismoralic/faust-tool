from telethon import events

async def get_all_users(client, chat_id):
    users = []
    async for user in client.iter_participants(chat_id):
        users.append((user.id, user.first_name or "Без имени"))
    return users

def register(client):
    @client.on(events.NewMessage(pattern=r"\.call"))
    async def call_all(event):
        chat = await event.get_chat()
        users = await get_all_users(event.client, chat.id)
        
        if not users:
            await event.reply("Не удалось собрать пользователей.")
            return
        
        mentions = " ".join([f"[{name}](tg://user?id={user_id})" for user_id, name in users])
        await event.reply(f"{mentions}")
        await event.delete()
