import aiohttp

async def get_access_token(client_id: str, client_secret: str) -> str:
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params) as resp:
            data = await resp.json()
            if "access_token" not in data:
                raise Exception(f"Could not get access token: {data}")
            return data["access_token"]

async def is_stream_live(client_id: str, client_secret: str, user_login: str) -> bool:
    token = await get_access_token(client_id, client_secret)
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}"
    }
    url = f"https://api.twitch.tv/helix/streams?user_login={user_login}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            data = await resp.json()
            if "data" not in data:
                raise Exception(f"Invalid Twitch API response: {data}")
            return len(data["data"]) > 0

