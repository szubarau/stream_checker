import os
import logging
from datetime import datetime
from telegram import Bot, InputMediaPhoto
from telegram.constants import ParseMode
from api import get_stream_status
from stream_status import StreamStatusManager

# Конфигурация логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class NotificationSender:
    def __init__(self):
        self.bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
        self.chat_id = os.getenv("TELEGRAM_CHANNEL")

    def _prepare_message(self, streamer, stream_data):
        """Подготовка сообщения с красивым форматированием"""
        game = stream_data.get('game_name', 'Игра не указана')
        title = stream_data.get('title', 'Без названия')
        viewers = stream_data.get('viewer_count', 0)

        # Форматирование времени начала
        try:
            start_time = datetime.strptime(stream_data['started_at'], '%Y-%m-%dT%H:%M:%SZ')
            time_str = start_time.strftime('%H:%M UTC')
        except (KeyError, ValueError):
            time_str = 'время неизвестно'

        return (
            f"🎮 <b>{streamer} начал стрим!</b>\n\n"
            f"🕹️ Игра: <b>{game}</b>\n"
            f"📺 Название: <i>{title}</i>\n"
            f"👀 Зрителей: <b>{viewers:,}</b>\n"
            f"⏱ Начало: <b>{time_str}</b>\n\n"
            f"🔴 <a href='https://twitch.tv/{streamer}'>Смотреть на Twitch</a>"
        )

    def _prepare_thumbnail(self, thumbnail_url):
        """Подготовка URL превью"""
        if not thumbnail_url:
            return None
        return thumbnail_url.replace('{width}', '1280').replace('{height}', '720')

    def send(self, streamer, stream_data):
        """Отправка уведомления"""
        try:
            message = self._prepare_message(streamer, stream_data)
            thumbnail = self._prepare_thumbnail(stream_data.get('thumbnail_url'))

            if thumbnail:
                self.bot.send_photo(
                    chat_id=self.chat_id,
                    photo=thumbnail,
                    caption=message,
                    parse_mode=ParseMode.HTML
                )
            else:
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text=message,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=False
                )

            logger.info(f"Уведомление для {streamer} отправлено")
            return True

        except Exception as e:
            logger.error(f"Ошибка отправки: {str(e)}", exc_info=True)
            return False


def main():
    logger.info("=== Старт мониторинга ===")

    streamer = "zumich"  # Замените на нужного стримера
    notifier = NotificationSender()
    status_manager = StreamStatusManager()

    try:
        # Получаем статусы
        last_status = status_manager.get_last_status()
        current_stream = get_stream_status(streamer)
        current_status = bool(current_stream)

        logger.info(
            f"Статус {streamer}: был {'online' if last_status else 'offline'}, сейчас {'online' if current_status else 'offline'}")

        # Отправляем уведомление при начале стрима
        if current_status and not last_status:
            notifier.send(streamer, current_stream)

        # Сохраняем статус
        status_manager.save_status(current_status)

    except Exception as e:
        logger.error(f"Критическая ошибка: {str(e)}", exc_info=True)
        raise

    logger.info("=== Мониторинг завершен ===")


if __name__ == "__main__":
    main()