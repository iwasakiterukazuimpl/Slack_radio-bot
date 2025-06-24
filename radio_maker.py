import os
from gtts import gTTS
from dotenv import load_dotenv
from slack_sdk import WebClient
import requests

# ✅ 環境変数の読み込み
load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# ✅ 要約されたテキスト（ダミー）
summary_text = """
おはようございます。昨日はプロジェクトXの進捗確認が行われました。
ログイン画面にバグが見つかり、対応が必要です。
次回のミーティングは来週月曜の10時です。
"""

# ✅ gTTSで音声ファイル作成
tts = gTTS(text=summary_text, lang='ja')
audio_filename = "summary.mp3"
tts.save(audio_filename)
print(f"✅ 音声ファイルを保存しました: {audio_filename}")

# ✅ Slackにファイル投稿 (multipart/form-data形式)
with open(audio_filename, "rb") as file:
    client = WebClient(token=SLACK_BOT_TOKEN)

try:
    response = client.files_upload_v2(
        channel=CHANNEL_ID,
        file=audio_filename,
        title="ラジオまとめ",
        initial_comment="🎧 今日の音声まとめです！"
    )
    print("✅ Slackに音声ファイルを投稿しました！")
except Exception as e:
    print("❌ エラーが発生しました:", str(e))
