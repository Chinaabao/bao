#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宝($BAO) 空投地址收集 · Telegram Bot 通道
=========================================
玩家在电报私聊 bot，发一条含 Solana 地址的消息；本脚本定时拉取 getUpdates，
提取有效 Solana 地址，去重后持久化到 lottery/data/tg_addresses.json。

产出（持久化在仓库）：
  lottery/data/tg_addresses.json
    {"addresses": [...], "offset": <已处理到的最新 update_id>}
  - addresses 供 bao_airdrop.py 合并（X 评论区 + TG 双通道）

环境变量（GitHub Secret）：
  BAO_TG_BOT_TOKEN   电报 bot token（用于 getUpdates 读取玩家消息）

注意：本脚本只“收集地址”，不发送任何公告、不转账。
"""
import json
import os
import re
import urllib.parse
import urllib.request

TG_API = "https://api.telegram.org"
ADDR_RE = re.compile(r"(?<![A-Za-z0-9])[1-9A-HJ-NP-Za-km-z]{32,44}(?![A-Za-z0-9])")
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
TG_FILE = os.path.join(DATA_DIR, "tg_addresses.json")


def tg_call(token, method, **params):
    url = f"{TG_API}/bot{token}/{method}"
    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def load_state():
    if os.path.exists(TG_FILE):
        with open(TG_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
        return set(d.get("addresses", [])), int(d.get("offset", 0))
    return set(), 0


def save_state(addresses, offset):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(TG_FILE, "w", encoding="utf-8") as f:
        json.dump({"addresses": sorted(addresses), "offset": offset}, f, indent=2)


def main():
    token = os.environ.get("BAO_TG_BOT_TOKEN", "").strip()
    if not token:
        raise SystemExit("缺少 BAO_TG_BOT_TOKEN（请在 GitHub Secrets 设置）")

    # 确认 bot 身份（拿到 username，玩家 @ 谁）
    me = tg_call(token, "getMe")
    if not me.get("ok"):
        raise SystemExit(f"getMe 失败：{me}")
    username = me["result"]["username"]
    print(f"[bot] @{username}")

    known, offset = load_state()
    print(f"[状态] 已收集 {len(known)} 个地址；从 offset={offset} 继续")

    updates = tg_call(token, "getUpdates", offset=offset, timeout=5)
    if not updates.get("ok"):
        raise SystemExit(f"getUpdates 失败：{updates}")

    added = 0
    new_offset = offset
    for u in updates.get("result", []):
        new_offset = max(new_offset, u["update_id"] + 1)
        msg = u.get("message") or {}
        chat = msg.get("chat") or {}
        text = msg.get("text") or ""
        # 只处理玩家私聊（chat.type == private），避免误收集群内闲聊
        if chat.get("type") != "private" or not text:
            continue
        for m in ADDR_RE.findall(text):
            if m not in known:
                known.add(m)
                added += 1
                print(f"  + 新增地址 {m}")

    if added or new_offset != offset:
        save_state(known, new_offset)
        print(f"[完成] 新增 {added} 个；累计 {len(known)} 个地址（已写回 {TG_FILE}）")
    else:
        print("[完成] 无新地址。")


if __name__ == "__main__":
    main()
