from telethon import events
from telethon.tl.functions.messages import DeleteHistoryRequest

def register(client):
    @client.on(events.NewMessage(outgoing=True, pattern=r"^\.voice"))
    async def test_command(event):
        if event.reply_to_msg_id:
            reply_msg = await event.get_reply_message()
            status_msg = await event.edit("Обрабатываю...")
            client._last_test_msg = status_msg
            await client.send_message("@smartspeech_sber_bot", reply_msg)
        else:
            await event.edit("Ответь на голосовое или видеосообщение, чтобы обработать его в речь.")

    @client.on(events.NewMessage(from_users="@smartspeech_sber_bot"))
    async def forward_response(event):
        if hasattr(client, "_last_test_msg") and client._last_test_msg:
            await client._last_test_msg.edit(event.text)
            client._last_test_msg = None

        await client(DeleteHistoryRequest(peer="@smartspeech_sber_bot", max_id=0, just_clear=False))
