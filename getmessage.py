import os
import requests
from dotenv import load_dotenv

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

url = "https://slack.com/api/conversations.history"
headers = {
    "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
}
params = {
    "channel": CHANNEL_ID,
    "limit": 5  # 最新5件だけ取得
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

for message in data.get("messages", []):
    print(f"[{message.get('ts')}] {message.get('text')}")
