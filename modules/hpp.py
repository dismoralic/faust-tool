from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r"\.hpp", outgoing=True))
    async def hpp_handler(event):
        await event.reply("test2")