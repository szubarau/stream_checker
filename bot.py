import os
import requests
from stream_checker import check_stream, load_last_status, save_last_status


def send_notification(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHANNEL")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    })


def main():
    STREAMER = "zumich"
    last_status = load_last_status()
    current_status = check_stream(STREAMER)

    if current_status and not last_status:
        send_notification(
            f"🎮 <b>{STREAMER} начал стрим!</b>\n"
            f"🔴 Смотрите здесь: https://twitch.tv/{STREAMER}"
        )

    save_last_status(current_status)


if __name__ == "__main__":
    main()