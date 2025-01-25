import os
from dotenv import load_dotenv
import requests
from typing import Literal

load_dotenv()
COOKIE = os.getenv("COOKIE")

class Bot:
    def __init__(self) -> None:
        self.xcsrf_token = self.get_xcsrf_token()

    def get_xcsrf_token(self) -> str:
        headers = {
            'cookie': COOKIE
        }

        response = requests.post('https://auth.roblox.com/v2/logout', headers=headers)

        x_csrf_token = response.headers.get('x-csrf-token', '')

        return x_csrf_token
    
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

def check_env() -> None:
    # Checks if the .env file exists
    if os.path.exists('.env'):
        return
    
    # If it doesn't it will proceed to generate the file
    print("No .env file exists. Proceeding with .env file generation protocol.")
    
    # Allows input for the cookie
    while True:
        cookie = input("Insert cookie here: ").strip()
        if cookie: break
        print("Cookie cannot be empty. Try again.")

    # Ensures the cookie starts with ".ROBLOSECURITY="
    if not cookie.startswith(".ROBLOSECURITY="):
        cookie = ".ROBLOSECURITY=" + cookie
    
    # Writes the cookie content into the new .env file
    try:
        with open('.env', 'w') as f:
            f.write(f"COOKIE={cookie}")
    except Exception as e:
        print(f"An error occurred while creating the .env file: {e}")

if __name__ == '__main__':
    check_env()
    bot = Bot()
