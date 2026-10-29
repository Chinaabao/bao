# 宝（$BAO）周边NFT创作机制 · 技术搭建方案 / Merch NFT Technical Plan
# 双语对照版：每节英文在前，中文在后 / Bilingual: English first, then Chinese

**English：**

> Version: v1.0 · Purpose: turn the "burn 100 $BAO → create & mint a merch NFT with the Bao image" mechanism into an executable technical plan.
> This doc covers: overall architecture, selection list, step-by-step rollout, contract logic, metadata spec, frontend flow, review/AI generation, cost estimate, security & compliance, and a launch checklist.

## 0. 一句话结论 / One-Sentence Conclusion

**English：**

**Zero self-hosted server for on-chain minting** (Solana is the backend); assets & metadata use decentralized storage (IPFS/Arweave) for permanent retrievability; frontend is static-hosted; review & AI generation run on Serverless. The whole flow needs no VPS, no rented cloud host, and no always-on server to operate.

**中文：**

**链上铸造零自建服务器**（Solana 就是后端）；素材与元数据用去中心化存储（IPFS/Arweave）保证永久可查；前端静态托管；审核与 AI 生成用 Serverless（无服务器函数）。全流程不需要你买 VPS、租云主机、自己运维任何常驻服务器。

---

## 1. 整体架构 / Overall Architecture

**English：**

```
┌────────────────────────────── User side ──────────────────────────────┐
│ Browser/Mobile → Frontend creation page (connect Phantom etc.)         │
└───────────────┬───────────────────────────────────────────────────────┘
                │ ① Pick asset/params, preview
                ▼
        ┌──────────────── Serverless backend (optional, on-demand) ─────┐
        │  Cloudflare Workers / Vercel Functions / Lambda               │
        │  · Call AI to generate merch image · Call image-review API    │
        │  · Upload image & metadata to IPFS/Arweave, return mint data  │
        └───────────────┬───────────────────────────────────────────────┘
                │ ② Return metadata URI + preview image
                ▼
        ┌──────────────── Decentralized storage ────────────────────────┐
        │  IPFS (Pinata) or Arweave: merch image + metadata JSON        │
        └───────────────┬───────────────────────────────────────────────┘
                │ ③ User wallet signs & submits directly (server not involved)
                ▼
        ┌──────────────── On-chain Solana ──────────────────────────────┐
        │  Program: burn 100 $BAO + Metaplex mint NFT (one tx)          │
        └───────────────┬───────────────────────────────────────────────┘
                ▼
        NFT enters user wallet → listable on Tensor / Magic Eden
```

**中文：**

```
┌────────────────────────────── 用户端 ──────────────────────────────┐
│ 浏览器/手机 → 前端创作页（连 Phantom 等 Solana 钱包）                 │
└───────────────┬───────────────────────────────────────────────────┘
                │ ① 选素材/参数、预览
                ▼
        ┌──────────────── Serverless 后端（可选，按需触发）───────────┐
        │  Cloudflare Workers / Vercel Functions / Lambda           │
        │  · 调 AI 生成周边图   · 调图片审核 API 做入链前过滤          │
        │  · 把图和元数据上传到 IPFS/Arweave，返回准备好的铸造数据      │
        └───────────────┬───────────────────────────────────────────┘
                │ ② 返回元数据 URI + 预览图
                ▼
        ┌──────────────── 去中心化存储 ──────────────────────────────┐
        │  IPFS（Pinata）或 Arweave：周边图 + 元数据 JSON（永久）      │
        └───────────────┬───────────────────────────────────────────┘
                │ ③ 用户钱包直接发起交易（你的服务器全程不参与）
                ▼
        ┌──────────────── Solana 链上 ──────────────────────────────┐
        │  Program：烧毁 100 $BAO + 调用 Metaplex 铸造 NFT           │
        └───────────────┬───────────────────────────────────────────┘
                ▼
        NFT 进入用户钱包 → 可挂 Tensor / Magic Eden 等 Solana NFT 市场流转
```

