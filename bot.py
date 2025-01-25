import requests
from typing import Literal

class Bot:
    def __init__(self) -> None:
        pass
    
    def check_presence(self, user_id: int) -> Literal['offline'] | Literal['online'] | Literal['gaming'] | Literal['unknown']:
        json = {
            "userIds": [
                user_id
            ]
        }

        response = requests.post('https://presence.roblox.com/v1/presence/users', json=json)

        if response.ok:
            presence_type = response.json()["userPresences"][0]["userPresenceType"]
            if presence_type == 0:
                return "offline"
            elif presence_type == 1:
                return "online"
            elif presence_type == 2:
                return "gaming"
            else:
                return "unknown"
        else:
            raise Exception(f"Error occurred. Status code: {response.status_code}. Text: {response.text}")
        
    def get_id_from_username(self, username: str) -> int:
        params = {
            "keyword": username
        }

        response = requests.get("https://users.roblox.com/v1/users/search", params=params)
        if response.ok:
            json = response.json()
            user_id = json['data'][0]['id']
            return user_id
        else:
            raise Exception(f"Error occurred. Status code: {response.status_code}. Text: {response.text}")
        