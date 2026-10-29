#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宝($BAO) 每日奖池累积公告 · 查询奖池地址 SOL 余额并自动发布到电报（GitHub Actions 版）
================================================================
每天查询奖池地址当前 SOL 持仓（作为本周奖池累积），生成中英双语公告，
通过 Telegram Bot 自动发到宝的电报频道。

敏感凭证一律从环境变量读取（GitHub Secrets 注入）：
  BAO_POOL_ADDRESS  奖池 Solana 地址（建好后填入 GitHub Secrets）
  BAO_TG_BOT_TOKEN  电报 bot token
  BAO_TG_CHAT_ID    目标电报频道 chat_id

用法：
  python3 scripts/bao_daily_pool.py
产出：
  daily_pool_announcement.txt  中英双语公告（可留档/复核）
"""
import json
import os
import urllib.parse
import urllib.request

SOL_RPC = os.environ.get("SOLANA_RPC", "https://api.mainnet-beta.solana.com")


def get_sol_balance(address: str) -> float:
    """调用 Solana JSON-RPC getBalance 查询地址 SOL 余额（返回 SOL，1 SOL = 1e9 lamports）。"""
    body = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "getBalance", "params": [address]
    }).encode("utf-8")
    req = urllib.request.Request(
        SOL_RPC, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if "error" in data:
        raise RuntimeError(f"Solana RPC error: {data['error']}")
    return data["result"]["value"] / 1e9


def render_announcement(address: str, balance_sol: float) -> str:
    """生成中英双语每日奖池公告：英文版在前，中文版在后。"""
    en = (
        "Bao ($BAO) Daily Prize Pool · Accumulated Balance\n"
        f"Pool address: `{address}`\n"
        f"Current balance: {balance_sol:.4f} SOL\n"
        "This is this week's accumulated prize pool (live on-chain balance).\n"
        "All data is verifiable on-chain."
    )
    zh = (
        "宝($BAO) 每日奖池 · 累积持仓\n"
        f"奖池地址：`{address}`\n"
        f"当前持仓：{balance_sol:.4f} SOL\n"
        "此为本周奖池累积（链上实时余额）。\n"
        "全部数据链上可复核。"
    )
    return en + "\n\n" + zh


def send_telegram(text: str, token: str, chat_id: str):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    address = os.environ.get("BAO_POOL_ADDRESS", "").strip()
    token = os.environ.get("BAO_TG_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("BAO_TG_CHAT_ID", "").strip()
    if not address:
        raise SystemExit("缺少 BAO_POOL_ADDRESS 环境变量（请在 GitHub Secrets 设置奖池地址）")
    if not token or not chat_id:
        raise SystemExit("缺少 BAO_TG_BOT_TOKEN / BAO_TG_CHAT_ID 环境变量")

    balance = get_sol_balance(address)
    text = render_announcement(address, balance)
    print(text)
    with open("daily_pool_announcement.txt", "w", encoding="utf-8") as f:
        f.write(text)

    res = send_telegram(text, token, chat_id)
    if res.get("ok"):
        print("\n[电报发布] 成功 → 已发到宝的电报频道")
    else:
        print("\n[电报发布] 失败：", res)


if __name__ == "__main__":
    main()