**English：**

**Core design**: the minting transaction is signed and submitted directly by the user wallet — the project holds no private keys, has no middle link, and the on-chain logic is transparent & auditable.

**中文：**

**核心设计**：铸造型交易由用户钱包直接签名并提交上链，项目方无托管私钥、无中间环节，链上逻辑透明可审计。

---

## 2. 选型清单 / Selection List

**English：**

| Stage | Preferred | Alternative | Self-hosted server |
|---|---|---|---|
| On-chain contract | **Solana + Anchor** (custom burn+mint) | Metaplex Candy Machine + custom guard | ❌ |
| Wallet connect | Phantom / Solflare wallet adapter (frontend SDK) | Any Solana wallet | ❌ |
| Assets & metadata | **IPFS (Pinata)** or **Arweave (Irys)** | Shadow Drive | ❌ (hosted) |
| Frontend | **Static site** on Vercel / Netlify | GitHub Pages | ❌ (static) |
| Review + AI generation | **Cloudflare Workers / Vercel Functions** | AWS Lambda | ❌ (serverless) |
| Chain explorer | Solscan / Solana Explorer | — | ❌ |

**中文：**

| 环节 | 首选 | 备选 | 是否自建服务器 |
|---|---|---|---|---:|
| 链上合约 | **Solana + Anchor**（自写 burn+mint 合约） | Metaplex Candy Machine + 自定义 guard | ❌ |
| 钱包连接 | Phantom / Solflare 钱包适配器（前端 SDK） | 任意支持 Solana 的钱包 | ❌ |
| 素材与元数据 | **IPFS（Pinata）** 或 **Arweave（Irys）** | Shadow Drive | ❌（服务商托管） |
| 前端 | **静态站**托管在 Vercel / Netlify | GitHub Pages | ❌（静态托管） |
| 审核 + AI 生成 | **Cloudflare Workers / Vercel Functions** | AWS Lambda | ❌（Serverless 按需跑） |
| 链上浏览器 | Solscan / Solana Explorer | — | ❌ |

**English：**

> All choices follow the "no self-owned server" path. If you later need admin whitelisting, batch management, or an ops dashboard, add one Serverless API — still no always-on server.

**中文：**

> 全选型均为「无自有服务器」路径。若你后续要做后台白名单、批量管理、运营数据大屏，再考虑加一个 Serverless API 即可，仍无需常驻服务器。

---

## 3. 分步落地 / Step-by-Step Rollout

**English：**

### Phase A: Testnet validation (recommended first, cost ≈ 0)
1. Deploy the contract on **Solana Devnet**, claim test tokens via `solana airdrop`.
2. Deploy a test $BAO (on Devnet), verify the full "burn 100 → mint 1" flow.
3. Run on testnet: connect wallet → create → review → mint → NFT in wallet.

### Phase B: Asset preparation
4. Build the **official Bao asset library**: expressions, poses, scene templates (can reuse the delivered emoji pack / kung fu poses / white-background main image).
5. Define creation freedom & rarity rules (see §7), write into frontend config.

### Phase C: Contract & backend
6. Write the `burn_buy_mint` contract in Anchor (see §4).
7. Deploy Serverless: AI generation + image review + storage upload (see §6).
8. Frontend integrates wallet adapter + creation studio + mint button.

### Phase D: Mainnet launch
9. Deploy the contract on mainnet, reset permissions & guards.
10. Small-scale grayscale (capped minting) → full open.
11. After opening, list on Tensor / Magic Eden markets.

**中文：**

### 阶段 A：测试网验证（推荐先做，成本≈0）
1. 在 **Solana Devnet** 上部署合约，用 `solana airdrop` 领测试币。
2. 部署测试版 $BAO（Devnet 上的代币），验证「烧 100 → 铸 1」全流程。
3. 在测试网跑通：连接钱包 → 创作 → 审核 → 铸造 → NFT 入钱包。

