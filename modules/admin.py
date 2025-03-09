from telethon import events
import json
import asyncio

WARN_FILE = "warnings.txt"

try:
    with open(WARN_FILE, "r") as f:
        warnings = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    warnings = {}

def save_warnings():
    with open(WARN_FILE, "w") as f:
        json.dump(warnings, f)

def register(client):
    @client.on(events.NewMessage(pattern=r"\.(mute|ban|kick|unban|unmute|warn|unwarn|admin help)", outgoing=True))
    async def moderation_handler(event):
        command = event.pattern_match.group(1)
        chat_id = str(event.chat_id)
        
        if command == "admin help":
            help_text = (
                "**Админ-команды:**\n"
                "`.mute <время в минутах> <причина>` – замутить пользователя (если не указано время — мут бессрочный).\n"
                "`.ban <время в минутах> <причина>` – забанить пользователя (если не указано время — бан бессрочный).\n"
                "`.kick <причина>` – кикнуть пользователя.\n"
                "`.unban` – разбанить пользователя.\n"
                "`.unmute` – размутить пользователя.\n"
                "`.warn <причина>` – выдать предупреждение. 3 варна = бан.\n"
                "`.unwarn` – снять одно предупреждение."
            )
            await event.edit(help_text)
            return

        reply = await event.get_reply_message()
        if not reply:
            await event.edit("Ответь на сообщение пользователя!")
            return

        user_id = str(reply.sender_id)
        user_mention = f"[{reply.sender.first_name}](tg://user?id={user_id})"

        args = event.message.text.split()[1:]
        duration = None
        reason = None

        if args:
            if args[0].isdigit():
                duration = int(args[0])
                reason = " ".join(args[1:]) if len(args) > 1 else None
            else:
                reason = " ".join(args)

        if command == "mute":
            await event.client.edit_permissions(event.chat_id, int(user_id), send_messages=False)
            response = f"{user_mention} замучен"
            if duration:
                response += f" на {duration} минут"
            if reason:
                response += f". Причина: {reason}"
            response += "."
            if duration:
                await asyncio.sleep(duration * 60)
                await event.client.edit_permissions(event.chat_id, int(user_id), send_messages=True)
        elif command == "ban":
            await event.client.kick_participant(event.chat_id, int(user_id))
            response = f"{user_mention} забанен"
            if duration:
                response += f" на {duration} минут"
            if reason:
                response += f". Причина: {reason}"
            response += "."
            if duration:
                await asyncio.sleep(duration * 60)
                await event.client.edit_permissions(event.chat_id, int(user_id), send_messages=True)
        elif command == "kick":
            await event.client.kick_participant(event.chat_id, int(user_id))
            response = f"{user_mention} кикнут"
            if reason:
                response += f". Причина: {reason}"
            response += "."
        elif command == "unban":
            await event.client.edit_permissions(event.chat_id, int(user_id), send_messages=True)
            response = f"{user_mention} разбанен."
        elif command == "unmute":
            await event.client.edit_permissions(event.chat_id, int(user_id), send_messages=True)
            response = f"{user_mention} размучен."
        elif command == "warn":
            if chat_id not in warnings:
                warnings[chat_id] = {}
            if user_id not in warnings[chat_id]:
                warnings[chat_id][user_id] = []
            warnings[chat_id][user_id].append(reason if reason else "Без причины")
            save_warnings()
            if len(warnings[chat_id][user_id]) >= 3:
                await event.client.kick_participant(event.chat_id, int(user_id))
                response = f"{user_mention} получил 3 предупреждения и был забанен."
                del warnings[chat_id][user_id]
                save_warnings()
            else:
                response = f"{user_mention} получил предупреждение ({len(warnings[chat_id][user_id])}/3)"
                if reason:
                    response += f". Причина: {reason}"
                response += "."
        elif command == "unwarn":
            if chat_id in warnings and user_id in warnings[chat_id] and warnings[chat_id][user_id]:
                warnings[chat_id][user_id].pop()
                save_warnings()
                response = f"{user_mention} снято одно предупреждение ({len(warnings[chat_id][user_id])}/3)."
            else:
                response = f"{user_mention} не имеет предупреждений."

        await event.edit(response)
