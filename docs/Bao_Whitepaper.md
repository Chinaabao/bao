# $BAO Whitepaper · $BAO 项目白皮书

**中文名：宝（Bao）· 吉祥物：可爱的功夫熊猫 · 双语对照版（每章英文在前，中文在后）**
**Bilingual edition — English first, then Chinese within each chapter**

> **Everyone deserves a chance to be the lucky one — every week.**
> **每个人都值得成为幸运儿，每周都有机会。**

---

## 1. Name & Mascot / 名称与吉祥物

**English：**

**Bao** is both the token name and the project mascot. The Chinese name "宝" means treasure — a token of fortune. The mascot is a cute kung fu panda who believes "everyone can win, every week." Bao serves as the project's visual symbol and community mascot.

**中文：**

**宝（Bao）** 既是代币名称，也是项目吉祥物的名字。中文名为「宝」，意为珍宝、幸运之宝。吉祥物是一只可爱的功夫熊猫，它相信"人人都能赢，每周都有机会"，是项目的视觉符号与社区吉祥物。

---

## 2. Overview / 项目概述

**English：**

$BAO is a community-driven meme coin on the Solana blockchain. We believe crypto belongs to every participant — not a few whales.

Through a weekly fair lottery based on the SHA256 algorithm, $BAO returns **50% of project income (in SOL)** to the community, giving every holder a chance to be the week's lucky winner. All tokens are added to the liquidity pool at launch and the supply is fixed; the team holds no reserved allocation, fully aligned with community interests.

**中文：**

$BAO 是一个基于 Solana 区块链的社区驱动型 meme 币。我们相信加密货币的精神属于每一个参与者——而不是少数巨鲸。

通过基于 SHA256 算法的每周公平抽奖机制，$BAO 将项目收入的 **50%（以 SOL）** 回馈社区，让每个持仓者都有机会成为当周的幸运儿。所有代币在发行时全部投入流动性池、发行量固定，项目方无预留名额，与社区利益完全绑定。

---

## 3. The Problem / 要解决的问题

**English：**

| Current | Consequence |
|---|---|
| Large team reserves | Dump at highs |
| Whale concentration | Market manipulated |
| Opaque mechanics | Broken trust |
| Misaligned interests | Frequent rugs |

$BAO is designed to solve these problems.

**中文：**

| 现状 | 后果 |
|---|---|
| 项目方预留大量代币 | 高位砸盘 |
| 巨鲸集中持仓 | 拉砸由人 |
| 机制不透明 | 信任崩塌 |
| 项目方与社区利益脱节 | Rug Pull 频发 |

$BAO 的设计就是为了解决这些问题。

---

## 4. Token & Tokenomics / 代币与经济

**English：**

| Item | Spec |
|---|---|
| Name | Bao |
| Symbol | $BAO |
| Mascot | Cute kung fu panda |
| Chain | Solana |
| Supply | 1,000,000,000 — fixed, never inflated |
| Allocation | 100% into liquidity pool at launch; no team reserve |
| Trading fee | Charged per platform rules |

**中文：**

| 项目 | 设定 |
|---|---|
| 代币名称 | Bao（中文名：宝）|
| 代币符号 | $BAO |
| 吉祥物 | 可爱的功夫熊猫 |
| 区块链 | Solana |
| 发行量 | 1,000,000,000（10 亿）固定不变、永不增发 |
| 代币去向 | 发行时全部投入流动性池，项目方无预留名额 |
| 交易手续费 | 按平台规则收取 |

---

## 5. Revenue Distribution / 收入分配

**English：**

**50%** of project income goes into the community prize pool for the weekly lottery. The project is fully aligned with the community.

```
Project income
  ├── 50% → Community prize pool (weekly lottery)
  └── 50% → Project operations & development
```

**中文：**

项目收入的 **50%** 充入社区奖池，用于每周抽奖发放；项目方与社区利益完全绑定。

```
每期项目收入
  ├── 50% → 社区奖池（每周抽奖分发）
  └── 50% → 项目运营与发展
```

---

## 6. Weekly Lottery / 每周抽奖机制

**English：**

### 6.1 Eligibility
- Addresses with market value ≥ **$100** at snapshot
- **One ticket** per address, one person one vote
- The community group is where results are published, **not a sign-up portal**

### 6.2 Snapshot & Random Source
| Item | Rule |
|---|---|
| Snapshot | Every Monday 00:00:00 UTC |
| Seed | First confirmed tx hash after Monday 00:00, permanently retrievable on-chain |

### 6.3 Sorting
For each qualifying address compute:

```
sort_key(Ai) = SHA256(address + tx hash)
```

Number addresses by ascending lexicographic order of `sort_key` (1..N, N = total tickets).

### 6.4 Draw
```
r = int(tx hash, 16) % N + 1
winning numbers = r, r+1, r+2  (mod N; wraps back to 1)
```

