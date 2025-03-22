from telethon import events
import time

async def edit_faust_message(event):
    start_time = time.time()
    await event.edit("Calculating ping...")
    ping_time = round((time.time() - start_time) * 1000, 2)
    text = ("𝙁𝙖𝙪𝙨𝙩-𝙏𝙤𝙤𝙡\n"
            "Version: 2.1.0\n\n"
            f"Ping: {ping_time} ms\n\n"
            "Only those who will risk going too far can possibly find out how far one can go\n\n"
            "Dev: @angel_xranytel\n"
            "Channel: @bio_faust")
    await event.edit(text)

def register(client):
    @client.on(events.NewMessage(pattern=r"^\.faust", outgoing=True))
    async def faust_command(event):
        await edit_faust_message(event)
