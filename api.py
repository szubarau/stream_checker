import os
import requests
from requests.exceptions import RequestException


def get_twitch_token():
    try:
        auth_url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": os.getenv("TWITCH_CLIENT_ID"),
            "client_secret": os.getenv("TWITCH_CLIENT_SECRET"),
            "grant_type": "client_credentials"
        }
        response = requests.post(auth_url, params=params)
        response.raise_for_status()
        return response.json()["access_token"]
    except (RequestException, KeyError) as e:
        print(f"Ошибка получения токена: {str(e)}")
        return None


def get_stream_status(streamer_name):
    try:
        token = get_twitch_token()
        if not token:
            return False

        headers = {
            "Client-ID": os.getenv("TWITCH_CLIENT_ID"),
            "Authorization": f"Bearer {token}"
        }
        url = f"https://api.twitch.tv/helix/streams?user_login={streamer_name}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        return bool(data.get("data", []))

    except (RequestException, KeyError) as e:
        print(f"Ошибка проверки стрима: {str(e)}")
        return False