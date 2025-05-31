import os
import logging
from datetime import datetime
from telegram import Bot
from telegram.constants import ParseMode
from api import get_stream_status
from stream_status import StreamStatusManager

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def format_stream_message(streamer, stream_data):
    """Форматирование сообщения о начале стрима"""
    game = stream_data.get('game_name', 'Игра не указана')
    title = stream_data.get('title', 'Без названия')
    viewers = stream_data.get('viewer_count', 0)
    started_at = stream_data.get('started_at', '')

    try:
        start_time = datetime.strptime(started_at, '%Y-%m-%dT%H:%M:%SZ')
        time_str = start_time.strftime('%H:%M UTC')
    except (ValueError, TypeError):
        time_str = 'время неизвестно'

    return (
        f"🎮 <b>{streamer} начал стрим!</b>\n\n"
        f"🕹️ Игра: <b>{game}</b>\n"
        f"📺 Название: <i>{title}</i>\n"
        f"👀 Зрителей: <b>{viewers}</b>\n"
        f"⏱ Начало: <b>{time_str}</b>\n\n"
        f"🔴 <a href='https://twitch.tv/{streamer}'>Смотреть на Twitch</a>"
    )


def send_telegram_notification(message):
    """Отправка уведомления в Telegram"""
    try:
        bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
        bot.send_message(
            chat_id=os.getenv("TELEGRAM_CHANNEL"),
            text=message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False
        )
        logger.info("Уведомление успешно отправлено")
    except Exception as e:
        logger.error(f"Ошибка отправки в Telegram: {str(e)}")


def main():
    logger.info("=== Запуск проверки стрима ===")

    streamer = "zumich"  # Замените на нужного стримера
    status_manager = StreamStatusManager()

    try:
        # Получаем статусы
        last_status, _ = status_manager.get_last_status()
        current_stream = get_stream_status(streamer)
        current_status = bool(current_stream)

        logger.info(
            f"Статус стрима: был {'online' if last_status else 'offline'}, сейчас {'online' if current_status else 'offline'}")

        # Отправляем уведомление при начале стрима
        if current_status and not last_status:
            message = format_stream_message(streamer, current_stream)
            send_telegram_notification(message)

        # Сохраняем новый статус
        status_manager.save_status(current_status)
        logger.info("Статус успешно сохранен")

    except Exception as e:
        logger.error(f"Критическая ошибка: {str(e)}", exc_info=True)
        raise

    logger.info("=== Проверка завершена ===")


if __name__ == "__main__":
    main()