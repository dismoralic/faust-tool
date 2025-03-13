import asyncio
from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=".sound"))
    async def send_to_voicy(event):
        reply = await event.get_reply_message()
        if not reply or not reply.media:
            return await event.reply("Ответь на голосовое или видео, чтобы распознать речь.")

        message = await event.reply("Обработка...")

        # Пересылаем в @VoicyBot
        await client.forward_messages("@VoicyBot", reply)

        # Ждём ответа от VoicyBot
        async for response in client.iter_messages("@VoicyBot", limit=5):
            if response.reply_to and response.reply_to.reply_to_msg_id == reply.id:
                await message.edit(f"- {response.text}")
                break
        else:
            await message.edit("Ошибка: faust-tool не ответил.")
