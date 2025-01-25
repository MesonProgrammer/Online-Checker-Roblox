from bot import Bot
import time
from plyer import notification
import winsound

def online_sound() -> None:
    winsound.Beep(1000, 1000)
    time.sleep(1)
    winsound.Beep(1000, 1000)

def gaming_sound() -> None:
    for _ in range(5):
        winsound.Beep(2000, 500)
        time.sleep(0.25)

def alarm(username: str, presence: str) -> None:
    if presence == 'unknown':
        return
    
    if presence == 'offline':
        text = f"**INFO**\n{username} is offline."
    else:
        if presence == 'online':
            online_sound()
        elif presence == 'gaming':
            gaming_sound()

        text = f"**ALARM** **ALARM**\n{username} is {presence.upper()}!!!"
    
    print(text+'\n')
    notification.notify(
        title=f"Info about {username}",
        message=text,
        timeout=10
    )

def terminal() -> None:
    bot = Bot()

    users = {}
    print("Select users ('q' to finish)")
    while True:
        username = input(f"Enter username (Users in list: {len(users)}): ").strip()
        if not username:
            print("Username cannot be empty.")
        
        if username.lower() == 'q':
            break
        
        try:
            user_id = bot.get_id_from_username(username)
        except Exception as e:
            print(f"An error occurred when verifying the username. Ensure it exists and that you have a stable WiFi connection.\nMore info about the error:\n{e}")
            continue

        users[user_id] = username
    
    if len(users) == 0:
        print("No users in list. Exiting program.")
        return
    
    sound = input("Enable sound? [Y/n]").strip()
    if sound.lower() == 'n':
        sound = False
    else:
        sound = True
    
    try:
        while True:
            for user_id, username in users.items():
                presence = bot.check_presence(user_id)
                alarm(username, presence)

                # Wait 30 seconds to prevent too many requests
                time.sleep(30)
    except KeyboardInterrupt:
        print("Program terminated via Keyboard Interrupt.")

if __name__ == '__main__':
    print("Welcome to the Online Checker for Roblox!")
    mode = input("Would you like to use the terminal or the GUI?\n1. Terminal\n2. GUI (WORK IN PROGRESS)\n> ").strip()
    if mode == "1":
        terminal()
