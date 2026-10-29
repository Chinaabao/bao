#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宝($BAO) 每周抽奖 · 开奖计算 + 自动发布到电报群（GitHub Actions 版）
================================================================
从 lottery_input.json 读取本期输入（holders / tx_hash / prize_sol / period），
按白皮书机制计算 3 名中奖者，生成中英公告，并通过 Telegram Bot 自动发到宝的电报群。

敏感凭证一律从环境变量读取（GitHub Secrets 注入）：
  BAO_TG_BOT_TOKEN  电报 bot token
  BAO_TG_CHAT_ID    目标电报群 chat_id

用法：
  python3 scripts/bao_lottery.py
产出：
  announcement.txt  中英开奖公告（可直接留档/复核）
  payouts.json      发放清单（给项目方签名用，脚本不转账）
"""
import hashlib
import json
import os
import urllib.parse
import urllib.request

INPUT_FILE = os.environ.get("LOTTERY_INPUT", "lottery_input.json")


def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def draw(holders, tx_hash, prize_sol, n_winners=3):
    """SHA256(地址+哈希) 字典序排序，r=int(哈希,16)%n+1，循环取 n_winners 人。"""
    n = len(holders)
    entries = [(sha256_hex(a + tx_hash), a) for a in holders]
    entries.sort(key=lambda x: x[0])
    r = (int(tx_hash, 16) % n) + 1
    winners = [entries[(r - 1 + k) % n][1] for k in range(n_winners)]
    return winners, round(prize_sol / n_winners, 6), r, n


def render_announcement(period, tx_hash, winners, amount_each, prize_sol, r, n):
    """生成中英双语开奖公示：英文版在前，中文版在后。"""
    winners_lines = "\n".join(f"  #{i}  {w}" for i, w in enumerate(winners, 1))
    en = (
        "Bao ($BAO) Weekly Lucky Draw · Result Announcement\n"
        f"Round: {period} | Prize pool: {prize_sol} SOL\n"
        f"Seed tx hash: {tx_hash}\n"
        f"Order: SHA256(addr+hash) lexicographic | r={r} | total votes {n}\n"
        "-------------------------------------------\n"
        f"Winners ({len(winners)}, {amount_each} SOL each):\n" +
        winners_lines +
        "\n-------------------------------------------\n"
        "Review window: 3 days after publish (no re-draw on correction; "
        "disqualified roll down by rank; remainder rolls into next round)\n"
        "Payout: signed by the project wallet, per list and amount.\n"
        "All data is verifiable on-chain; this notice remains on record permanently.\n"
    )
    zh = (
        "宝($BAO) 每周幸运抽奖 · 开奖公示\n"
        f"期次：{period}　奖池：{prize_sol} SOL\n"
        f"种子交易哈希：{tx_hash}\n"
        f"排序：SHA256(地址+哈希) 字典序　编号 r={r}　总票数 {n}\n"
        "-------------------------------------------\n"
        f"中奖者（{len(winners)} 人，各得 {amount_each} SOL）：\n" +
        winners_lines +
        "\n-------------------------------------------\n"
        "复查窗口：公布后 3 天（纠错不重抽，剔除者按排号顺延递补，差额滚入下期）\n"
        "发放：由项目方钱包签名，按名单与金额执行。\n"
        "全部数据链上可复核，本公示永久留痕。\n"
    )
    return en + "\n" + zh


def send_telegram(text, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    token = os.environ.get("BAO_TG_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("BAO_TG_CHAT_ID", "").strip()
    if not token or not chat_id:
        raise SystemExit("缺少 BAO_TG_BOT_TOKEN / BAO_TG_CHAT_ID 环境变量（请在 GitHub Secrets 设置）")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    holders = data["holders"]
    tx_hash = data["tx_hash"]
    prize = float(data["prize_sol"])
    period = data.get("period", "本期")

    winners, amount_each, r, n = draw(holders, tx_hash, prize)
    text = render_announcement(period, tx_hash, winners, amount_each, prize, r, n)
    print(text)

    with open("announcement.txt", "w", encoding="utf-8") as f:
        f.write(text)
    payouts = [{"address": w, "amount_sol": amount_each} for w in winners]
    with open("payouts.json", "w", encoding="utf-8") as f:
        json.dump({"period": period, "prize_sol": prize, "payouts": payouts},
                  f, ensure_ascii=False, indent=2)
    print("\n[已产出] announcement.txt / payouts.json")

    res = send_telegram(text, token, chat_id)
    if res.get("ok"):
        print("\n[电报发布] 成功 → 已发到宝的电报群")
    else:
        print("\n[电报发布] 失败：", res)


if __name__ == "__main__":
    main()
