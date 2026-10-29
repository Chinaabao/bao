# Bao（$BAO · 宝）

> **吉祥物**：国风功夫熊猫「宝」（斗笠、青绿盘扣中式服、云纹、红绳中国结、木葫芦、行囊竹杖，3D 可爱国风）
> **口号**：每个人都值得成为幸运儿，每周都有机会 · Everyone deserves a chance to be the lucky one — every week.
> **链**：Solana　**总量**：1,000,000,000（固定永不增发）　**发行**：所有代币投入流动性池，项目方无预留

这是宝（$BAO）项目的公开仓库，集中存放项目文档与每周抽奖自动化。

## 目录

```
├── docs/                               # 项目文档（独立成篇，白皮书不含路线图与NFT）
│   ├── Bao_项目白皮书.md               # 项目完整白皮书（11章，每章英文在前·中文在后）
│   ├── Bao_Logo标准规范.md             # Logo 标准参数（核心图/单色/反白/色值/安全区）
│   ├── 上线与迁移路线图.md             # 上线与迁移路线图（独立文档）
│   └── 周边NFT铸造技术方案.md           # 周边NFT铸造技术方案（独立文档）
└── lottery/                            # 每周幸运抽奖
    ├── Bao每周抽奖白皮书.md               # 抽奖白皮书（对外简短介绍）
    ├── 每周抽奖公式说明.md               # 抽奖公式与执行规则
    ├── scripts/bao_lottery.py          # 开奖计算 + 自动发电报
    ├── .github/workflows/bao-weekly-lottery.yml  # 每周一自动开奖
    ├── lottery_input.example.json      # 每期输入模板
    └── Bao_每周抽奖公告模板_中英.md        # 中英公告话术
```

## 每周抽奖（核心机制）

- **资格**：快照时（周一 00:00 UTC）持仓市值 ≥ $100，一人一票
- **种子**：周一 00:00 后第一个确认交易哈希（透明可复核）
- **公式**：`SHA256(地址+哈希)` 字典序排序，`r=int(哈希,16)%N+1`，循环取 3 人平分奖池
- **发放**：由项目方钱包签名执行（脚本只算不开奖转账）

详见 [`lottery/每周抽奖公式说明.md`](lottery/每周抽奖公式说明.md)。

## Logo 标准

官方 Logo 为圆形徽章·斗笠熊猫图形标（不含文字）。标准参数见 [`docs/Bao_Logo标准规范.md`](docs/Bao_Logo标准规范.md)——含彩色主标 / 黑色单色版 / 白色反白版、标准色值、最小尺寸、安全区与禁止项。

## 自动化

`lottery/.github/workflows/bao-weekly-lottery.yml` 每周一 00:00 UTC 自动开奖并发布到宝的电报群。
- Secrets：`BAO_TG_BOT_TOKEN`、`BAO_TG_CHAT_ID`
- 每期填 `lottery/lottery_input.json`（参考 `lottery_input.example.json`）
- 首次用 **Actions → Run workflow** 手动触发测试

## 社区
- X：https://x.com/Chinaabao
- Telegram：https://t.me/Chinaabao

> 声明：本白皮书与机制按境外合规设计（含 "Not for US persons"），请遵守所在地法律。
