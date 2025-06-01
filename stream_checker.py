import asyncio
from stream_status import is_stream_live
from bot import send_telegram_message

PREVIOUS_STATUS = False


async def main(client_id: str, client_secret: str, user_login: str, bot_token: str, chat_id: str):
    global PREVIOUS_STATUS
    while True:
        try:
            is_live = await is_stream_live(client_id, client_secret, user_login)
            if is_live and not PREVIOUS_STATUS:
                await send_telegram_message(bot_token, chat_id, f"🎥 Стрим на канале <b>{user_login}</b> начался!")
                PREVIOUS_STATUS = True
            elif not is_live:
                PREVIOUS_STATUS = False
        except Exception as e:
            print(f"[ERROR] {e}")
        await asyncio.sleep(60)


if __name__ == "__main__":
    import os

    client_id = os.environ["TWITCH_CLIENT_ID"]
    client_secret = os.environ["TWITCH_CLIENT_SECRET"]
    user_login = os.environ["TWITCH_USER_LOGIN"]
    bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHANNEL"]

    asyncio.run(main(client_id, client_secret, user_login, bot_token, chat_id))
