import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta, timezone

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

JST = timezone(timedelta(hours=9))
now = datetime.now(JST)

start_ts = now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
end_ts = now.replace(hour=23, minute=59, second=59, microsecond=0).timestamp()

headers = {
    "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
}

params = {
    "channel": CHANNEL_ID,
    "oldest": str(start_ts),
    "latest": str(end_ts),
    "inclusive": True,
    "limit": 100
}

response = requests.get("https://slack.com/api/conversations.history", headers=headers, params=params)
data = response.json()

print("API Response:", data)

if data.get("ok") and data.get("messages"):
    for msg in data["messages"]:
        print("📝 投稿:", msg.get("text"))
else:
    print("⚠️ メッセージが取得できませんでした。エラー内容:", data.get("error"))