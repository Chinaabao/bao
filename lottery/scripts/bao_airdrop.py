#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宝($BAO) 空投机器人 · X 置顶推文评论区地址收集 + $BAO 自动空投
================================================================
流程：
  1. 用 X Bearer Token 拉取置顶推文评论区回复（Search API, conversation_id）
  2. 正则提取 Solana 地址并去重（同一地址只算一次）
  3. 读取历史已空投地址（airdrop_history.json），剔除曾领过空投的钱包
  4. 按固定数量生成空投清单（本次有效地址）
  5. 中英双语公告到电报群
  6. 仅当显式确认（CONFIRM_PAYOUT=yes）且有私钥+代币 mint 时，自动转账 $BAO
     转账成功后将本次地址写入历史，防止重复空投

历史文件 airdrop_history.json 保存在仓库中（透明、可审计、持久）：
  - 每个钱包只能领取一次空投；已空投的地址在后续空投中自动剔除

环境变量（由 GitHub Secrets / workflow 注入）：
  X_BEARER_TOKEN          X API Bearer Token
  PINNED_TWEET_ID         置顶推文 ID（x.com/Chinaabao/status/<ID> 中的数字）
  AIRDROP_AMOUNT          每人空投 $BAO 数量（整数）
  AIRDROP_TOKEN_MINT      $BAO 代币 mint 地址
  AIRDROP_WALLET_PRIVKEY  空投钱包私钥（base58；不填则只出名单不转账）
  CONFIRM_PAYOUT          是否确认发放：仅 "yes"/"true" 才执行转账（空投前人工确认）
  AIRDROP_HISTORY_FILE    历史文件路径（默认 airdrop_history.json）
  AIRDROP_TOKEN_DECIMALS  $BAO 代币小数位（默认 6）
  SOLANA_RPC              Solana RPC 节点（默认公共主网）
  BAO_TG_BOT_TOKEN        电报 bot token
  BAO_TG_CHAT_ID          目标电报频道/群 chat_id

用法：
  python3 scripts/bao_airdrop.py
产出：
  airdrop_list.json         本次有效空投清单（地址->数量）
  airdrop_announcement.txt  中英双语公告
  airdrop_transfers.json    转账结果（确认发放后）
  airdrop_history.json      已空投地址历史（合并写回）
"""
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


# ---------- 2.5 读取 Telegram 通道收集的地址 ----------
def load_tg_addresses(path="lottery/data/tg_addresses.json"):
    """读取 TG bot 收集的地址清单（双通道之一）；文件不存在时返回空列表。"""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        d = json.load(f)
    return d.get("addresses", [])


# ---------- 历史去重（每个钱包只能领一次空投） ----------
def load_history(path):
    """读取历史已空投地址集合；文件不存在时返回空集合。"""
    if not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return set(data)
    return set(data.get("airdropped", []))


def save_history(path, new_addresses):
    """把本次已空投地址合并写回历史文件（与旧历史取并集，去重）。"""
    old = load_history(path)
    merged = sorted(old | set(new_addresses))
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"airdropped": merged}, f, indent=2)
    return merged


# ---------- 3. 公告 ----------
def render_announcement(collected, skipped, winners, amount):
    en_lines = [
        "Bao ($BAO) Airdrop · Address Collection",
        f"Qualified addresses from the pinned tweet comments: {collected}",
        f"Already-airdropped (skipped): {skipped}",
        f"Valid this round: {len(winners)}",
        f"Each valid address receives {amount} $BAO",
    ]
    if not winners:
        en_lines.append("No new address this round.")
    en = "\n".join(en_lines)
    zh_lines = [
        "宝($BAO) 空投 · 地址收集",
        f"从置顶推文评论区收集到合格地址：{collected} 个",
        f"历史已空投（剔除）：{skipped} 个",
        f"本次有效地址：{len(winners)} 个",
        f"每个有效地址获得 {amount} $BAO",
    ]
    if not winners:
        zh_lines.append("本轮没有新地址。")
    zh = "\n".join(zh_lines)
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
    """用空投钱包向每个有效地址转账 amount * $BAO。返回每笔结果列表。"""
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
    history_file = os.environ.get("AIRDROP_HISTORY_FILE", "airdrop_history.json").strip()
    confirm = os.environ.get("CONFIRM_PAYOUT", "").strip().lower() in ("yes", "true", "1")

    if not bearer or not tweet_id or not amount_str:
        raise SystemExit("缺少 X_BEARER_TOKEN / PINNED_TWEET_ID / AIRDROP_AMOUNT（请在 GitHub Secrets/变量设置）")
    amount = int(amount_str)

    print("[1/4] 拉取置顶推文评论区...")
    texts = fetch_x_replies(bearer, tweet_id)
    print(f"  获取到 {len(texts)} 条回复")

    print("[2/4] 提取并去重地址（X 评论区 + TG bot 双通道）...")
    x_addresses = extract_addresses(texts)
    tg_addresses = load_tg_addresses()
    # 双通道合并、保持顺序去重（同一地址只记一次）
    addresses = list(dict.fromkeys(x_addresses + tg_addresses))
    print(f"  X 评论区 {len(x_addresses)} 个 / TG 收集 {len(tg_addresses)} 个 / 合并唯一 {len(addresses)} 个")

    print("[3/4] 剔除历史已空投地址...")
    history = load_history(history_file)
    skipped = [a for a in addresses if a in history]
    winners = [a for a in addresses if a not in history]
    print(f"  历史已空投 {len(history)} 个；本次剔除 {len(skipped)} 个；本轮有效 {len(winners)} 个")

    print("[4/4] 生成公告...")
    text = render_announcement(len(addresses), len(skipped), winners, amount)
    with open("airdrop_list.json", "w", encoding="utf-8") as f:
        json.dump([{"address": a, "amount": amount} for a in winners], f, indent=2)
    with open("airdrop_announcement.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(text)

    if token and chat_id:
        res = send_telegram(text, token, chat_id)
        print("\n[电报公告]", "成功" if res.get("ok") else f"失败：{res}")

    # 发放：需 私钥 + mint + 人工确认（CONFIRM_PAYOUT=yes）三者齐备才执行
    if privkey and mint and confirm:
        if not winners:
            print("\n[空投发放] 本轮无新地址，跳过转账。")
        else:
            print(f"\n[空投发放] 已确认，开始自动转账 {len(winners)} 笔...")
            results = transfer_airdrop(privkey, mint, winners, amount, decimals)
            ok = [r for r in results if "signature" in r]
            fail = [r for r in results if "error" in r]
            with open("airdrop_transfers.json", "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
            print(f"  成功 {len(ok)} 笔 / 失败 {len(fail)} 笔（详见 airdrop_transfers.json）")
            # 只有成功转账的地址才写入历史，防止下次重复空投
            if ok:
                history_now = save_history(history_file, [r["address"] for r in ok])
                print(f"  已更新历史：累计已空投 {len(history_now)} 个地址")
                text2 = (
                    f"✅ $BAO 空投发放完成：{len(ok)} 笔成功，{len(fail)} 笔失败。\n"
                    f"累计已空投地址：{len(history_now)} 个（每个钱包仅限一次）"
                )
                if token and chat_id:
                    send_telegram(text2, token, chat_id)
    elif privkey and mint:
        print("\n[空投发放] 未确认（CONFIRM_PAYOUT 未设为 yes），仅收集公告，不发放。请确认名单后勾选确认再运行。")
    else:
        print("\n[空投发放] 未提供私钥/代币 mint，仅生成名单，不转账（由项目方钱包手动执行）")


if __name__ == "__main__":
    main()
