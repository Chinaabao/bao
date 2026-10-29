# 宝($BAO) 每周抽奖 · 公告模板（中英对照）

> 用途：每周开奖后，按本模板向 X 与 Telegram 发布公示。**发放由项目方钱包签名执行，本公告只公示哈希、名单、金额与复查说明，不执行转账。**
> 数据来源由 `bao_lottery.py` 产出；哈希、名单、金额永久上链留痕可复核。

---

## 开奖公示 / Draw Announcement（公布时立即发）

**【中文】**

> 🐼 宝($BAO) 每周幸运抽奖 · 开奖公示
> 📅 期次：{period}
> 💰 奖池：{prize_sol} SOL　｜ 中奖者 {winners_n} 人，各得 {amount_each} SOL
> 🔗 种子交易哈希：{tx_hash}
> 🔢 开奖编号：r={r}　总票数 {n}　（SHA256(地址+哈希) 字典序排序，r=int(哈希,16)%总票数+1）
> 🏆 中奖名单：
> 1. {addr_1}
> 2. {addr_2}
> 3. {addr_3}
> ⏳ 复查窗口：公布后 3 天（纠错不重抽，剔除者按排号顺延递补，差额滚入下期）
> ✅ 发放：周四由项目方钱包按名单与金额签名发放
> 全部数据链上可复核，永久留痕。

**【EN】**

> 🐼 Bao($BAO) Weekly Lucky Draw · Results
> 📅 Round: {period}
> 💰 Prize Pool: {prize_sol} SOL ｜ Winners: {winners_n}, each {amount_each} SOL
> 🔗 Seed Tx Hash: {tx_hash}
> 🔢 Draw: r={r}, tickets {n} (SHA256(addr+hash) sort; r=int(hash,16)%n+1)
> 🏆 Winners:
> 1. {addr_1}
> 2. {addr_2}
> 3. {addr_3}
> ⏳ Review window: 3 days after announcement (errors fixed without redraw; alternates fill in order; surplus rolls to next round)
> ✅ Payout: signed & sent Thursday by project wallet
> All data verifiable on-chain.

---

## 发放完成确认 / Payout Confirmed（周四发放后发）

**【中文】**
> ✅ 宝($BAO) 第 {period} 期中奖发放已完成，{winners_n} 位幸运儿各收到 {amount_each} SOL。感谢参与，下周再见！🐼

**【EN】**
> ✅ Bao($BAO) Round {period} payouts completed. {winners_n} lucky winners each received {amount_each} SOL. See you next week! 🐼

---

## 补充话术（可选）

- **奖池空转说明**（奖池 < 1 SOL 顺延）：本期奖池不足 1 SOL，按规则顺延至下期合并开奖。
- **复查剔除递补**：如复查期内发现某中奖者不合规，按排号顺延递补，差额滚入下期。
- **保底滚存**：奖池折合价值 < 1 SOL 不开奖，顺延下期。

> 提示：以上 {period}、{prize_sol}、{winners_n}、{amount_each}、{tx_hash}、{r}、{n}、{addr_*} 由 `bao_lottery.py --period ... --prize-sol ... --tx-hash ...` 自动产出后填入。
