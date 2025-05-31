from telegram import Bot
from telegram.constants import ParseMode
from api import get_stream_status
import os


def main():
    streamer = "zumich"
    status_manager = StreamStatusManager()

    last_status = status_manager.get_last_status()
    current_stream = get_stream_status(streamer)
    current_status = bool(current_stream)

    if current_status and not last_status:
        try:
            bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
            game_name = current_stream.get('game_name', 'Unknown Game')
            title = current_stream.get('title', 'No title')

            message = (
                f"🎮 <b>{streamer} начал стрим!</b>\n\n"
                f"🕹️ Игра: <b>{game_name}</b>\n"
                f"📺 Название: <i>{title}</i>\n\n"
                f"🔴 <a href='https://twitch.tv/{streamer}'>Смотреть на Twitch</a>"
            )

            bot.send_message(
                chat_id=os.getenv("TELEGRAM_CHANNEL"),
                text=message,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=False
            )
            print("Уведомление отправлено")
        except Exception as e:
            print(f"Ошибка отправки уведомления: {str(e)}")

    status_manager.save_status(current_status)
    print(f"Статус сохранен: {'online' if current_status else 'offline'}")