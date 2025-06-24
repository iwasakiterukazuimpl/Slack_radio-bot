#!/usr/bin/env python3
"""
Slack認証を単独でテストするデバッグスクリプト
"""
import os
import requests
from dotenv import load_dotenv

print("🔍 Slack認証デバッグスクリプト")
print("=" * 50)

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

print(f"📋 環境変数チェック:")
print(f"   SLACK_BOT_TOKEN: {'設定済み' if SLACK_BOT_TOKEN else '未設定'}")
if SLACK_BOT_TOKEN:
    print(f"   トークン形式: {'xoxb-' if SLACK_BOT_TOKEN.startswith('xoxb-') else 'その他'}")
    print(f"   トークン長: {len(SLACK_BOT_TOKEN)} 文字")
print(f"   CHANNEL_ID: {'設定済み' if CHANNEL_ID else '未設定'}")
print()

if not SLACK_BOT_TOKEN or not CHANNEL_ID:
    print("❌ 必要な環境変数が設定されていません")
    exit(1)

print("🔐 基本認証テスト (auth.test):")
headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
response = requests.get("https://slack.com/api/auth.test", headers=headers)
auth_data = response.json()

print(f"   レスポンス: {auth_data}")
if auth_data.get("ok"):
    print(f"   ✅ 認証成功!")
    print(f"   ユーザー: {auth_data.get('user')}")
    print(f"   チーム: {auth_data.get('team')}")
else:
    print(f"   ❌ 認証失敗: {auth_data.get('error')}")
    exit(1)

print()

print("📝 メッセージ取得テスト (conversations.history):")
params = {
    "channel": CHANNEL_ID,
    "limit": 5  # テスト用に少数のメッセージのみ取得
}

response = requests.get("https://slack.com/api/conversations.history", headers=headers, params=params)
data = response.json()

print(f"   レスポンス: {data}")
if data.get("ok"):
    print(f"   ✅ メッセージ取得成功!")
    messages = data.get("messages", [])
    print(f"   メッセージ数: {len(messages)}")
    for i, msg in enumerate(messages[:3]):  # 最初の3メッセージを表示
        print(f"   [{i+1}] {msg.get('text', 'テキストなし')[:50]}...")
else:
    print(f"   ❌ メッセージ取得失敗: {data.get('error')}")
    
    error_code = data.get("error")
    if error_code == "invalid_auth":
        print("   💡 トークンが無効です。以下を確認してください:")
        print("      - トークンがxoxb-で始まっているか")
        print("      - トークンが正しくコピーされているか")
        print("      - トークンの権限にchannels:historyが含まれているか")
    elif error_code == "channel_not_found":
        print("   💡 チャンネルが見つかりません:")
        print("      - CHANNEL_IDが正しいか確認してください")
    elif error_code == "not_in_channel":
        print("   💡 ボットがチャンネルに参加していません:")
        print("      - ボットをチャンネルに招待してください")

print()
print("🏁 デバッグ完了")
