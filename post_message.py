import os
import requests
from dotenv import load_dotenv

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
MESSAGE_TEXT = "こんにちは！これはBotからのメッセージです。"

url = "https://slack.com/api/chat.postMessage"
headers = {
    "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    "Content-type": "application/json"
}
data = {
    "channel": CHANNEL_ID,
    "text": MESSAGE_TEXT
}

response = requests.post(url, headers=headers, json=data)
print(response.json())