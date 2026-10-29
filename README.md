# Bao（$BAO · 宝）

**English：**

> **Mascot**: Chinese-style kung fu panda "Bao" (straw hat, jade-green frog-button robe, cloud pattern, red-knot tassel, wooden gourd, bundle & bamboo staff; 3D cute Chinese style)
> **Slogan**: Everyone deserves a chance to be the lucky one — every week. · 每个人都值得成为幸运儿，每周都有机会。
> **Chain**: Solana　**Supply**: 1,000,000,000 (fixed, never inflated)　**Launch**: all tokens to liquidity pool, no team reserve

This is the public repository of the Bao ($BAO) project, hosting project docs and the weekly lottery automation.

## 目录 / Table of Contents

**English：**

```
├── docs/                               # Project docs (standalone)
│   ├── Bao_Whitepaper.md               # Full whitepaper: project + weekly lottery (11 chapters, English-first Chinese-after)
│   └── Bao_Logo_Specification.md       # Logo standard (core/mono/reverse/colors/clear space)
└── lottery/                            # Weekly lucky draw
    ├── scripts/bao_lottery.py          # Draw computation + auto Telegram post
    ├── .github/workflows/bao-weekly-lottery.yml    # Weekly auto draw (Monday 00:00 UTC)
    ├── lottery_input.example.json      # Per-round input template
    └── Bao_Weekly_Lottery_Announcement_Template.md # Bilingual announcement copy
```

**中文：**

```
├── docs/                               # 项目文档（独立成篇）
│   ├── Bao_Whitepaper.md               # 完整白皮书（项目+每周抽奖机制，11章，英文在前·中文在后）
│   └── Bao_Logo_Specification.md       # Logo 标准参数（核心图/单色/反白/色值/安全区）
└── lottery/                            # 每周幸运抽奖
    ├── scripts/bao_lottery.py          # 开奖计算 + 自动发电报
    ├── .github/workflows/bao-weekly-lottery.yml    # 每周一自动开奖
    ├── lottery_input.example.json      # 每期输入模板
    └── Bao_Weekly_Lottery_Announcement_Template.md # 中英公告话术
```

---

## 每周抽奖 / Weekly Lottery

**English：**

- **Eligibility**: market value ≥ $100 at snapshot (Monday 00:00 UTC), one person one vote
- **Seed**: first confirmed tx hash after Monday 00:00 (transparent & verifiable)
- **Formula**: `SHA256(addr+hash)` lexicographic sort, `r=int(hash,16)%N+1`, take 3 cyclically to split the pool
- **Payout**: signed by project wallet (the script only computes, it does not transfer)

See [`docs/Bao_Whitepaper.md`](docs/Bao_Whitepaper.md) §6 for the full formula.

**中文：**

- **资格**：快照时（周一 00:00 UTC）持仓市值 ≥ $100，一人一票
- **种子**：周一 00:00 后第一个确认交易哈希（透明可复核）
- **公式**：`SHA256(地址+哈希)` 字典序排序，`r=int(哈希,16)%N+1`，循环取 3 人平分奖池
- **发放**：由项目方钱包签名执行（脚本只算不开奖转账）

完整公式见 [`docs/Bao_Whitepaper.md`](docs/Bao_Whitepaper.md) 第 6 章。

---

## Logo 标准 / Logo Standard

**English：**

The official Logo is a **panda bust head mark** (straw-hat Chinese-style panda, no text). Standards in [`docs/Bao_Logo_Specification.md`](docs/Bao_Logo_Specification.md) — color primary (jade-green robe + brown straw hat, white background), palette, minimum sizes, clear space, and prohibitions. Monochrome / reverse pending master finalization.

**中文：**

官方 Logo 为**熊猫半身头像标**（斗笠国风熊猫，不含文字）。标准参数见 [`docs/Bao_Logo_Specification.md`](docs/Bao_Logo_Specification.md)——含彩色主标（青绿中式服＋棕褐斗笠、白底）、标准色值、最小尺寸、安全区与禁止项。单色版/反白版待主标定稿后制作。

---

## 自动化 / Automation

**English：**

`lottery/.github/workflows/bao-weekly-lottery.yml` triggers every Monday 00:00 UTC to auto-draw and post to the Bao Telegram group.
- Secrets: `BAO_TG_BOT_TOKEN`, `BAO_TG_CHAT_ID`
- Fill `lottery/lottery_input.json` each round (see `lottery_input.example.json`)
- First run: test via **Actions → Run workflow**

**中文：**

`lottery/.github/workflows/bao-weekly-lottery.yml` 每周一 00:00 UTC 自动开奖并发布到宝的电报群。
- Secrets：`BAO_TG_BOT_TOKEN`、`BAO_TG_CHAT_ID`
- 每期填 `lottery/lottery_input.json`（参考 `lottery_input.example.json`）
- 首次用 **Actions → Run workflow** 手动触发测试

**每日奖池播报 / Daily Pool Announcement**（English）：

`lottery/.github/workflows/bao-daily-pool.yml` sends a bilingual pool-balance announcement every day at 20:00 (UTC+8, 12:00 UTC), reporting the prize-pool address's current SOL balance as this week's accumulated pool.
- Secrets: add `BAO_POOL_ADDRESS` (the prize-pool Solana address) once created; reuses `BAO_TG_BOT_TOKEN`, `BAO_TG_CHAT_ID`

（中文）：

`lottery/.github/workflows/bao-daily-pool.yml` 每天 20:00（UTC+8，即 12:00 UTC）发送一条中英双语奖池公告，播报奖池地址当前 SOL 持仓，作为本周奖池累积。
- Secrets：建好奖池地址后，在 GitHub Secrets 添加 `BAO_POOL_ADDRESS`；复用 `BAO_TG_BOT_TOKEN`、`BAO_TG_CHAT_ID`

---

## 社区 / Community

**English：**

- X: https://x.com/Chinaabao
- Telegram: https://t.me/Chinaabao

> Disclaimer: this whitepaper & mechanics are designed for offshore compliance (incl. "Not for US persons"); please follow the laws of your jurisdiction.

**中文：**

- X：https://x.com/Chinaabao
- Telegram：https://t.me/Chinaabao

> 声明：本白皮书与机制按境外合规设计（含 "Not for US persons"），请遵守所在地法律。
