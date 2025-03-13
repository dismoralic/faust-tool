import os
import requests
import json
from pydub import AudioSegment
from telethon import events

WIT_AI_TOKEN = "J2H26WNNL2SHNPN5YAIG3R3S6T34M62U"

def register(client):
    @client.on(events.NewMessage(pattern=".sound"))
    async def speech_to_text(event):
        reply = await event.get_reply_message()
        if not reply or not reply.media:
            return await event.reply("Ответь на голосовое или видео, чтобы распознать речь.")

        message = await event.reply("⏳ Распознаю речь...")

        file_path = await client.download_media(reply.media, "audio.ogg")

        audio = AudioSegment.from_file(file_path, format="ogg")
        wav_path = file_path.replace(".ogg", ".wav")
        audio.export(wav_path, format="wav")

        headers = {
            "Authorization": f"Bearer {WIT_AI_TOKEN}",
            "Content-Type": "audio/wav"
        }

        with open(wav_path, "rb") as audio_file:
            response = requests.post("https://api.wit.ai/speech?v=20230201", headers=headers, data=audio_file)

        os.remove(file_path)
        os.remove(wav_path)

        try:
            texts = [json.loads(chunk)["text"] for chunk in response.text.strip().split("\n") if chunk]
            longest_text = max(texts, key=len) if texts else "Не удалось распознать речь."
        except Exception:
            longest_text = "Ошибка обработки ответа от Wit.ai."

        await message.edit(longest_text)
