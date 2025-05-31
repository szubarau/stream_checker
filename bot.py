from telegram import Bot
from telegram.constants import ParseMode
from api import get_stream_status
import os


def main():
    streamer = "zumich"
    status_manager = StreamStatusManager()

    was_live = status_manager.get_last_status()
    is_live = get_stream_status(streamer)

    if is_live and not was_live:
        bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
        message = (
            f"🎮 <b>{streamer} начал стрим!</b>\n\n"
            f"🔴 Смотрите здесь: https://twitch.tv/{streamer}"
        )
        bot.send_message(
            chat_id=os.getenv("TELEGRAM_CHANNEL"),
            text=message,
            parse_mode=ParseMode.HTML
        )

    status_manager.save_status(is_live)


if __name__ == "__main__":
    main()