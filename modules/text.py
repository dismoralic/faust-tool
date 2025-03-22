import pytesseract
from PIL import Image
from io import BytesIO
from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.text$', outgoing=True))
    async def recognize_text(event):
        await event.edit('Обрабатываю..')
        
        if event.reply_to and (reply_msg := await event.get_reply_message()):
            if reply_msg.photo or reply_msg.sticker or reply_msg.file:
                try:
                    image = await client.download_media(reply_msg, bytes)
                    text = pytesseract.image_to_string(Image.open(BytesIO(image)), lang='eng+rus')
                    await event.edit(text or 'Текст не распознан.')
                except Exception as e:
                    await event.edit(f'Ошибка распознавания: {e}')
            else:
                await event.edit('Ответь на изображение или стикер.')
        else:
            await event.edit('Команда работает только в ответ на изображение.')