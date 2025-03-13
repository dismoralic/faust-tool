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
            audio.set_frame_rate(16000).set_channels(1).export(wav_path, format="wav")

            headers = {"Authorization": f"Bearer {WIT_AI_TOKEN}", "Content-Type": "audio/wav"}
            with open(wav_path, "rb") as f:
                response = requests.post("https://api.wit.ai/speech?v=20230216", headers=headers, data=f)

            os.remove(file_path)
            os.remove(wav_path)

            if response.status_code != 200:
                return await event.edit(f"❌ Ошибка: {response.status_code}\n{response.text}")

            json_data = response.text.strip().split("\n")
            texts = [json.loads(line).get("text", "") for line in json_data if line.strip()]
            longest_text = max(texts, key=len, default="❌ Текст не распознан")

            await event.edit(longest_text)

        except Exception as e:
            await event.edit(f"❌ Ошибка обработки: {str(e)}")
