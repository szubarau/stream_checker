import os
import requests
import json

def get_twitch_token():
    auth_url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": os.getenv("TWITCH_CLIENT_ID"),
        "client_secret": os.getenv("TWITCH_CLIENT_SECRET"),
        "grant_type": "client_credentials"
    }
    response = requests.post(auth_url, params=params).json()
    return response["access_token"]

def check_stream(streamer_name):
    token = get_twitch_token()
    headers = {
        "Client-ID": os.getenv("TWITCH_CLIENT_ID"),
        "Authorization": f"Bearer {token}"
    }
    url = f"https://api.twitch.tv/helix/streams?user_login={streamer_name}"
    response = requests.get(url, headers=headers).json()
    return bool(response["data"])

def load_last_status():
    try:
        with open("last_status.json", "r") as f:
            return json.load(f).get("is_live", False)
    except FileNotFoundError:
        return False

def save_last_status(is_live):
    with open("last_status.json", "w") as f:
        json.dump({"is_live": is_live}, f)