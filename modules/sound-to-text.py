import os
import asyncio
import speech_recognition as sr
from pydub import AudioSegment
from telethon import events
from telethon.tl.types import MessageMediaDocument

def register(client):
    @client.on(events.NewMessage(pattern=".sound"))
    async def speech_to_text(event):
        reply = await event.get_reply_message()
        if not reply or not reply.media:
            return await event.reply("Ответь на голосовое или видео, чтобы распознать речь.")
        
        file_path = await client.download_media(reply, "voice.ogg")
        audio_path = "voice.wav"
        
        try:
            AudioSegment.from_file(file_path).export(audio_path, format="wav")
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language="ru-RU")
            await event.reply(f"Распознанный текст: {text}")
        except Exception as e:
            await event.reply(f"Ошибка: {str(e)}")
        finally:
            os.remove(file_path)
            os.remove(audio_path)
            await event.delete()

