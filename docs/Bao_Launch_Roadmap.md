# Bao（$BAO）项目 · 上线与迁移路线图 v1.0 / Launch & Migration Roadmap
# 双语对照版：每节英文在前，中文在后 / Bilingual: English first, then Chinese

**English：**

> Purpose: turn the phased route — "GitHub self-hosting first → later buy domain → migrate off Pump to self-operated" — into an executable, verifiable roadmap. It covers three phases, milestones, a migration evaluation checklist, and cross-cutting items.

## 0. 总原则 / Guiding Principles

**English：**

- **Prove the mechanism on Pump, build a real community and liquidity first; talk about migration only afterwards.**
- Don't self-host early just to save platform fees — with no traffic, self-hosting only costs more money and effort.
- Full "serverless" path throughout: presentation layer on GitHub Pages / Vercel static hosting, functional layer on Serverless, assets via IPFS/Arweave.

**中文：**

- **先在 Pump 上跑通机制、攒出真实社区与流动性，再谈迁移。**
- 前期不要为省平台费提前自营——没流量时自营只会更费钱、更费劲。
- 全程"无服务器"路径：展示层用 GitHub Pages / Vercel 静态托管，功能层用 Serverless，素材走 IPFS/Arweave。

---

## 1. 三期路线总览 / Three-Phase Overview

**English：**

| Phase | Timing | Core goal | Hosting / chain |
|---|---|---|---|
| **Phase 1 · Cold-start validation** | At launch | Prove the mechanism on Pump, build community, establish brand | GitHub Pages + Serverless; token on Pump |
| **Phase 2 · Brand & mechanism deepening** | After community/liquidity grows | Buy domain, IP registration, launch merch & emoji mechanics | Domain binding; mechanism running |
| **Phase 3 · Self-operated migration** | When migration checklist is met | Migrate to self-operated contract + self-provided liquidity + DEX listing | Self-operated contract + Raydium, etc. |

**中文：**

| 阶段 | 时间定位 | 核心目标 | 托管/链 |
|---|---|---|---|
| **第一期 · 冷启动验证** | 上线即做 | 在 Pump 上跑通机制、建社区、立品牌 | GitHub Pages + Serverless；代币在 Pump |
| **第二期 · 品牌与机制深化** | 社区/流动性起来后 | 买域名、IP 登记、周边&表情机制上线 | 域名绑定；机制跑通 |
| **第三期 · 自营迁移** | 满足迁移评估清单后 | 迁出自营合约 + 自供流动性 + 上 DEX | 自营合约 + Raydium 等 |

---

## 2. 第一期 · 冷启动验证 / Phase 1 · Cold-Start Validation

**English：**

**Goal**: launch $BAO on Pump, prove the "weekly lottery + merch NFT + AI emoji pack" mechanism, and accumulate the first community and liquidity.

**Task list**
- [ ] Launch $BAO on Pump (supply 1B, fixed, all tokens to liquidity pool, no team reserve)
- [ ] GitHub Pages landing page: mascot, whitepaper link, mechanism intro, community entry
- [ ] Serverless functional layer (Cloudflare Workers / Vercel Functions):
  - Lottery results page (snapshot, seed hash, winners, amounts)
  - Merch NFT minting (burn 100 $BAO + small fee)
  - AI emoji creation (burn $BAO + fee, image / image-to-video API)
- [ ] Assets & metadata via IPFS/Arweave
- [x] Community on Telegram / X: X `https://x.com/Chinaabao`; Telegram `https://t.me/Chinaabao` (established)
- [ ] Complete & distribute all 8 animated emoji GIFs

**Milestones (acceptance)**
- Weekly lottery runs 2–4 consecutive periods per whitepaper with no major errors
- Community reaches a perceivable scale (per your target); liquidity initially established
- Landing page + functional layer fully accessible & operable

**中文：**

**目标**：在 Pump 上把 $BAO 发出去，跑通「每周抽奖 + 周边NFT + AI表情包」机制，攒出第一批社区与流动性。

