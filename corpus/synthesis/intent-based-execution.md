---
id: synthesis-intent-based-execution
source: synthesis
source_url: null
title: "Intent-Based Execution & Order Flow: pattern, variants, audit checklist"
ingested_at: 2026-06-04T00:00:00Z
vuln_class:
  - mev
  - front-running
  - signature-replay
  - slippage
  - access-control
  - price-manipulation
  - dos
protocol_category:
  - dex
  - intent-settlement
  - clob
  - otc
  - cross-chain-bridge
tags:
  - synthesis
  - intent-based-execution
  - solver
  - order-flow
  - cow-protocol
  - mev
derives_from:
  - arxiv-2602.17805
  - arxiv-2603.04168
  - arxiv-2605.04471
  - arxiv-2603.26290
  - solodit-zokyo-2024-06-09-elektrik-0-0
  - solodit-trust-security-2023-05-15-brahma-2-3
  - solodit-trust-security-2023-05-15-brahma-2-0
  - solodit-hexens-2025-02-21-1inch-0-0
  - solodit-hexens-2025-02-21-1inch-1-3
  - solodit-cyfrin-2026-03-04-cyfrin-ethcf-swapboard-v2-0-0-0
  - solodit-cyfrin-2026-03-04-cyfrin-ethcf-swapboard-v2-0-0-1
  - solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-0-1
  - solodit-cyfrin-2026-04-07-cyfrin-myriad-pr145-v2-0-1-0
  - solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-3
  - solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-0
  - solodit-zokyo-2023-12-11-limit-break-0-2
  - solodit-zokyo-2023-12-11-limit-break-1-0
  - solodit-hexens-2025-14-03-mintify-1-1
  - solodit-pashov-audit-group-2023-11-01-pump-1-1
  - rekt-ripmevbot
  - rekt-ripmevbot2
  - rekt-moneyfornothing
  - swc-114
---

# Intent-Based Execution & Order Flow

## Pattern

Intent-based architectures decouple **what** a user wants from **how** it
gets executed. The user signs an *intent* (or limit order) — a struct
that declares a desired outcome (sell ≤ X of token A, receive ≥ Y of
token B, by some deadline) — and hands it to a permissionless off-chain
agent. That agent appears under many names: **solver** (CoW Protocol),
**facilitator** (Elektrik), **filler** (Across, deBridge, FloodPlain),
**taker** (0x/limit-order systems), or **operator** (Myriad CLOB). The
agent competes — often in an auction — to settle the intent on-chain,
fronting its own liquidity, batching/matching counterparties, routing
across venues, and pocketing whatever surplus it can. The **settlement
contract is the trust boundary**: the solver is free to execute however
it likes, so long as the contract verifies the user's signature and
enforces the constraints the user actually signed (limit price, fees,
deadline, recipient). The OMNIINTENT framework (arxiv-2603.04168) frames
this as the core tension of the intent-centric paradigm — letting users
specify intents instead of execution details trades off expressiveness
against trust, privacy, and composability.

Bugs cluster wherever the contract **fails to bind a constraint the user
assumed was enforced**, or wherever the solver/operator's privileged
position (timing, ordering, exclusive order flow, fronted liquidity)
lets it extract value the user did not consent to give. Because the
solver is economically motivated and frequently the only party who can
settle (whitelisted takers, exclusive order flow), an under-constrained
order is not just sub-optimal — it is an open option the solver will
exercise against the user.

A second, infrastructure-layer dimension is **order flow itself as a
traded asset**. Once intents are routed off the public mempool into
private channels and solver/builder relationships, the right to execute
(and to reorder) becomes valuable and concentrating. arxiv-2605.04471
shows Exclusive Order Flows (EOFs) and non-atomic MEV account for the
majority of trading-related builder revenue and drive builder
centralization; arxiv-2603.26290 formalizes Principal-Execution-
Beneficiary (PEB) separation, where intent originator, executor (e.g.
MEV searcher), and ultimate beneficiary are functionally decoupled. The
auditor's job spans both layers: the on-chain settlement contract *and*
the economic assumptions about who routes, fronts, and orders the flow.

## Variants

### V1: Solver/facilitator surplus capture & unrepaid fronted liquidity

