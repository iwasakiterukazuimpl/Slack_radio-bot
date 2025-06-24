#!/usr/bin/env python3
"""
Slack Radio Bot - 統合版
前日のSlack投稿を取得し、ラジオ風に要約して音声ファイルを作成・投稿するボット
"""

import os
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from gtts import gTTS
from slack_sdk import WebClient
from openai import OpenAI

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
else:
    openai_client = None

def fetch_yesterday_messages():
    """前日のSlackメッセージを取得する"""
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    yesterday = now - timedelta(days=1)
    
    start_ts = yesterday.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    end_ts = yesterday.replace(hour=23, minute=59, second=59, microsecond=0).timestamp()
    
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
    
    if data.get("ok") and data.get("messages"):
        messages = [msg.get("text", "") for msg in data["messages"] if msg.get("text")]
        return messages
    else:
        print("⚠️ メッセージが取得できませんでした。エラー内容:", data.get("error"))
        return []

def create_radio_summary(messages):
    """メッセージをラジオ風に要約する"""
    if not messages:
        return "昨日は特に投稿がありませんでした。"
    
    if not openai_client:
        print("⚠️ OpenAI API キーが設定されていません。")
        return "OpenAI API キーが設定されていないため、要約を生成できません。"
    
    messages_text = "\n".join(messages)
    
    prompt = f"""
あなたは人気ラジオDJです。以下のSlackチャンネルの昨日の投稿内容を、明るく親しみやすいラジオ番組風に要約してください。

投稿内容:
{messages_text}

要約のポイント:
- ラジオDJ風の明るい口調で
- 重要な情報は漏らさずに
- 聞き手が興味を持つような構成で
- 日本語で自然な話し言葉で
- 「おはようございます」で始めて、「それでは良い一日を！」で終わる

要約:
"""
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ OpenAI API エラー: {str(e)}")
        return "申し訳ございません。要約の生成中にエラーが発生しました。"

def generate_audio(summary_text):
    """要約テキストを音声ファイルに変換する"""
    try:
        tts = gTTS(text=summary_text, lang='ja')
        audio_filename = f"radio_summary_{datetime.now().strftime('%Y%m%d')}.mp3"
        tts.save(audio_filename)
        print(f"✅ 音声ファイルを保存しました: {audio_filename}")
        return audio_filename
    except Exception as e:
        print(f"❌ 音声ファイル生成エラー: {str(e)}")
        return None

def post_to_slack(audio_filename, summary_text):
    """音声ファイルをSlackに投稿する"""
    if not audio_filename:
        return False
        
    try:
        client = WebClient(token=SLACK_BOT_TOKEN)
        
        response = client.files_upload_v2(
            channel=CHANNEL_ID,
            file=audio_filename,
            title="📻 昨日のラジオまとめ",
            initial_comment=f"🎧 昨日の投稿をラジオ風にまとめました！\n\n要約:\n{summary_text[:200]}..."
        )
        
        print("✅ Slackに音声ファイルを投稿しました！")
        return True
    except Exception as e:
        print(f"❌ Slack投稿エラー: {str(e)}")
        return False

def main():
    """メイン処理: 前日のメッセージを取得→要約→音声化→投稿"""
    print("🎙️ Slackラジオボット開始")
    
    print("📥 前日のメッセージを取得中...")
    messages = fetch_yesterday_messages()
    
    if not messages:
        print("📭 前日のメッセージがありませんでした。")
        return
    
    print(f"📝 {len(messages)}件のメッセージを取得しました。")
    
    print("🤖 ラジオ風要約を生成中...")
    summary = create_radio_summary(messages)
    print(f"📄 要約完了: {summary[:100]}...")
    
    print("🎵 音声ファイルを生成中...")
    audio_file = generate_audio(summary)
    
    print("📤 Slackに投稿中...")
    success = post_to_slack(audio_file, summary)
    
    if success:
        print("🎉 ラジオボット処理完了！")
    else:
        print("❌ 処理中にエラーが発生しました。")

if __name__ == "__main__":
    main()