### 阶段 B：资产准备
4. 建立**宝官方素材库**：表情、姿势、场景模板（可直接复用已交付的表情包/练功姿势/白底主形象）。
5. 确定创作自由度与稀有度规则（见第 7 节），写进前端配置。

### 阶段 C：合约与后端
6. 用 Anchor 写 `burn_buy_mint` 合约（见第 4 节）。
7. 部署 Serverless：AI 生成 + 图片审核 + 上传存储（见第 6 节）。
8. 前端接入钱包适配器 + 创作工作室 + 铸造按钮。

### 阶段 D：主网上线
9. 主网部署合约，重新设置权限与 guard。
10. 小规模灰度（限额铸造）→ 全量开放。
11. 开放后接入 Tensor / Magic Eden 市场列表。

---

## 4. 合约逻辑 / Contract Logic

**English：**

**Recommended**: write a custom Solana Program that completes "burn + mint" in a **single transaction**, with atomicity guaranteeing no "burned but not minted".

```
instruction burn_and_mint(input):
  # 1) validate
  assert user wallet holds >= 100 $BAO
  assert mint slot not occupied / passed guard

  # 2) burn 100 $BAO (transfer to a dead address, or call spl-token burn)
  spl_token_burn(from=user, mint=$BAO, amount=100)

  # 3) mint NFT (CPI to Metaplex token_metadata)
  metaplex_mint_new_edition(mint=newNFT, metadata_uri=prepared IPFS/Arweave URI)

  # 4) optional: collect mint fee (small SOL) → split 50/50 per whitepaper
  transfer_sol(fee, to=prize-pool & operations accounts)
```

**中文：**

**推荐方案**：自写 Solana Program，在**同一笔交易**里完成"烧币 + 铸造"，原子性保证不会"烧了币没铸成"。

```
指令 burn_and_mint(input):
  # 1) 校验
  assert 用户钱包持有 >= 100 $BAO
  assert 该铸造名额未被占用 / 或已通过 guard 校验

  # 2) 烧毁 100 $BAO（转到一个不可用/销毁地址，或调用 spl-token burn）
  spl_token_burn(from=user, mint=$BAO, amount=100)

  # 3) 铸造 NFT（CPI 调用 Metaplex token_metadata）
  metaplex_mint_new_edition(mint=新NFT, metadata_uri=提前准备好的IPFS/Arweave URI)

  # 4) 可选：收取铸造手续费（小额 SOL）→ 按白皮书 50/50 分配
  transfer_sol(fee, to=奖池账户与运营账户)
```

**English：**

**Comparison of two approaches**

| Approach | Pros | Cons |
|---|---|---|
| A. Custom Anchor contract (recommended) | Fully custom atomic burn+mint, transparent logic | Needs Solana dev skill (Anchor/Rust) |
| B. Metaplex Candy Machine + custom guard | Official tool (Sugar), mature community | Burning custom token needs extra guard; limited customization |

> Suggestion: start with B (Candy Machine) to ship MVP fast, migrate to A (custom contract) for full customization once there is volume.

**中文：**

**两种落地方式对比**

| 方式 | 优点 | 缺点 |
|---|---|---|
| A. Anchor 自写合约（推荐） | 完全自定义 burn+mint 原子逻辑、逻辑透明 | 需要一定 Solana 开发能力（Anchor/Rust） |
| B. Metaplex Candy Machine + 自定义 guard | 用官方工具（Sugar）部署，社区成熟 | 烧自定义代币需额外写 guard，定制受限 |

> 建议：先走 B（Candy Machine）快速跑通 MVP，等有量再迁到 A 自写合约做完整定制。

---

## 5. 元数据规范 / Metadata Spec

**English：**

Each NFT's metadata JSON must include (on-chain permanent — be sure to write the license terms in):