Starting from #r, take 3 winners in cyclic order; they split the weekly pool equally:

```
amount_each = prize_sol / 3
```

**中文：**

### 6.1 参与资格
- 快照时持仓市值 ≥ **$100** 的地址
- 每个地址 **1 张券，一人一票**
- 社区群是**公布结果的场所**，不是报名入口

### 6.2 快照与随机源
| 项 | 规则 |
|---|---|
| 快照时点 | 每周一 00:00:00 UTC |
| 随机种子 | 周一 00:00 后第一个确认交易哈希，链上永久可查 |

### 6.3 排号
对每个合格地址计算：

```
sort_key(Ai) = SHA256(地址 + 交易哈希)
```

按 `sort_key` **字典序升序**编号（1..N，N=总票数）。

### 6.4 开奖
```
r = int(交易哈希, 16) % N + 1
中奖号 = r, r+1, r+2（对 N 取模，超出回到 1）
```

从第 r 号起**循环取模**抽 3 名中奖者，平分当周奖池：

```
amount_each = prize_sol / 3
```

---

## 7. Fairness & Anti-Sybil / 公平性与防女巫

**English：**

- Sorting decided by **SHA256**, verifiable by anyone
- Seed is a future tx hash, unpredictable before announced
- List locked before seed, no one can inject addresses
- Tx hash permanently on-chain, verifiable anytime
- **Anti-Sybil**: on-chain address-link detection merges suspected duplicate addresses into one ticket (one person, one vote); exceptional cases are handled via community report and public review; unflagged addresses participate normally

**中文：**

- 排序由 **SHA256** 数学决定，任何人可复算
- 随机种子是未来产生的交易哈希，公布前不可预测
- 名单先锁定、种子后产生，无人能塞名单
- 交易哈希永久上链，任何时间可读取复核
- **防女巫**：通过链上地址关联检测，将疑似重复来源的地址合并计 **1 张券**（一人一票）；异常情况经社区举报与公开复核处理，未被标记的地址正常参与

---

## 8. Payout & Rollover / 发放与保底

**English：**

| Time | Action |
|---|---|
| Monday 00:00 UTC | Snapshot + determine hash |
| Monday (announce) | Announce hash + winners + amount, on-chain |
| Mon–Thu | **3-day review window** |
| Thursday | Distribute SOL per list & amount |

- Review corrects but does **not re-draw**; disqualified replaced by next in order, remainder rolls over
- Pool holds **SOL**, 3 winners **split SOL directly** — no fluctuation, no buyback, no sell pressure
- If the pool is below **1 SOL**, no draw this week; it rolls over to the next period

**中文：**

| 时间 | 动作 |
|---|---|
| 周一 00:00 UTC | 快照 + 确定随机哈希 |
| 周一（公告日） | 同步公布哈希 + 名单 + 金额，上链留痕 |
| 周一至周四 | **3 日复查窗口** |
| 周四 | 确认无误后，按名单与金额发放 SOL |

- 复查只纠错、**不重抽**；剔除者按排号顺延递补，差额滚入下期
- 奖池持有 **SOL**，3 名中奖者**直接平分 SOL**——无波动、无回购、无套现卖压
- 奖池折合价值低于 **1 SOL** 时，本周不开奖，顺延至下期

---

## 9. Transparency / 透明度承诺

**English：**

- Prize pool address public, anyone can check balance
- Weekly: hash, winners, amounts
- Results & review basis on-chain
- Weekly announcement in community group

**中文：**

- 奖池地址公开，任何人可查余额
- 每周公布：哈希、中奖名单、中奖金额
- 结果与复核依据全部上链
- 社区群每周公示

---

## 10. Risk Disclosure / 风险提示

**English：**

- Crypto is highly risky, prices volatile
- Meme coins can go to zero
- Past performance ≠ future returns
- Only invest what you can afford to lose

**中文：**

- 加密货币投资风险极高，价格波动剧烈
- Meme 币可能随时归零
- 过往表现不代表未来收益
- 请只投入你能承受损失的金额

---

## 11. Disclaimer / 免责声明

**English：**

This whitepaper is informational only and **does not constitute investment advice**.

$BAO is a community entertainment project. Participation is **free**, driven by **holding**, and the pool comes from **project income** — it is not gambling or lottery-ticket sales.

Participation means you accept all terms.

**Not for US persons.**

**中文：**

本白皮书仅为项目介绍，**不构成任何投资建议**。

$BAO 是一个社区娱乐项目。抽奖为**免费参与**、由**持仓触发**、奖池来自**项目收入**，不构成任何形式的博彩或彩票销售。

参与即表示理解并同意全部条款。

**本项目不面向美国用户（Not for US persons）。**

---

*Every week, someone becomes the lucky one — and this week, it could be you. 🐼*
*每周都有人成为幸运儿——这周，可能就是你。🐼*
