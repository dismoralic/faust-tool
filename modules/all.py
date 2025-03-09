from telethon import events

async def get_users(client, chat_id, limit=100):
    users = []
    async for user in client.iter_participants(chat_id):
        users.append(f"[{user.first_name or 'Без имени'}](tg://user?id={user.id})")
        if len(users) >= limit:
            break
    return users

def register(client):
    @client.on(events.NewMessage(pattern=r"\.call"))
    async def call_command(event):
        me = await event.client.get_me()
        if event.sender_id != me.id:
            return

        chat = await event.get_chat()
        users = await get_users(event.client, chat.id)

        if not users:
            await event.reply("Не удалось собрать пользователей.")
            return

        await event.reply(" ".join(users))
        await event.delete()