```json
{
  "name": "宝·开心贴纸 #0001",
  "symbol": "BAO",
  "description": "社区成员用 100 $BAO 创作的宝(Bao)官方周边NFT。",
  "image": "ipfs://<CID>",
  "attributes": [
    { "trait_type": "表情", "value": "开心" },
    { "trait_type": "稀有度", "value": "1/1" },
    { "trait_type": "创作者", "value": "<用户钱包地址前6位>" }
  ],
  "properties": {
    "license": "仅限以宝(Bao)形象创作周边并转售；禁止商用盗印实物、禁止贬损形象、禁止违法违规用途。",
    "files": [{ "uri": "ipfs://<CID>", "type": "image/png" }]
  }
}
```

**中文：**

每件 NFT 的 metadata JSON 必须包含（链上永久，务必把授权条款写进去）：

```json
{
  "name": "宝·开心贴纸 #0001",
  "symbol": "BAO",
  "description": "社区成员用 100 $BAO 创作的宝(Bao)官方周边NFT。",
  "image": "ipfs://<CID>",
  "attributes": [
    { "trait_type": "表情", "value": "开心" },
    { "trait_type": "稀有度", "value": "1/1" },
    { "trait_type": "创作者", "value": "<用户钱包地址前6位>" }
  ],
  "properties": {
    "license": "仅限以宝(Bao)形象创作周边并转售；禁止商用盗印实物、禁止贬损形象、禁止违法违规用途。",
    "files": [{ "uri": "ipfs://<CID>", "type": "image/png" }]
  }
}
```

**English：**

> Writing the license into metadata = minting is deemed acceptance of the terms; on-chain record, permanently verifiable.

**中文：**

> 授权许可写在 metadata 里 = 铸造即视为接受条款，链上留痕、永久可查。

---

## 6. 审核与 AI 生成 / Review & AI Generation

**English：**

- **AI generation**: user inputs params / picks template → Serverless calls image-generation API → produces Bao-themed merch image.
- **Pre-onchain review**: call image-review API (prohibited / stolen / vulgar filter) → only approved content may upload & mint.
- **Storage upload**: after approval, Serverless uploads to IPFS/Arweave, generates metadata URI, returns to frontend.
- **Why review is mandatory**: on-chain content is permanent and cannot be removed; pre-onchain gatekeeping is the final barrier.

> The review basis can be written into on-chain metadata or recorded separately for traceability.

**中文：**

- **AI 生成**：用户输入参数/选择模板 → Serverless 调图像生成 API → 产出宝主题周边图。
- **入链前审核**：调用图片审核 API（违禁/盗图/低俗过滤）→ 通过才允许上传与铸造。
- **上传存储**：通过后由 Serverless 上传到 IPFS/Arweave，生成 metadata URI 返回给前端。
- **为什么必须审核**：链上内容永久、撤不掉，入链前把关是最后一道闸。

> 审核的判定依据可写入链上元数据或单独记录，保持可追溯。

---

## 7. 规则与稀有度 / Rules & Rarity

**English：**

| Item | Suggestion |
|---|---|
| Consumption | Burn 100 $BAO (deflationary); optionally add a small SOL mint fee |
| Creation | Official asset-library combos (expression × pose × scene template), controllable series |
| Limited | Support both 1/1 unique and limited N editions |
| Rarity | Clearly priced; **no random blind-box draws** (avoid blind-box/gambling regulation) |
| Revenue | Mint fee / trading royalty split 50/50 per whitepaper: prize pool + operations |

**中文：**

| 项 | 建议 |
|---|---|
| 消耗 | 烧毁 100 $BAO（通缩）；可选每件再加小额 SOL 铸造费 |
| 创作 | 官方素材库组合（表情×姿势×场景模板），成系列可控 |
| 限量 | 支持 1/1 独一份 与 限量 N 份 两种 |
| 稀有度 | 明码定价，**不做随机盲盒抽取**（规避盲盒/博彩监管） |
| 收益 | 铸造费/交易版税按白皮书 50/50：奖池 + 运营 |

---

## 8. 成本估算 / Cost Estimate

**English：**

