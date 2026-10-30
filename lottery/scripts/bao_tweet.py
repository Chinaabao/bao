#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宝($BAO) 自动发推机器人 · GitHub Actions 定时/手动发布英文推文
================================================================
用 OAuth 1.0a（用户级授权）调用 X API POST /2/tweets 发推。
X 发布内容为全英文（X 自带翻译，无需中文对照）。

环境变量（由 GitHub Secrets / workflow 注入）：
  X_CONSUMER_KEY           Consumer Key（API Key）
  X_CONSUMER_SECRET        Consumer Secret（API Secret）
  X_ACCESS_TOKEN           Access Token
  X_ACCESS_TOKEN_SECRET    Access Token Secret
  X_TWEET_TEXT             要发布的推文文本（英文，≤280 字符）
  X_TWEET_ALT_TEXT         可选：媒体替代文本（预留，暂未启用）

用法：
  python3 scripts/bao_tweet.py
输出：
  发布成功打印推文 ID 与链接；失败退出码 1
"""
import os
import sys

try:
    from requests_oauthlib import OAuth1
    import requests
except ImportError:
    print("缺少依赖：pip install requests requests-oauthlib")
    sys.exit(1)

API_URL = "https://api.x.com/2/tweets"
# 超过 280 字符的推文会被 X 拒绝
MAX_LEN = 280


def post_tweet(text):
    oauth = OAuth1(
        os.environ["X_CONSUMER_KEY"],
        os.environ["X_CONSUMER_SECRET"],
        os.environ["X_ACCESS_TOKEN"],
        os.environ["X_ACCESS_TOKEN_SECRET"],
    )
    return requests.post(API_URL, json={"text": text}, auth=oauth, timeout=30)


def main():
    text = os.environ.get("X_TWEET_TEXT", "").strip()
    if not text:
        raise SystemExit("缺少 X_TWEET_TEXT 环境变量（请在 workflow 输入或变量中填写推文内容）")
    if len(text) > MAX_LEN:
        raise SystemExit(f"推文超 {MAX_LEN} 字符（当前 {len(text)}），请精简后再发")

    print(f"[发推] 长度 {len(text)} 字符")
    r = post_tweet(text)
    print(f"[HTTP] {r.status_code}")
    print(r.text[:600])

    if r.status_code == 201:
        data = r.json()["data"]
        print(f"✅ 发布成功 id={data['id']}")
        print(f"🔗 https://x.com/Chinaabao/status/{data['id']}")
    else:
        print("❌ 发布失败（检查凭证是否配对、权限是否为 Read and write、内容是否合规）")
        sys.exit(1)


if __name__ == "__main__":
    main()
