# Bao（$BAO · 宝）

**English：**

> **Mascot**: Chinese-style kung fu panda "Bao" (straw hat, jade-green frog-button robe, cloud pattern, red-knot tassel, wooden gourd, bundle & bamboo staff; 3D cute Chinese style)
> **Slogan**: Everyone deserves a chance to be the lucky one — every week. · 每个人都值得成为幸运儿，每周都有机会。
> **Chain**: Solana　**Supply**: 1,000,000,000 (fixed, never inflated)　**Launch**: all tokens to liquidity pool, no team reserve

This is the public repository of the Bao ($BAO) project, hosting project docs and the weekly lottery automation.

## 目录 / Table of Contents

**English：**

```
├── docs/                               # Project docs (standalone; whitepaper excludes roadmap & NFT)
│   ├── Bao_Whitepaper.md               # Full whitepaper (11 chapters, English-first Chinese-after)
│   ├── Bao_Logo_Specification.md       # Logo standard (core/mono/reverse/colors/clear space)
│   ├── Bao_Launch_Roadmap.md           # Launch & migration roadmap (standalone)
│   └── Bao_Merchandise_NFT_Scheme.md   # Merch NFT technical plan (standalone)
└── lottery/                            # Weekly lucky draw
    ├── Bao_Weekly_Lottery_Whitepaper.md            # Lottery whitepaper (short external intro)
    ├── Bao_Weekly_Lottery_Formula.md               # Lottery formula & execution rules
    ├── scripts/bao_lottery.py          # Draw computation + auto Telegram post
    ├── .github/workflows/bao-weekly-lottery.yml    # Weekly auto draw (Monday 00:00 UTC)
    ├── lottery_input.example.json      # Per-round input template
    └── Bao_Weekly_Lottery_Announcement_Template.md # Bilingual announcement copy
```

**中文：**

```
├── docs/                               # 项目文档（独立成篇，白皮书不含路线图与NFT）
│   ├── Bao_Whitepaper.md               # 项目完整白皮书（11章，每章英文在前·中文在后）
│   ├── Bao_Logo_Specification.md       # Logo 标准参数（核心图/单色/反白/色值/安全区）
│   ├── Bao_Launch_Roadmap.md           # 上线与迁移路线图（独立文档）
│   └── Bao_Merchandise_NFT_Scheme.md   # 周边NFT铸造技术方案（独立文档）
└── lottery/                            # 每周幸运抽奖
    ├── Bao_Weekly_Lottery_Whitepaper.md            # 抽奖白皮书（对外简短介绍）
    ├── Bao_Weekly_Lottery_Formula.md               # 抽奖公式与执行规则
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

See [`lottery/Bao_Weekly_Lottery_Formula.md`](lottery/Bao_Weekly_Lottery_Formula.md).

**中文：**

- **资格**：快照时（周一 00:00 UTC）持仓市值 ≥ $100，一人一票
- **种子**：周一 00:00 后第一个确认交易哈希（透明可复核）
- **公式**：`SHA256(地址+哈希)` 字典序排序，`r=int(哈希,16)%N+1`，循环取 3 人平分奖池
- **发放**：由项目方钱包签名执行（脚本只算不开奖转账）

详见 [`lottery/Bao_Weekly_Lottery_Formula.md`](lottery/Bao_Weekly_Lottery_Formula.md)。

---

## Logo 标准 / Logo Standard

**English：**

The official Logo is a circular-badge straw-hat panda graphic mark (no text). Standards in [`docs/Bao_Logo_Specification.md`](docs/Bao_Logo_Specification.md) — color primary / black monochrome / white reverse, palette, minimum sizes, clear space, and prohibitions.

**中文：**

官方 Logo 为圆形徽章·斗笠熊猫图形标（不含文字）。标准参数见 [`docs/Bao_Logo_Specification.md`](docs/Bao_Logo_Specification.md)——含彩色主标 / 黑色单色版 / 白色反白版、标准色值、最小尺寸、安全区与禁止项。

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
