from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r"\.(mute|ban|kick|unban|unmute)", outgoing=True))
    async def moderation_handler(event):
        command = event.pattern_match.group(1)
        reply = await event.get_reply_message()

        if not reply:
            await event.edit("Ответь на сообщение пользователя!")
            return

        user_id = reply.sender_id
        user_mention = f"[{reply.sender.first_name}](tg://user?id={user_id})"

        args = event.message.text.split()[1:]
        duration = None
        reason = None

        if args:
            try:
                duration = int(args[0])
                reason = " ".join(args[1:]) if len(args) > 1 else None
            except ValueError:
                reason = " ".join(args)

        if command == "mute":
            await event.client.edit_permissions(event.chat_id, user_id, send_messages=False)
            response = f"{user_mention} замучен{' на ' + str(duration) + ' минут' if duration else ''}{' по причине: ' + reason if reason else ''}."
        elif command == "ban":
            await event.client.kick_participant(event.chat_id, user_id)
            response = f"{user_mention} забанен{' на ' + str(duration) + ' минут' if duration else ''}{' по причине: ' + reason if reason else ''}."
        elif command == "kick":
            await event.client.kick_participant(event.chat_id, user_id)
            response = f"{user_mention} кикнут."
        elif command == "unban":
            await event.client.edit_permissions(event.chat_id, user_id, send_messages=True)
            response = f"{user_mention} разбанен."
        elif command == "unmute":
            await event.client.edit_permissions(event.chat_id, user_id, send_messages=True)
            response = f"{user_mention} размучен."

        await event.edit(response)