**任务清单**
- [ ] 在 Pump 发行 $BAO（总量 10 亿、固定、所有代币投入流动性池、项目方无预留）
- [ ] GitHub Pages 上线展示页：吉祥物、白皮书链接、机制介绍、社区入口
- [ ] Serverless 功能层（Cloudflare Workers / Vercel Functions）：
  - 抽奖公示页（快照、哈希种子、中奖名单、金额）
  - 周边NFT铸造（烧 100 $BAO + 小额成本费）
  - AI 表情包创作（烧 $BAO + 成本费，图像/图生视频 API）
- [ ] 素材与元数据走 IPFS/Arweave
- [x] 建立 Telegram / X 社区：X `https://x.com/Chinaabao`；Telegram `https://t.me/Chinaabao`（已建立）
- [ ] 表情包动图 8 张全部完成并分发

**里程碑（验收）**
- 每周抽奖按白皮书机制连续运行 2-4 期，无重大差错
- 社区成员达到可感知规模（以你设定目标为准），流动性初步建立
- 展示页 + 功能层全流程可访问、可操作

---

## 3. 第二期 · 品牌与机制深化 / Phase 2 · Brand & Mechanism Deepening

**English：**

**Goal**: solidify the brand, add legal/IP protection, and mature the merch & emoji mechanics.

**Task list**
- [ ] Buy a domain (suggest low-cost suffix like `.xyz`, tens of RMB/year), bind to hosting
- [ ] **Mascot copyright registration** (whole + split poses/expressions, multiple works)
- [ ] **Trademark registration** (Bao image as brand mark, for merch products/services)
- [ ] Website ToS / privacy policy / disclaimer online (incl. Bao image usage license terms)
- [ ] Digital collectible cards / social assets (avatar frames, wallpapers) launch
- [ ] Merch NFT & AI emoji consumption tiers and fee settlement running
- [ ] Evaluate the real platform-fee share of transactions, prepare for migration

**Milestones (acceptance)**
- Domain stable; landing + functional pages share unified branding
- Copyright/trademark application accepted or certified
- All mechanisms stable and user-operable

**中文：**

**目标**：立住品牌，补上法律/IP 保护，周边与表情机制成熟。

**任务清单**
- [ ] 购买域名（建议 `.xyz` 等低成本后缀，一年几十块），绑定到托管
- [ ] **吉祥物著作权登记**（整体 + 拆分姿势/表情多件）
- [ ] **商标注册**（宝形象作为品牌标识，用于周边商品/服务）
- [ ] 网站 ToS / 隐私政策 / 免责声明上线（含宝形象使用许可条款）
- [ ] 数字收藏卡 / 社交资产（头像框、壁纸）上线
- [ ] 周边NFT 与 AI 表情包消耗分层、成本费结算跑通
- [ ] 评估平台费在交易中的实际占比，为迁移做准备

**里程碑（验收）**
- 域名稳定访问，展示页+功能页统一品牌
- 著作权/商标登记受理或已获证书
- 全部机制稳定运行，用户可自主操作

---

## 4. 第三期 · 自营迁移 / Phase 3 · Self-Operated Migration

**English：**

**Goal**: self-deploy the contract + self-provide liquidity + list on DEX, taking back the bulk of trading fees.

**Task list**
- [ ] Write the Solana contract (replicate or reimplement token, lottery & mint logic)
- [ ] **Contract security audit** (mandatory — against vulnerabilities / rug risk)
- [ ] Provide & lock LP (set lock period, anti-rug mechanism, build trust)
- [ ] List on DEX (Raydium, etc.), migrate existing liquidity
- [ ] Publish migration announcement, smooth transition (old/new pool handover, user notice)
- [ ] Fully switch to self-operated; platform fees belong to the project

**Milestones (acceptance)**
- Contract audit passed
- Liquidity migrated smoothly, no user asset loss
- Trading fees handled by self-operation; cost structure optimized

**中文：**

**目标**：自部署合约 + 自供流动性 + 上 DEX，把交易费大头收归自己。

**任务清单**
- [ ] 自写 Solana 合约（复制或重实现代币与抽奖/铸造逻辑）
- [ ] **合约安全审计**（必须，防漏洞/防 Rug 风险）
- [ ] 提供并锁定 LP（设锁定期、防 Rug 机制，建立信任）
- [ ] 上 DEX（Raydium 等），迁移现有流动性
- [ ] 公布迁移公告，平稳过渡（旧池/新池交接、用户告知）
- [ ] 全量切到自营，平台费归自己

