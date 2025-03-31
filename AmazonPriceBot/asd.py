# CODERPSYCHO #
# https://coderpsycho.psychotr.com/

# Burda da aynı şekilde mesaj almak istediğiniz telegram API giriniz ( Here, in the same way, enter the telegram API you want to receive messages from )

import requests

TELEGRAM_TOKEN = ""
API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

def get_chat_id():
    response = requests.get(f"{API_URL}getUpdates")
    updates = response.json()
    
    if updates.get("result"):
        chat_id = updates["result"][0]["message"]["chat"]["id"]
        print(f"Chat ID'niz: {chat_id}")
    else:
        print("Henüz mesaj almadınız.")
get_chat_id()
