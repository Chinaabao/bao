#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宝($BAO) 空投机器人 · X 置顶推文评论区地址收集 + $BAO 自动空投
================================================================
流程：
  1. 用 X Bearer Token 拉取置顶推文评论区回复（Search API, conversation_id）
  2. 正则提取 Solana 地址并去重（同一地址只算一次）
  3. 按固定数量生成空投清单
  4. 中英双语公告到电报群
  5. 用空投钱包私钥自动转账 $BAO（SPL token；未填私钥则只出清单不发）

环境变量（由 GitHub Secrets / workflow 注入）：
  X_BEARER_TOKEN          X API Bearer Token
  PINNED_TWEET_ID         置顶推文 ID（x.com/Chinaabao/status/<ID> 中的数字）
  AIRDROP_AMOUNT          每人空投 $BAO 数量（整数）
  AIRDROP_TOKEN_MINT      $BAO 代币 mint 地址
  AIRDROP_WALLET_PRIVKEY  空投钱包私钥（base58；不填则只出名单不转账）
  AIRDROP_TOKEN_DECIMALS  $BAO 代币小数位（默认 6）
  SOLANA_RPC              Solana RPC 节点（默认公共主网）
  BAO_TG_BOT_TOKEN        电报 bot token
  BAO_TG_CHAT_ID          目标电报频道/群 chat_id

用法：
  python3 scripts/bao_airdrop.py
产出：
  airdrop_list.json         合格空投清单（地址->数量）
  airdrop_announcement.txt  中英双语公告