**里程碑（验收）**
- 合约审计通过
- 流动性平稳迁移，无用户资产损失
- 交易费由自营承接，成本结构优化

---

## 5. 迁移评估清单 / Migration Evaluation Checklist

**English：**

> Go/no-go gate — migrate only when all items are met:

- [ ] Community & liquidity have scale (not the early cold-start stage)
- [ ] Platform fee is a real, data-backed cost burden
- [ ] You can bear the responsibility of contract security (audit + operations)
- [ ] You can provide initial liquidity and design LP-lock / anti-rug mechanisms
- [ ] Technical capacity/resources suffice to write & maintain contract & frontend
- [ ] Migration plan announced to community; transition contingency ready

> If any item is unmet, stay on Pump and keep running; do not force migration.

**中文：**

> go/no-go 门，全部满足才迁：

- [ ] 社区与流动性已具规模（不是早期冷启动阶段）
- [ ] 平台费确实成为明显成本负担（有真实数据支撑）
- [ ] 你能承担合约安全（审计 + 运维）责任
- [ ] 有可提供的初始流动性，且能设计锁 LP / 防 Rug 机制
- [ ] 技术能力/资源足以自写并维护合约与前端
- [ ] 迁移方案已告知社区，过渡期预案就绪

> 任一不满足，就继续留在 Pump 上跑，不强行迁移。

---

## 6. 贯穿全程的事项 / Cross-Cutting Items

**English：**

- **Compliance framing**: per the whitepaper — digital merch NFT risk is lower than the token; user- & market-facing compliance is the responsibility of the operating jurisdiction; the whitepaper includes the "Not for US persons" disclaimer.
- **IP protection**: copyright/trademark registration + website ToS usage license + infringement enforcement fallback; on-chain records are evidence/traceability only, not legal protection.
- **Cost mechanism**: AI emoji / merch NFT charge a small fee to cover compute; 50/50 into prize pool & operations, aligned with the whitepaper revenue split.
- **Security**: users self-sign wallets, multi-sig admin, review before on-chain, private keys never shipped to frontend.

**中文：**

- **合规口径**：延续白皮书既定框架——数字周边NFT风险低于代币；面向用户与市场合规由实际运营所在地负责；白皮书含 "Not for US persons" 免责。
- **IP 保护**：著作权/商标登记 + 网站 ToS 使用许可 + 侵权执法兜底；链上记录只当证据/溯源，不当法律保护。
- **成本机制**：AI 表情 / 周边NFT 收小额成本费覆盖算力，50/50 进奖池与运营，与白皮书收入分配对齐。
- **安全**：用户钱包自签、admin 多签、上链前审核、私钥绝不下发前端。

---

## 7. 与已交付资产的对接 / Alignment with Delivered Assets

**English：**

| Asset delivered | Use in the roadmap |
|---|---|
| Whitepaper v1.0 (bilingual) | Core content of landing page + mechanism basis |
| Mascot static assets (9-expression sheet, final kung fu poses) | Brand visuals, asset library, identity anchors for NFT / AI creation |
| Animated emoji GIFs (8, in progress) | Digital merch spread, social assets |
| Merch NFT technical plan | Phase 2/3 minting implementation |
| Copyright/trademark, AI-emoji mechanism, integration & cost plan | Phase 2 rollout |

**中文：**

| 已有资产 | 在路线图中的用途 |
|---|---|
| 白皮书 v1.0（中英对照） | 展示页核心内容 + 机制依据 |
| 吉祥物静态资产（表情九宫格、练功姿势终版） | 品牌视觉、素材库、周边NFT/AI创作的身份锚点 |
| 表情包动图（8 张，进行中） | 数字周边传播、社交资产 |
| 周边NFT技术搭建方案 | 第二/三期铸造实现 |
| 著作权/商标、AI表情机制、接入与成本方案 | 第二期落地 |

---

*Document for internal planning reference; timing and scale follow your actual resources and community feedback, and can be detailed per phase.*
*文档供项目内部规划参考；时间点与规模以你实际资源与社区反馈为准，可按阶段细化执行。*
