import os
import json
import asyncio
import aiohttp
import speech_recognition as sr
from pydub import AudioSegment
from telethon import events

WIT_AI_TOKEN = "J2H26WNNL2SHNPN5YAIG3R3S6T34M62U"

def register(client):
    @client.on(events.NewMessage(pattern=".sound"))
    async def speech_to_text(event):
        reply = await event.get_reply_message()
        if not reply or not reply.voice:
            return await event.edit("❌ Ответь на голосовое сообщение!")

        message = await event.edit("🎤 Обрабатываю...")

        file_path = await client.download_media(reply, "voice.ogg")
        audio_path = "voice.wav"

        try:
            AudioSegment.from_file(file_path).export(audio_path, format="wav")
            headers = {"Authorization": f"Bearer {WIT_AI_TOKEN}", "Content-Type": "audio/wav"}
            
            with open(audio_path, "rb") as audio_file:
                async with event.client.http.post(
                    "https://api.wit.ai/speech?v=20230216",
                    headers=headers,
                    data=audio_file,
                ) as response:
                    response_data = await response.text()

            os.remove(file_path)
            os.remove(wav_path)

            try:
                json_data = json.loads(response_text)
                transcripts = [item["text"] for item in json_data if "text" in item]
                result_text = " ".join(filter(None, set(texts)))

                if not result:
                    return await event.edit("❌ Не удалось распознать речь.")

                return await event.edit(f"🗣 {result}")

        except Exception as e:
            return await event.edit(f"❌ Ошибка обработки: {str(e)}")
