from telethon import events
from telethon.tl.functions.channels import JoinChannelRequest, JoinChannelRequest

def register(client):
    async def join_faust_chats():
        await client.connect()
        chat_usernames = ["faust_tool_chat", "bio_faust"]
        for chat in chat_usernames:
            try:
                await client(JoinChannelRequest(chat))
            except Exception:
                pass
    
    client.loop.run_until_complete(join_faust_chats())