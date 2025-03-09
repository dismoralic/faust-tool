import asyncio
from telethon import events
from googletrans import Translator, LANGUAGES

def register(client):
    translator = Translator()
    active_translations = {}

    @client.on(events.NewMessage(pattern=r"\.trns on (\w+)"))
    async def translate_on(event):
        lang_code = event.pattern_match.group(1)
        if lang_code not in LANGUAGES:
            await event.edit("❌ Неверный код языка!")
            return
        active_translations[event.sender_id] = lang_code
        await event.edit(f"✅ Перевод включен на {LANGUAGES[lang_code].capitalize()}.")

    @client.on(events.NewMessage(pattern=r"\.trns list"))
    async def translate_list(event):
        lang_list = "\n".join([f"`{code}` - {name.capitalize()}" for code, name in LANGUAGES.items()])
        await event.edit(f"🌍 **Доступные языки:**\n\n{lang_list}")

    @client.on(events.NewMessage(pattern=r"\.trns help"))
    async def translate_help(event):
        help_text = (
            "📖 **Команды переводчика:**\n"
            "`.trns on <код_языка>` - Включает автоматический перевод на указанный язык.\n"
            "`.trns off` - Отключает автоматический перевод.\n"
            "`.trns list` - Показывает список доступных языков.\n"
            "`.trns help` - Показывает это сообщение."
        )
        await event.edit(help_text)

    @client.on(events.NewMessage)
    async def auto_translate(event):
        if event.sender_id in active_translations and event.text and not event.text.startswith("."):
            lang = active_translations[event.sender_id]

            if event.out:
                try:
                    translated = await translator.translate(event.text, dest=lang)
                    if translated and translated.src and translated.src != lang:
                        await event.edit(translated.text)
                except Exception as e:
                    await event.reply(f"⚠ Ошибка перевода: {e}")

    @client.on(events.NewMessage(pattern=r"\.trns off"))
    async def translate_off(event):
        if event.sender_id in active_translations:
            del active_translations[event.sender_id]
            await event.edit("Перевод отключен.")