| Item | Cost |
|---|---|
| Solana tx fee | A few cents each (<0.01 SOL, mainnet) |
| Devnet testing | Free |
| Metadata + image storage | IPFS Pinata free tier or by volume; Arweave one-time permanent ≈ $0.5–1/MB |
| Serverless review + generation | Per-call billing; negligible at low volume |
| Mainnet deployment | Small one-time (account rent + deploy fee) |

> The cost driver is not infrastructure but AI-generation & review API calls — controllable by volume.

**中文：**

| 项 | 成本 |
|---|---|
| Solana 交易手续费 | 每笔约几美分（<0.01 SOL，主网） |
| Devnet 测试 | 免费 |
| 元数据+图存储 | IPFS Pinata 免费档或按量；Arweave 一次性永久约 $0.5–1/MB |
| Serverless 审核+生成 | 按调用次数计费，量小几乎可忽略 |
| 主网部署 | 少量一次性（账户租金 + 部署费） |

> 成本大头不是基础设施，而是 AI 生成与审核的 API 调用量，可按量控制。

---

## 9. 安全与合规要点 / Security & Compliance

**English：**

- **Private-key safety**: the project holds no user private keys; minting transactions are signed by the user wallet, preventing man-in-the-middle theft.
- **Permission management**: contract sets admin authority; guard/fee/whitelist updatable; use multi-sig for fund changes.
- **Review fallback**: pre-onchain review + license embedded in metadata; zero tolerance for stolen/prohibited content.
- **Avoid "blind-box / random draw" characterization**: rarity clearly priced, no random draws, lowering blind-box/gambling regulatory risk.
- **Compliance framing**: per the whitepaper — digital goods (merch NFT) are inherently lower-risk than the token; user- & market-facing compliance is the responsibility of the operating jurisdiction; the whitepaper includes the "Not for US persons" disclaimer.

**中文：**

- **私钥安全**：项目方无托管用户私钥；铸造型交易由用户钱包签名，杜绝中间人盗币。
- **权限管理**：合约设 admin authority，guard/费率/白名单可更新；涉及资金变动用多签。
- **审核兜底**：上链前审核 + metadata 内嵌使用许可；对盗图/违禁内容 0 容忍。
- **避免"盲盒/随机抽奖"定性**：稀有度明码定价，不做随机抽取，降低触碰盲盒/博彩监管的风险。
- **合规口径**：延续白皮书既定框架——数字商品（周边NFT）本身风险低于代币；面向用户与市场合规由项目实际运营所在地负责，白皮书含 "Not for US persons" 免责，不面向美国人士。

---

## 10. 上线检查清单 / Launch Checklist

**English：**

- [ ] Devnet full flow works (connect wallet → create → review → burn → mint → visible in wallet)
- [ ] Metadata contains license + creator + rarity, permanently retrievable
- [ ] Image-review pass rate & prohibited-block behavior normal
- [ ] Contract permissions (admin/multi-sig) configured; fee & guard verified
- [ ] Mainnet grayscale capped mint → observe → full open
- [ ] Listed on Tensor / Magic Eden; visible & tradable
- [ ] Revenue 50/50 (prize pool + operations) split logic tested

**中文：**

- [ ] Devnet 全流程跑通（连钱包→创作→审核→烧币→铸造→钱包可见）
- [ ] 元数据含版权许可 + 创作者 + 稀有度，且永久可查
- [ ] 图片审核通过率、违禁拦截情况正常
- [ ] 合约权限（admin/多签）配置完成，费率与 guard 验证无误
- [ ] 主网灰度限额铸造 → 观察后全量开放
- [ ] 接入 Tensor / Magic Eden 列表，市场可见、可交易
- [ ] 收益 50/50（奖池+运营）分配逻辑测试通过

---

*Document for internal rollout reference; concrete tech implementation follows the latest official Solana / Metaplex docs and testnet testing.*
*文档供内部落地参考；具体技术实现请以 Solana / Metaplex 官方最新文档与测试网实测为准。*
