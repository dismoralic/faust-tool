import os
from telethon import events

OWNER_ID = 6279401007
BLACKLIST_FILE = "blacklist.txt"

def load_blacklist():
    if not os.path.exists(BLACKLIST_FILE):
        return set()
    with open(BLACKLIST_FILE, "r") as f:
        return set(map(int, f.read().splitlines()))

def save_blacklist(blacklist):
    with open(BLACKLIST_FILE, "w") as f:
        f.write("\n".join(map(str, blacklist)))

def register(client):
    blacklist = load_blacklist()

    @client.on(events.NewMessage)
    async def check_blacklist(event):
        if event.sender_id in blacklist:
            await event.respond("Вы были забанены! Обратитесь к владельцу бота.")
            return

    @client.on(events.NewMessage(pattern=r"^\.block (\d+)$", outgoing=True))
    async def block_user(event):
        if event.sender_id != OWNER_ID:
            return
        
        target_id = int(event.pattern_match.group(1))
        if target_id not in blacklist:
            blacklist.add(target_id)
            save_blacklist(blacklist)
            await event.reply(f"Пользователь `{target_id}` заблокирован.")

    @client.on(events.NewMessage(pattern=r"^\.unblock (\d+)$", outgoing=True))
    async def unblock_user(event):
        if event.sender_id != OWNER_ID:
            return
        
        target_id = int(event.pattern_match.group(1))
        if target_id in blacklist:
            blacklist.remove(target_id)
            save_blacklist(blacklist)
            await event.reply(f"Пользователь `{target_id}` разблокирован.")
