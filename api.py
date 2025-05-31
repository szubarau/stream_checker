import os
import requests
from requests.exceptions import RequestException


def get_twitch_token():
    """Получение OAuth-токена Twitch"""
    try:
        auth_url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": os.getenv("TWITCH_CLIENT_ID"),
            "client_secret": os.getenv("TWITCH_CLIENT_SECRET"),
            "grant_type": "client_credentials"
        }
        response = requests.post(auth_url, params=params)
        response.raise_for_status()
        return response.json().get("access_token")
    except Exception as e:
        print(f"Ошибка получения токена: {str(e)}")
        return None


def get_stream_status(streamer_name):
    """Проверка статуса стрима с обработкой ошибок"""
    try:
        token = get_twitch_token()
        if not token:
            return None

        headers = {
            "Client-ID": os.getenv("TWITCH_CLIENT_ID"),
            "Authorization": f"Bearer {token}"
        }

        # Получаем ID пользователя
        users_url = f"https://api.twitch.tv/helix/users?login={streamer_name}"
        users_response = requests.get(users_url, headers=headers)
        users_response.raise_for_status()
        user_data = users_response.json().get('data', [])

        if not user_data:
            print(f"Стример {streamer_name} не найден")
            return None

        user_id = user_data[0]['id']

        # Проверяем стрим
        streams_url = f"https://api.twitch.tv/helix/streams?user_id={user_id}"
        streams_response = requests.get(streams_url, headers=headers)
        streams_response.raise_for_status()
        stream_data = streams_response.json().get('data', [])

        return stream_data[0] if stream_data else None

    except Exception as e:
        print(f"Ошибка проверки стрима: {str(e)}")
        return None