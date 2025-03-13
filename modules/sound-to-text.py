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
            return await event.edit("❌ Ответь на голосовое сообщение.")

        await event.edit("⏳ Распознаю речь...")

        try:

            file_path = await client.download_media(reply.media, "audio.ogg")

            audio = AudioSegment.from_file(file_path, format="ogg")
            wav_path = file_path.replace(".ogg", ".wav")
            audio.export(wav_path, format="wav", parameters=["-ac", "1", "-ar", "16000", "-sample_fmt", "s16"])

            headers = {
                "Authorization": f"Bearer {WIT_AI_TOKEN}",
                "Content-Type": "audio/wav"
            }

            with open(wav_path, "rb") as audio_file:
                response = requests.post("https://api.wit.ai/speech?v=20230201", headers=headers, data=audio_file)

            os.remove(file_path)
            os.remove(wav_path)

            if response.status_code != 200:
                return await event.edit(f"❌ Ошибка {response.status_code}: {response.text}")

            valid_json_lines = [line for line in response.text.strip().split("\n") if line.strip().startswith("{")]
            texts = [json.loads(line).get("text", "") for line in valid_json_lines if line]

            longest_text = max(texts, key=len) if texts else "❌ Ничего не распознано."

        except Exception as e:
            longest_text = f"❌ Ошибка обработки: {str(e)}"

        await event.edit(longest_text)