"""
import base64
import json
import os
import re
import urllib.parse
import urllib.request

X_API = os.environ.get("X_API_BASE", "https://api.x.com")
SOL_RPC = os.environ.get("SOLANA_RPC", "https://api.mainnet-beta.solana.com")
# Solana 地址：base58，32-44 位，前后不以字母数字为界（避免误匹配单词）
ADDR_RE = re.compile(r"(?<![A-Za-z0-9])[1-9A-HJ-NP-Za-km-z]{32,44}(?![A-Za-z0-9])")


# ---------- 1. 拉取 X 置顶推文评论区 ----------
def fetch_x_replies(bearer, tweet_id):
    """用 Search API 按 conversation_id 拉取该推文下所有回复文本（自动分页）。"""
    texts = []
    next_token = None
    base = f"{X_API}/2/tweets/search/recent"
    for _ in range(30):  # 最多 30 页，防止无限循环
        params = {
            "query": f"conversation_id:{tweet_id}",
            "tweet.fields": "author_id,text",
            "max_results": 100,
        }
        if next_token:
            params["next_token"] = next_token
        url = base + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {bearer}"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if "data" in data:
            texts.extend(t["text"] for t in data["data"])
        meta = data.get("meta", {})
        next_token = meta.get("next_token")
        if not next_token:
            break
    return texts


# ---------- 2. 提取并去重地址 ----------
def extract_addresses(texts):
    """从回复文本提取 Solana 地址并去重（保持首次出现顺序）。"""
    seen, out = set(), []
    for t in texts:
        for m in ADDR_RE.findall(t):
            if m not in seen:
                seen.add(m)
                out.append(m)
    return out


# ---------- 3. 公告 ----------
def render_announcement(addresses, amount, winners):
    en = (
        "Bao ($BAO) Airdrop · Address Collection\n"
        f"Qualified addresses from the pinned tweet comments: {len(addresses)}\n"
        f"Each qualified address receives {amount} $BAO\n"
        "List & amounts below; payout is executed by the airdrop wallet. All verifiable on-chain."
    )
    zh = (
        "宝($BAO) 空投 · 地址收集\n"
        f"从置顶推文评论区收集到合格地址：{len(addresses)} 个\n"
        f"每个合格地址获得 {amount} $BAO\n"
        "名单与数量如下，由空投钱包执行发放，全部链上可复核。"
    )
    body = en + "\n\n" + zh
    if winners:
        body += "\n\n" + "\n".join(f"• {addr}: {amount} $BAO" for addr in winners)
    return body


def send_telegram(text, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ---------- 4. 自动转账 $BAO（SPL token） ----------
def transfer_airdrop(privkey_b58, mint_b58, winners, amount, decimals):
    """用空投钱包向每个合格地址转账 amount * $BAO。"""
    from solders.keypair import Keypair
    from solders.pubkey import Pubkey
    from solders.transaction import Transaction
    from solana.rpc.api import Client
    from spl.token.constants import TOKEN_PROGRAM_ID
    from spl.token.instructions import (
        create_associated_token_account,
        get_associated_token_address,
        transfer_checked,
    )

    payer = Keypair.from_base58_string(privkey_b58)
    mint = Pubkey.from_string(mint_b58)
    client = Client(SOL_RPC)
    results = []
    for addr in winners:
        try:
            dest = Pubkey.from_string(addr)
            dest_ata = get_associated_token_address(dest, mint)
            payer_ata = get_associated_token_address(payer.pubkey(), mint)
            txn = Transaction()
            # 若接收方没有该代币的关联账户，先创建
            acct = client.get_account_info(dest_ata)
            if acct.value is None:
                txn.add(create_associated_token_account(
                    payer.pubkey(), dest, mint, TOKEN_PROGRAM_ID))
            txn.add(transfer_checked(
                payer_ata, mint, dest_ata, payer.pubkey(),
                int(amount * 10 ** decimals), decimals))
            sig = client.send_transaction(txn, payer)
            results.append({"address": addr, "amount": amount, "signature": str(sig.value)})
        except Exception as e:
            results.append({"address": addr, "amount": amount, "error": str(e)})
    return results


def main():
    bearer = os.environ.get("X_BEARER_TOKEN", "").strip()
    tweet_id = os.environ.get("PINNED_TWEET_ID", "").strip()
    amount_str = os.environ.get("AIRDROP_AMOUNT", "").strip()
    mint = os.environ.get("AIRDROP_TOKEN_MINT", "").strip()
    privkey = os.environ.get("AIRDROP_WALLET_PRIVKEY", "").strip()
    decimals = int(os.environ.get("AIRDROP_TOKEN_DECIMALS", "6"))
    token = os.environ.get("BAO_TG_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("BAO_TG_CHAT_ID", "").strip()

    if not bearer or not tweet_id or not amount_str:
        raise SystemExit("缺少 X_BEARER_TOKEN / PINNED_TWEET_ID / AIRDROP_AMOUNT（请在 GitHub Secrets/变量设置）")
    amount = int(amount_str)

    print("[1/3] 拉取置顶推文评论区...")
    texts = fetch_x_replies(bearer, tweet_id)
    print(f"  获取到 {len(texts)} 条回复")

    print("[2/3] 提取并去重地址...")
    addresses = extract_addresses(texts)
    print(f"  提取到 {len(addresses)} 个唯一地址")

    # 空投名单（每人固定数量）
    winners = addresses

    print("[3/3] 生成公告...")
    text = render_announcement(addresses, amount, winners)
    with open("airdrop_list.json", "w", encoding="utf-8") as f:
        json.dump([{"address": a, "amount": amount} for a in winners], f, indent=2)
    with open("airdrop_announcement.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(text)

    if token and chat_id:
        res = send_telegram(text, token, chat_id)
        print("\n[电报公告]", "成功" if res.get("ok") else f"失败：{res}")

    # 自动转账（仅当提供私钥与 mint）
    if privkey and mint:
        print("\n[空投发放] 开始自动转账...")
        results = transfer_airdrop(privkey, mint, winners, amount, decimals)
        ok = [r for r in results if "signature" in r]
        fail = [r for r in results if "error" in r]
        with open("airdrop_transfers.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"  成功 {len(ok)} 笔 / 失败 {len(fail)} 笔（详见 airdrop_transfers.json）")
        if ok:
            text2 = render_announcement([], amount, []) + "\n" + (
                f"✅ 空投发放完成：{len(ok)} 笔成功，{len(fail)} 笔失败。"
            )
            if token and chat_id:
                send_telegram(text2, token, chat_id)
    else:
        print("\n[空投发放] 未提供私钥/代币 mint，仅生成名单，不转账（由项目方钱包手动执行）")


if __name__ == "__main__":
    main()
