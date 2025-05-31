import os
import requests
from requests.exceptions import RequestException
from urllib.parse import quote


def _make_twitch_request(url, headers):
    """Общая функция для запросов к Twitch API"""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        raise Exception(f"Twitch API error: {str(e)}")


def get_twitch_token():
    """Получение OAuth-токена с кэшированием"""
    auth_url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": os.getenv("TWITCH_CLIENT_ID"),
        "client_secret": os.getenv("TWITCH_CLIENT_SECRET"),
        "grant_type": "client_credentials"
    }
    return _make_twitch_request(auth_url, params={}, method="POST").get("access_token")


def get_streamer_id(login, headers):
    """Получение ID стримера по логину"""
    url = f"https://api.twitch.tv/helix/users?login={quote(login)}"
    data = _make_twitch_request(url, headers).get("data", [])
    return data[0]["id"] if data else None


def get_stream_status(streamer_login):
    """Получение полной информации о стриме"""
    token = get_twitch_token()
    if not token:
        return None

    headers = {
        "Client-ID": os.getenv("TWITCH_CLIENT_ID"),
        "Authorization": f"Bearer {token}"
    }

    streamer_id = get_streamer_id(streamer_login, headers)
    if not streamer_id:
        return None

    streams_url = f"https://api.twitch.tv/helix/streams?user_id={streamer_id}"
    streams_data = _make_twitch_request(streams_url, headers).get("data", [])

    return streams_data[0] if streams_data else None