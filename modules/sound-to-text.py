import os
import requests
import asyncio
import speech_recognition as sr
from pydub import AudioSegment
from telethon import events

WIT_AI_TOKEN = "J2H26WNNL2SHNPN5YAIG3R3S6T34M62U"

def register(client):
    @client.on(events.NewMessage(pattern=".sound"))
    async def speech_to_text(event):
        reply = await event.get_reply_message()
        if not reply or not reply.media:
            return await event.reply("Ответь на голосовое или видео сообщение, чтобы распознать речь.")

        message = await event.reply("Обработка...")
        
        file_path = await client.download_media(reply, "voice.ogg")
        audio_path = "voice.wav"

        try:
            AudioSegment.from_file(file_path).export(audio_path, format="wav")

            with open(audio_path, "rb") as audio_file:
                headers = {"Authorization": f"Bearer {WIT_AI_TOKEN}", "Content-Type": "audio/wav"}
                response = requests.post("https://api.wit.ai/speech?v=20230228", headers=headers, data=audio_file)

            if response.status_code == 200:
                data = response.json()
                text = data.get("text", "Не удалось распознать речь.")
            else:
                text = f"Ошибка: {response.text}"

            await message.edit(f"🗣 {text}")

        except Exception as e:
            await message.edit(f"Ошибка: {str(e)}")

        finally:
            os.remove(file_path)
            os.remove(audio_path)