The solver fronts liquidity or borrows from a vault to satisfy the
intent, then keeps any positive slippage ("surplus"). The contract must
(a) enforce the user's signed minimum-out and (b) verify the solver's
books actually balance. In **Elektrik** (solodit-zokyo-2024-06-09-
elektrik-0-0), a `Facilitator` could borrow assets from the vault via
`_processFacilitatorInteraction` with *no on-chain check that the
borrowed assets were repaid* — accepted as a design choice (the extra
token is the facilitator's CoW-style incentive), but a clear case where
solver economics live outside contract invariants. In **Myriad**
(solodit-cyfrin-2026-04-07-cyfrin-myriad-pr145-v2-0-1-0), price-overlap
surplus `(1 − price_YES − price_NO) × fill` was *gifted to one
counterparty* as price improvement instead of being swept to the
protocol's `feeModule` as the cross-market path did — the contract did
not hold each side to its own signed limit.

### V2: Solver liquidity concentration / liquidity-exhaustion attacks

Intent-based cross-chain bridges let off-chain solvers immediately
fulfill orders by fronting their own liquidity, which introduces
systemic risk: solver liquidity concentration and delayed settlement.
arxiv-2602.17805 analyzes 3.5M intents ($9.24B) across Mayan Swift,
Across, and deBridge and introduces *liquidity-exhaustion attacks*:
rational attackers profit against high-solver-margin protocols
(deBridge: 80.5% of attacks profitable), and Byzantine attackers can
suppress availability across all three (failed intents and solver losses
of up to ~$978 roughly every 16 minutes). Across resisted due to low
solver margins and deep liquidity. Takeaway: a protocol that leans on a
small set of solvers fronting capital inherits a liveness/availability
attack surface that contract review alone won't surface.

### V3: Signed-order integrity gaps (missing fields, replay, ERC-1271)

The intent is a signature over a struct, so **any economically relevant
field not in the signed payload can be swapped by the executor**. In
**Limit Break** (solodit-zokyo-2023-12-11-limit-break-1-0), `feeOnTop`
was not part of the signature, so a knowledgeable taker could lift the
maker's signature off the marketplace and execute directly with *zero
fees*. Cross-deployment replay is the dual failure: in solodit-zokyo-
2023-12-11-limit-break-0-2, the EIP-712 domain separator was not asserted
against the contract's actual chain/address, so a signature from one
chain could be replayed on another. Conversely, validating signatures
with bare `ECDSA.tryRecover` (solodit-cyfrin-2026-03-13-cyfrin-myriad-
clob-v2-0-2-3) *excludes* smart-contract wallets (Safe, ERC-4337) that
cannot produce EOA signatures — fixed by `SignatureChecker.
isValidSignatureNow` (ECDSA + ERC-1271).

### V4: No expiry — the order as a perpetual free option

Signed orders without an enforced deadline are free options the
counterparty exercises only when the market moves in its favor. In
**Swapboard** (solodit-cyfrin-2026-03-04-cyfrin-ethcf-swapboard-v2-0-0-0),
orders had no `deadline` field and stayed fillable indefinitely — an
order selling 1 WETH for 2,000 USDC remains a 50%-below-market gift
after ETH doubles. The mirror-image issue (solodit-cyfrin-2026-03-04-
cyfrin-ethcf-swapboard-v2-0-0-1) is the **taker-side fill deadline**:
without one, a filler's transaction can sit in the mempool during
congestion and execute later at a now-unfavorable rate (the same reason
Uniswap routers carry `deadline`). Mature systems (0x, CoW Protocol,
1inch, Myriad CLOB) put expiry on the order *and* allow a fill deadline.

### V5: Front-running of fills / cancellations and escrow reinitialization

Settlement is ordering-sensitive (SWC-114, transaction order
dependence). In **1inch Fusion** (solodit-hexens-2025-02-21-1inch-0-0,
rated Critical), an escrow PDA derived from `(seed, maker, order_id)` was
fully closed on cancel, allowing **reinitialization with the same
order_id**; an attacker front-runs the taker's `fill` and swaps in a
malicious order (worse rate, higher fees, or a native-asset switch that
drains the taker's SOL) at the same escrow address. In **Pump**
(solodit-pashov-audit-group-2023-11-01-pump-1-1), a maker's `cancel`
could be front-run by `fulfill`, forcing the order to execute anyway.
Defenses: bind a nonce/order hash that cannot be reused after close,
gate fills/cancels against reordering, and let users set fill deadlines.

### V6: Privileged operator/relayer timing and off-chain trust anchors

When a trusted operator/relayer controls *when* settlement happens, it
can exploit any value that floats between sign-time and settle-time. In
**Myriad CLOB** (solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-0),
the `Order` struct had no `maxFeeBps`; fees are read from `FeeModule` at
settlement, so a fee change between signing and settlement charges the
user a rate they never agreed to — even a good-faith operator harms
users, and a malicious one could settle at 100% BPS. When an **off-chain
signing/quoting API** is the trust anchor (solodit-hexens-2025-14-03-
mintify-1-1), a failure of that API to validate `amount`/`owed` enables
direct theft on-chain; the fix is defense-in-depth on-chain validation
of amounts/limits rather than relying solely on the API.

### V7: Settlement-hook / fulfiller-callback spoofing

Intent settlement contracts often run arbitrary pre/post hooks and
fulfiller callbacks. In **FloodPlain** (solodit-cyfrin-2025-06-10-cyfrin-
bunni-v2-1-0-1, High), a `SELECTOR_EXTENSION` guard meant to stop hooks
from invoking the fulfiller callback was only a "magic value" check; an
attacker controlling the extension bytes (and the fact that it guarded
`sourceConsiderations` but not the overloaded `sourceConsideration`)
could route a malicious Flood order so the hook executes an arbitrary
external call against a victim fulfiller — risking dangling approvals
that are drained later. Settlement hooks must restrict callable
targets/selectors and validate `msg.sender`.

### V8: Order flow as an extractable/centralizing asset

At the infrastructure layer, routing intents off the public mempool
turns order flow into a traded, concentrating asset. arxiv-2605.04471
identifies 75 Exclusive Order Flows and 322 non-atomic MEV flows that
account for 71% and 23% of trading-related builder revenue, and argues
builder centralization is an *emergent property* of PBS. arxiv-2603.26290
formalizes PEB separation (originator ≠ executor ≠ beneficiary), which
characterizes solver/searcher economics (and is abused for AML evasion).
The execution agents themselves are attack surface: **0xbad / RIP MEV
BOT** (rekt-ripmevbot) and **RIP MEV Bot 2** (rekt-ripmevbot2) were both
drained because their on-chain execution/swap functions lacked access
control, and **Money for Nothing** (rekt-moneyfornothing) shows the
proposer capturing ~98% of an MEV bot's backrun as a bribe — order-flow
value accrues to whoever controls ordering. A related on-chain symptom:
1inch Fusion allowed maker==taker self-fills (solodit-hexens-2025-02-21-
1inch-1-3), enabling wash-volume inflation and reward farming.

## Audit checklist

- Are **all economically relevant order fields** (price/limit, fees and
  `feeOnTop`, deadline, recipient, token in/out, slippage) inside the
  EIP-712 signed payload, so the executor cannot swap them?
  [limit-break-1-0]
- Does the **domain separator bind chainId and contract address**, and is
  it asserted against the actual deployment, to block cross-chain /
  cross-deployment signature replay? [limit-break-0-2]
- Is signature validation done via `SignatureChecker` (ECDSA **and**
  ERC-1271) so smart-contract / AA wallets can sign intents?
  [myriad-clob-v2-0-2-3]
- Does the order carry an **expiration the contract enforces**, so it
  isn't a perpetual free option? [swapboard-0-0]
- Can the **filler/taker set a fill deadline** to avoid stale mempool
  execution during congestion? [swapboard-0-1]
- Is there a signed **`maxFeeBps`** (or fully signed fee) so a privileged
  operator can't change fees between sign-time and settle-time?
  [myriad-clob-v2-0-3-0]
- Does settlement enforce each side's **signed minimum-out / limit**, and
  **sweep solver surplus** to the user or protocol rather than gifting it
  to a counterparty? [elektrik-0-0, myriad-pr145-0-1-0]
- If a solver/facilitator **fronts or borrows liquidity**, does the
  contract verify repayment / that net settlement invariants hold?
  [elektrik-0-0]
- Are **fill/cancel paths resistant to front-running** and to **escrow
  reinitialization** with a reused order id/nonce? [1inch-0-0,
  pump-1-1, swc-114]
- Is **self-fill (maker == taker) blocked** where it would inflate volume
  or farm rewards? [1inch-1-3]
- Do **settlement pre/post hooks restrict callable targets/selectors** and
  validate the caller, so callbacks can't be spoofed into arbitrary
  external calls or dangling approvals? [bunni-v2-1-0-1]
- If an **off-chain signing/quoting API is the trust anchor**, is there
  defense-in-depth on-chain validation of amounts/limits should it fail?
  [mintify-1-1]
- Is the protocol's exposure to **solver liquidity concentration / a
  single solver's failure** bounded (fallback paths, liveness under
  Byzantine solvers)? [arxiv-2602.17805]
- Is order flow routed through **private/exclusive channels** that could
  centralize execution or let builders/proposers capture user value?
  [arxiv-2605.04471, moneyfornothing]
- Are the protocol's own **execution bots / privileged swap functions
  access-controlled** so anyone can't call them to manipulate swaps?
  [ripmevbot, ripmevbot2]
- Is a cancelled/invalidated order's **status read correctly** by
  integrating code (e.g., `invalidateOrder` setting `filledAmount` to
  MAX_UINT can look "filled")? [brahma-2-0]

## Prior incidents

- **0xbad / RIP MEV BOT (Sep 2022 — $1.5M)**: a backrun-arbitrage MEV
  bot was drained of 1,101 ETH because its execution contract function
  was not properly access-controlled. [cites: rekt-ripmevbot]
- **RIP MEV Bot 2 (Nov 2023 — $2M)**: an unprotected public swap
  function let an attacker manipulate Curve WETH/WBTC pools (funded by a
  $50M flash loan) and sandwich the bot. [cites: rekt-ripmevbot2]
- **Money for Nothing (Dec 2023 — $1.3M)**: an MEV bot backran a Uni V3
  whale's fat-finger and paid ~98% of the take as a bribe to the solo
  validator — order-flow value captured by the proposer.
  [cites: rekt-moneyfornothing]
- **Elektrik (Zokyo audit, 2024 — High)**: facilitators could borrow
  vault assets via the order engine with no on-chain repayment check.
  [cites: solodit-zokyo-2024-06-09-elektrik-0-0]
- **1inch Fusion (Hexens, 2025 — Critical/High)**: order fulfillment
  front-run combined with escrow PDA reinitialization let an attacker
  swap in a malicious order and steal from the taker.
  [cites: solodit-hexens-2025-02-21-1inch-0-0]
- **Brahma / CoW Protocol (Trust Security, 2023 — Low)**: a cancelled CoW
  order was mis-read as filled because `invalidateOrder` sets
  `filledAmount` to MAX_UINT; DCA approvals to the `vaultRelayer` also
  extend user trust to CoW infrastructure.
  [cites: solodit-trust-security-2023-05-15-brahma-2-0,
  solodit-trust-security-2023-05-15-brahma-2-3]

## References

- arxiv-2602.17805 — Exploiting Liquidity Exhaustion Attacks in
  Intent-Based Cross-Chain Bridges (solver liquidity concentration)
- arxiv-2603.04168 — OMNIINTENT: Trusted Intent-Centric Framework
  (intent-centric paradigm trade-offs)
- arxiv-2605.04471 — Order Flow Exclusivity and Value Extraction
  Mechanisms (EOF, non-atomic MEV, builder centralization)
- arxiv-2603.26290 — PEB Separation and State Migration (principal /
  executor / beneficiary decoupling)
- solodit-zokyo-2024-06-09-elektrik-0-0 — Facilitators can borrow assets
  and never repay
- solodit-trust-security-2023-05-15-brahma-2-3 — TRST-L-4 CoW-Swap risks
- solodit-trust-security-2023-05-15-brahma-2-0 — CoW Swap orders seen as
  filled although cancelled
- solodit-hexens-2025-02-21-1inch-0-0 — Order fulfillment front-run via
  escrow reinitialization
- solodit-hexens-2025-02-21-1inch-1-3 — Self-exchange (maker == taker)
- solodit-cyfrin-2026-03-04-cyfrin-ethcf-swapboard-v2-0-0-0 — No order
  expiration (free option)
- solodit-cyfrin-2026-03-04-cyfrin-ethcf-swapboard-v2-0-0-1 — No fill
  deadline (stale taker execution)
- solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-0-1 — FloodPlain selector
  extension / fulfiller-callback spoofing
- solodit-cyfrin-2026-04-07-cyfrin-myriad-pr145-v2-0-1-0 — Price-overlap
  surplus gifted to counterparty
- solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-3 — Missing ERC-1271
  support
- solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-0 — No maximum fee
  protection (operator settlement timing)
- solodit-zokyo-2023-12-11-limit-break-0-2 — Signature replayable across
  domains
- solodit-zokyo-2023-12-11-limit-break-1-0 — Applied fees bypassed
  (feeOnTop not signed)
- solodit-hexens-2025-14-03-mintify-1-1 — Theft if off-chain signing API
  fails
- solodit-pashov-audit-group-2023-11-01-pump-1-1 — Cancellation can be
  front-run
- rekt-ripmevbot — RIP MEV BOT / 0xbad ($1.5M)
- rekt-ripmevbot2 — RIP MEV Bot 2 ($2M)
- rekt-moneyfornothing — Money for Nothing ($1.3M, proposer capture)
- swc-114 — Transaction Order Dependence
