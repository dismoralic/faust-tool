import os
import json
import aiohttp
from pydub import AudioSegment
from telethon import events

WIT_AI_TOKEN = "J2H26WNNL2SHNPN5YAIG3R3S6T34M62U"

def register(client):
    @client.on(events.NewMessage(pattern=".sound"))
    async def speech_to_text(event):
        reply = await event.get_reply_message()
        if not reply or not reply.voice:
            return await event.edit("❌ Ответь на голосовое сообщение!")

        await event.edit("🎤 Обрабатываю...")

        file_path = await client.download_media(reply, "voice.ogg")
        audio_path = "voice.wav"

        try:
            AudioSegment.from_file(file_path).export(audio_path, format="wav")
            headers = {"Authorization": f"Bearer {WIT_AI_TOKEN}", "Content-Type": "audio/wav"}

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.wit.ai/speech?v=20230216",
                    headers=headers,
                    data=open(audio_path, "rb"),
                ) as response:
                    response_text = await response.text()

            os.remove(file_path)
            os.remove(audio_path)

            try:
                json_data = json.loads(response_text)
                texts = [item["text"] for item in json_data.get("speech", {}).get("tokens", []) if "text" in item]

                result = " ".join(texts) if texts else None
                if not result:
                    return await event.edit("❌ Не удалось распознать речь.")

                return await event.edit(f"🗣 {result}")

            except json.JSONDecodeError:
                return await event.edit("❌ Ошибка обработки ответа от Wit.ai.")

        except Exception as e:
            return await event.edit(f"❌ Ошибка обработки: {str(e)}")
