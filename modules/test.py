from telethon import events

async def test_command(event):
    await event.edit("👍")

def register(client):
    client.add_event_handler(test_command, events.NewMessage(pattern=r"^\.test$", outgoing=True))
