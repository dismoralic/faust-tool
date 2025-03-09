from telethon import events
import io

async def save_self_destruct_media(event):
    """Сохраняет самоуничтожающиеся фото и видео."""
    reply = await event.get_reply_message()
    if not reply or not reply.media or not reply.media.ttl_seconds:
        await event.reply("❌ Реплай на самоуничтожающееся фото или видео!")
        return

    await event.edit(":)")  
    new = io.BytesIO(await reply.download_media(bytes))  

    if reply.video:
        new.name = "saved_video.mp4"
    elif reply.photo:
        new.name = "saved_image.jpg"
    else:
        new.name = reply.file.name or "saved_media"

    await event.client.send_file("me", new)  
    await event.delete()  

def register(client):
    client.add_event_handler(save_self_destruct_media, events.NewMessage(pattern=r"\.sv", outgoing=True))
