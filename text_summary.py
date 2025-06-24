import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# トークン読み込み
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ① Slackのメッセージ（仮の例。実際はSlack APIで取得）
messages = [
    "昨日、プロジェクトXの進捗確認を行いました。",
    "次回のミーティングは来週月曜10時です。",
    "バグ報告：ログイン画面でエラーが出ています。"
]

# ② 要約処理
def summarize_messages(messages):
    text = "\n".join(messages)
    print("🔍 GPTに渡す内容:\n", text)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "あなたはSlackの会話を要約する秘書です。簡潔に、敬語で、今日のラジオの冒頭挨拶のようにまとめてください。"},
            {"role": "user", "content": text}
        ],
        temperature=0.7
    )

    summary = response.choices[0].message.content
    print("📝 要約結果:\n", summary)
    return summary

# ③ Slackに投稿
def post_to_slack(text):
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    payload = {
        "channel": CHANNEL_ID,
        "text": text
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200 or not response.json().get('ok'):
        print("⚠️ 投稿に失敗しました:", response.json())
    else:
        print("✅ 投稿成功:", response.json()['message']['text'])

# 実行フロー
if __name__ == "__main__":
    summary = summarize_messages(messages)
    post_to_slack(summary)
