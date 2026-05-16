---
id: synthesis-reentrancy-variants-beyond-cei-read-only-cross-function-cross-contract-callback-hooks
source: synthesis
source_url: null
title: "Reentrancy variants beyond CEI: read-only, cross-function, cross-contract, callback hooks — pattern, variants, audit checklist"
ingested_at: 2026-05-16T00:00:00Z
vuln_class:
  - reentrancy
  - read-only-reentrancy
  - cross-function-reentrancy
  - cross-contract-reentrancy
  - cei-violation
  - external-call
  - callback-hook
protocol_category:
  - lending
  - amm
  - bridge
  - vault
  - nft
tags:
  - synthesis
  - reentrancy
  - erc777
  - erc721
  - read-only-reentrancy
  - cross-function
  - cross-contract
derives_from:
  - swc-107
  - solodit-cyfrin-2023-06-16-beanstalk-wells-0-3
  - solodit-hexens-2025-03-17-valantis-1-0
  - solodit-hexens-2022-11-04-1inch-0-0
  - solodit-hexens-2023-02-27-polygonzkevm-0-0
  - solodit-zokyo-2024-08-29-xyro-2-0
  - solodit-zokyo-2023-08-30-vaultka-2-1
  - solodit-zokyo-2024-02-26-tide-1-3
  - solodit-zokyo-2024-06-30-devve-0-0
  - solodit-zokyo-2024-06-26-starter-0-3
  - solodit-zokyo-2024-10-16-isle-finance-1-4
  - solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-3-0
  - solodit-zokyo-2023-12-22-creditswap-1-3
  - solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-3-2
  - solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-1-9
  - solodit-cyfrin-2023-09-06-woosh-deposit-vault-1-0
  - solodit-guardian-audits-2023-05-01-key-finance-1-3
  - solodit-auditone-2022-12-14-unicrow-0-2
  - solodit-auditone-2023-06-29-coinlend-0-3
  - solodit-zachobront-2023-06-01-dhedge-1-1
  - rekt-sturdy-rekt
  - rekt-eralend-rekt
  - rekt-conic-finance-rekt
  - rekt-midas-capital-rekt
  - rekt-dforce-network-rekt
  - rekt-curve-vyper-rekt
  - arxiv-2603.26497
  - arxiv-2601.06914
---

# Reentrancy variants beyond CEI

## Pattern

Classical reentrancy (SWC-107) is the recursive-call attack made famous
by the DAO: an external call hands execution to an untrusted contract
*before* the caller has finished updating its own state, and the
attacker re-enters the same function in a state where its preconditions
still look satisfied. The textbook fix is Checks-Effects-Interactions
(CEI), and OpenZeppelin's `ReentrancyGuard` (`nonReentrant`). [swc-107]

But the modern attack surface is much wider. Years of post-mortems show
the bug class has at least four practically distinct variants that all
defeat naive "I added `nonReentrant` to the entrypoint" reasoning:

1. **Read-only reentrancy** — a *view* function returns stale state
   *during* an external call, and downstream consumers (oracles, fee
   modules, virtual price formulas) act on the stale value. The
   re-entered call never writes — it only reads. The originating
   function may even be properly `nonReentrant`; the view it exposes is
   not, so the lock is invisible from outside. [solodit-cyfrin-2023-06-16-beanstalk-wells-0-3] [solodit-hexens-2025-03-17-valantis-1-0]

2. **Cross-function reentrancy** — `f()` makes an external call before
   updating state; the attacker re-enters via a *different* function
   `g()` that shares the same state but isn't behind the same lock
   (different modifier, different contract instance of
   `ReentrancyGuard`, or simply forgotten). [solodit-hexens-2022-11-04-1inch-0-0] [solodit-zokyo-2023-08-30-vaultka-2-1]

3. **Cross-contract reentrancy** — two contracts in the same protocol
   each import their own `ReentrancyGuard`; the locks live in
   independent storage, so locking `A.refund()` does not lock
   `B.singleClaim()` that reads/writes the same shared escrow. [solodit-auditone-2022-12-14-unicrow-0-2] [solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-1-9]

4. **Callback-hook reentrancy** — the external "call" is *implicit*: a
   token (ERC777, ERC1363, native ETH `call`), an NFT
   (`onERC721Received`, `onERC1155Received`), a router/strategy, a
   cross-chain messenger, or a custom hooklet hands execution to the
   recipient as a side effect of "just a transfer". Auditors miss it
   because the source code looks like an inert `safeTransfer`. [solodit-zokyo-2024-08-29-xyro-2-0] [solodit-hexens-2023-02-27-polygonzkevm-0-0] [solodit-guardian-audits-2023-05-01-key-finance-1-3]

These variants compose: a typical real-world incident chains an
ERC777/ERC721/native-ETH hook (variant 4) with a missing CEI ordering
(classic) to reach a stale view (variant 1) on a different contract
(variant 3). The 2022–2024 rekt.news leaderboard shows the variants
have caused well over $80M of recorded loss across Sturdy, EraLend,
Conic, Midas, dForce and Curve/Vyper. [rekt-sturdy-rekt] [rekt-eralend-rekt] [rekt-conic-finance-rekt] [rekt-midas-capital-rekt] [rekt-dforce-network-rekt] [rekt-curve-vyper-rekt]

Recent academic work confirms detection lags: handcrafted scenario
benchmarks show top static analyzers still miss many cross-function and
read-only patterns even when the canonical CEI case is detected. [arxiv-2603.26497] [arxiv-2601.06914]

## Variants

### V1: Read-only reentrancy (oracle/view stale state)

The classic pattern: an AMM or vault burns LP tokens / transfers tokens
*before* updating its internal reserves or virtual-price cache, and
exposes `getReserves()` / `get_virtual_price()` / `totalSupply()` as a
plain `view`. A re-enterer (via ERC777 hook, native ETH `call`, or
`onERC721Received`) calls back during the gap and queries the view; the
view returns the *pre-update* values. External consumers using that
view as an oracle (lending markets pricing collateral, fee modules
quoting swap fees) see manipulated prices.

This is the single most lucrative variant historically:

- Curve LP virtual-price reentrancy (Chainsecurity, April 2022) seeded
  a multi-year tail of exploits. [rekt-midas-capital-rekt]
- Midas Capital (WMATIC-stMATIC Curve LP) — `self.D` and `totalSupply`
  updated after a callback inside `remove_liquidity`. [rekt-midas-capital-rekt]
- dForce Network used `wstETHCRV-gauge` virtual price; the re-entrant
  read returned an inflated price; same contract pattern as Midas. [rekt-dforce-network-rekt]
- Sturdy Finance, Conic Finance, EraLend (SyncSwap LP) — same family.
  EraLend's source even had a comment "_Note reserves are not updated
  at this point to allow read the old values_" — "comments are not
  effective reentrancy protection." [rekt-sturdy-rekt] [rekt-conic-finance-rekt] [rekt-eralend-rekt]
- Beanstalk Wells `removeLiquidity` updated reserves after token
  transfers; mitigated by adding a guard-active check to
  `getReserves()` (not by locking it). [solodit-cyfrin-2023-06-16-beanstalk-wells-0-3]
- Valantis STEX AMM: the `withdraw` function was `nonReentrant`, but
  the intermediate state between burning token0 and withdrawing token1
  was observable via `getLiquidityQuote` (a `view`) inside the receive
  callback; the swap-fee module used the imbalanced ratio. [solodit-hexens-2025-03-17-valantis-1-0]
- Devve treasury: read-only reentrancy between
  `refundFromAdminInETH()` and `refund()` because state updates happen
  after `payable.transfer` and `refund()`'s `nonReentrant` only locks
  on entry to `refund()` itself. [solodit-zokyo-2024-06-30-devve-0-0]

Canonical defense (Beanstalk pattern): make read views revert if the
reentrancy guard is *active* — a `nonReadReentrant`-style modifier that
only checks the lock without setting it, applied to every view that
external integrators may use as an oracle. [solodit-cyfrin-2023-06-16-beanstalk-wells-0-3] [solodit-hexens-2025-03-17-valantis-1-0]

### V2: Cross-function reentrancy (shared state, unshared lock)

The attacker re-enters via a *sibling* function that touches the same
state but isn't behind the same lock — either because it was never
marked `nonReentrant`, or because the modifier sits on the wrong
function.

- 1inch ERC20Pods double-delegation: while `_beforeTokenTransfer` was
  iterating the `_pods` mapping for the `from` address, an attacker
  re-entered `addPod()` (a different public function) to mutate the
  pods array mid-loop; the second pass to the `to` branch then minted
  delegation again. Hexens explicitly recommends reentrancy locks for
  cross-function mitigation. [solodit-hexens-2022-11-04-1inch-0-0]
- Vaultka SakeVaultV2: `openPosition()` lacked `nonReentrant` but
  shared state with `closePosition`, `liquidatePosition`,
  `fulfilliedRequestSwap` — any unguarded entrypoint defeats the lock
  on its siblings. [solodit-zokyo-2023-08-30-vaultka-2-1]
- IPC `SubnetActorManagerFacet.unstake` is exposed to cross-function
  reentrancy at `LibStaking.withdrawWithConfirm`; the auditors note
  it's not immediately exploitable but the surface area exists. [solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-3-0]

A particularly painful subvariant: **reentrancy-guard conflict**. If
`_processVaultRewards` is itself `nonReentrant` and is also called from
an externally `nonReentrant` function, the inner call reverts on the
already-acquired lock, bricking the function entirely. Either lift
guards to externals only, or use a different guard instance. [solodit-zokyo-2024-06-26-starter-0-3]

### V3: Cross-contract reentrancy (different `ReentrancyGuard` storage)

Two contracts each `import "ReentrancyGuard.sol"` — each gets its own
`_status` slot in its own storage. Locking contract A does nothing to
contract B. If they share off-chain accounting (a mapping, an escrow,
a hooklet's view of pool state), an attacker can hop between them.

- Unicrow: `refund()` (in one contract) sends ETH to the buyer before
  setting `claimed=1`; the buyer re-enters `UnicrowClaim.singleClaim()`
  (in another contract). Both functions are `nonReentrant`, but the
  guards are in separate contracts so the state is unsynchronized;
  attacker drains the escrow. [solodit-auditone-2022-12-14-unicrow-0-2]
- Bunni v2: `BunniHubLogic.deposit` refunds excess ETH *before*
  calling `hookletAfterDeposit`; a malicious recipient can call
  `BunniToken.transfer` during the refund, triggering
  `hookletBeforeTransfer` / `hookletAfterTransfer` on the *same*
  hooklet before it has been notified of the deposit — corrupting the
  hooklet's accounting. The two contracts (Hub, BunniToken) have
  independent locks. [solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-1-9]
- CreditSwap CreditorNFT and CreditUSDMinter: auditors specifically
  recommend `ReentrancyGuard` "to avoid cross-function or
  cross-contract reentrancy exploits." [solodit-zokyo-2023-12-22-creditswap-1-3]

A more exotic instance: dHEDGE L1→L2 buyback. The Cross-Domain
Messenger can deliver queued L1 messages; if any reachable contract
hands control back to the user mid-`_buyBack`, the next queued L1
message triggers another `buyBackFromL1` before `claimedAmountOf` is
incremented. Only "ERC20 with no callback" assumption keeps it safe;
the auditors flag any future ERC777 or upgradeable token as making the
bug live. [solodit-zachobront-2023-06-01-dhedge-1-1]

### V4: Callback-hook reentrancy (ERC777, ERC721, native ETH, custom hooks)

The external call doesn't *look* external. A `safeTransfer`, a
`safeMint`, a `payable.transfer`/`call.value`, or a hooklet call yields
execution to attacker-controlled code.

- **ERC777 `tokensToSend` / `tokensReceived`**: the lesser-known
  `ERC777TokensSender` hook runs on the *from* side before
  `balanceOf(this)` reflects the transfer. In Polygon zkEVM bridge,
  attacker registers self as its own ERC777Sender via ERC1820, then
  re-enters `bridgeAsset()` recursively; each level locks in
  `balanceBefore=0` while the bottom call deposits 1 token; every level
  emits a deposit event for that amount, multiplying funds claimable on
  the destination chain by the reentrancy depth. [solodit-hexens-2023-02-27-polygonzkevm-0-0]
- ERC777 hooks on a "callback token" let a malicious admin re-enter
  `finalizeGame()` in Xyro Bullseye and drain the treasury when state
  is updated post-transfer. [solodit-zokyo-2024-08-29-xyro-2-0]
- Tide WaveContract `executeRuffle()` sends rewards to the winner;
  ERC777-style hooks let the winner re-enter and win again. [solodit-zokyo-2024-02-26-tide-1-3]
- Coinlend `buyCredits` calls `transferFrom` before `_mint`; ERC777
  payToken lets an attacker repeatedly call `buyCredits` in one tx. [solodit-auditone-2023-06-29-coinlend-0-3]
- Woosh Deposit Vault `deposit()` transfers ERC20 (potentially ERC777)
  *before* pushing to the `deposits` array — even without an immediate
  exploit, this enables read-only reentrancy on the `deposits` view. [solodit-cyfrin-2023-09-06-woosh-deposit-vault-1-0]
- **ERC721 `onERC721Received`**: Key Finance `unstakeAndWithdrawLpToken`
  hands execution to the LP NFT recipient mid-loop; tokens stay in
  `tokensStaked` while `idToOwner`/`stakedIndex` are cleared,
  desynchronizing on-chain bookkeeping. [solodit-guardian-audits-2023-05-01-key-finance-1-3]
- Isle Finance auditors flag every `ERC721.safeMint` /
  `safeTransferFrom` without `nonReentrant` as latent reentrancy
  surface. [solodit-zokyo-2024-10-16-isle-finance-1-4]
- **Transient-storage staged state (post-Cancun)**: Licredity's
  `exchangeFungible` clears the `stagedFungible` transient flag *after*
  `baseFungible.transfer(recipient, amountOut)`. A callback-capable
  token lets the recipient re-enter `depositFungible` while the staged
  flag is still set, recording a deposit without an actual transfer.
  Transient storage doesn't change the rules — CEI still applies. [solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-3-2]
- **Native ETH `call`** in fallback paths is the original hook —
  Devve's `payable.transfer` to user with state updated afterward is a
  textbook example of how `.transfer`/`.call` still grants execution
  even when the protocol assumed gas limits would prevent it. [solodit-zokyo-2024-06-30-devve-0-0]

### V5 (special case): compiler / language-level guard bypass

Even a correctly-applied `@nonreentrant('lock')` modifier can be
defeated below the source-language level. Curve/Vyper July 2023:
storage slots for the reentrancy lock in versions 0.2.15, 0.2.16, 0.3.0
were *misaligned* between `add_liquidity` and `remove_liquidity`, so
the guard wrote to slot X but the sibling function checked slot Y.
~$69M drained from CRV/ETH, alETH/ETH, msETH/ETH, pETH/ETH. The
takeaway: pin and audit the compiler version; treat the reentrancy
lock as a piece of code to be tested, not assumed. [rekt-curve-vyper-rekt]

## Audit checklist

State ordering and CEI

- Does every external call (including `safeTransfer`,
  `safeTransferFrom`, `safeMint`, native ETH send, `call`, router
  invocation, hooklet/strategy call) happen *after* every state update
  that the function or any sibling function or any external view
  consumer relies on? [swc-107] [solodit-cyfrin-2023-09-06-woosh-deposit-vault-1-0]
- Is staged / transient state (`tstore`, scratch mappings) cleared
  *before* any external call that might re-enter? [solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-3-2]
- For ETH refunds via `transfer`/`call` at the end of a function, do
  *all* downstream hooks (events, hooklet `after` callbacks, accrual
  updates) come *after* the refund — or has the refund been moved
  *after* them? [solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-1-9]

Reentrancy guards

- Is *every* state-mutating external function in the contract
  `nonReentrant`, not just the obvious ones? Sibling functions sharing
  state must share a lock. [solodit-zokyo-2023-08-30-vaultka-2-1] [solodit-hexens-2022-11-04-1inch-0-0]
- Do contracts that share state share a *single* `ReentrancyGuard`
  instance (e.g., via a shared base contract or storage slot), or do
  they each have independent `_status` slots that don't synchronize? [solodit-auditone-2022-12-14-unicrow-0-2]
- Are `nonReentrant` modifiers stacked on internal helpers that are
  also called from externally guarded entrypoints? (Guard conflict
  bricks the function.) [solodit-zokyo-2024-06-26-starter-0-3]
- Is the guard storage layout stable across the compiler versions in
  use? (Vyper 0.2.x/0.3.0 storage misalignment bug.) [rekt-curve-vyper-rekt]

Read-only / view exposure

- Does any external `view` expose intermediate state that integrators
  might use as a price/oracle/fee input? (`getReserves`,
  `get_virtual_price`, `totalSupply`, `tokenPrice`, `getLiquidityQuote`,
  `convertToAssets`, custom share-price getters.) [solodit-cyfrin-2023-06-16-beanstalk-wells-0-3] [solodit-hexens-2025-03-17-valantis-1-0]
- Do those views revert when the reentrancy guard is active (a
  `nonReadReentrant`-style modifier that checks but does not set
  `_status`)? [solodit-cyfrin-2023-06-16-beanstalk-wells-0-3] [solodit-hexens-2025-03-17-valantis-1-0]
- For Curve LP integrations specifically, do consumers call a
  `nonreentrant`-locked function (e.g., `remove_liquidity(0)`) *before*
  reading `get_virtual_price`, or do they use a known-mitigated
  workaround? [rekt-midas-capital-rekt] [rekt-dforce-network-rekt]

Callback-hook surface

- Could *any* token in scope ever be ERC777, ERC1363, fee-on-transfer
  with a hook, an upgradeable proxy that could add hooks, or a wrapped
  native (`WETH.withdraw` → ETH `call`)? If yes, treat every
  `safeTransfer` as an external call to attacker-controlled code. [solodit-zokyo-2024-02-26-tide-1-3] [solodit-zokyo-2024-08-29-xyro-2-0] [solodit-auditone-2023-06-29-coinlend-0-3]
- Does any function use `safeMint` or `safeTransferFrom` for ERC721 /
  ERC1155 (triggers `onERC*Received`)? Is it `nonReentrant`? [solodit-guardian-audits-2023-05-01-key-finance-1-3] [solodit-zokyo-2024-10-16-isle-finance-1-4]
- Does the contract integrate with cross-domain messengers, queued
  L1→L2 messages, or external hooklets/strategies that can be invoked
  during execution? [solodit-zachobront-2023-06-01-dhedge-1-1] [solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-1-9]
- For ERC777 specifically, can the attacker register themselves as
  their own `ERC777TokensSender` via ERC1820 to gain a callback on the
  `from` side of `transferFrom`? (The PolygonZkEVM bridge attack
  vector.) [solodit-hexens-2023-02-27-polygonzkevm-0-0]

Balance-delta accounting

- Does the contract compute amounts as `balanceAfter - balanceBefore`
  around a transfer, *and* update accounting per-call? Recursive
  reentrancy can make every level observe `balanceBefore=0` and emit
  the same deposit multiple times. [solodit-hexens-2023-02-27-polygonzkevm-0-0]

## Prior incidents

- **The DAO (2016)** — the canonical recursive-call drain that
  defined the bug class and CEI as the textbook fix. [cites: swc-107]
- **Market.xyz (Oct 2022) — $220k**: Curve LP read-only reentrancy
  precursor to the chain of 2023 incidents. [cites: rekt-midas-capital-rekt]
- **Midas Capital (Jan 2023) — $660k**: WMATIC-stMATIC Curve LP
  read-only reentrancy via `remove_liquidity` callback manipulating
  `virtual_price`. [cites: rekt-midas-capital-rekt]
- **dForce Network (Feb 2023) — $3.65M (returned)**: same Curve LP
  virtual-price reentrancy on Arbitrum + Optimism. [cites: rekt-dforce-network-rekt]
- **Sturdy Finance (Jun 2023) — $800k**: Balancer pool read-only
  reentrancy → `SturdyOracle` returns manipulated B-stETH-STABLE
  price. [cites: rekt-sturdy-rekt]
- **Conic Finance (Jul 2023) — $3.3M (1st attack)**: reentered
  `rETH-f.totalSupply()` via `CurveLPOracleV2`; built-in reentrancy
  protection failed due to ETH/WETH address mix-up. [cites: rekt-conic-finance-rekt]
- **EraLend (Jul 2023, zkSync Era) — $3.4M**: SyncSwap LP burn
  callback before `update_reserves`; oracle reads stale reserves.
  Source comment literally warned about the routine. [cites: rekt-eralend-rekt]
- **Curve/Vyper (Jul 2023) — $69M**: compiler-level storage-slot
  misalignment of `@nonreentrant('lock')` in Vyper 0.2.15/0.2.16/0.3.0
  let attacker re-enter between `add_liquidity` and `remove_liquidity`
  in CRV/ETH, alETH/ETH, msETH/ETH, pETH/ETH pools. [cites: rekt-curve-vyper-rekt]
- **dForce (2020) — $25M**: imBTC ERC777 hook reentrancy on
  `transferFrom`. (Earlier ERC777 incident referenced inside the 2023
  dForce post-mortem.) [cites: rekt-dforce-network-rekt]
- **Polygon zkEVM bridge (audit, 2023)**: ERC777 reentrancy on
  `bridgeAsset` would have amplified deposits by reentrancy depth via
  `balanceOf` delta accounting. Caught in audit. [cites: solodit-hexens-2023-02-27-polygonzkevm-0-0]
- **1inch ERC20Pods (audit, 2022)**: cross-function reentrancy from
  `_beforeTokenTransfer` into `addPod()` to double-mint delegation.
  Caught in audit. [cites: solodit-hexens-2022-11-04-1inch-0-0]

## References

Corpus entries cited (same as `derives_from`):

- `swc-107` — SWC-107: Reentrancy (canonical pattern, CEI, OZ guard).
- `solodit-cyfrin-2023-06-16-beanstalk-wells-0-3` — Beanstalk Wells
  read-only reentrancy; canonical `getReserves` guard-active fix.
- `solodit-hexens-2025-03-17-valantis-1-0` — Valantis STEX AMM:
  read-only via intermediate state inside `nonReentrant` withdraw.
- `solodit-hexens-2022-11-04-1inch-0-0` — 1inch ERC20Pods
  cross-function reentrancy double delegation.
- `solodit-hexens-2023-02-27-polygonzkevm-0-0` — PolygonZkEVM bridge
  ERC777 reentrancy with `balanceOf` delta amplification.
- `solodit-zokyo-2024-08-29-xyro-2-0` — Xyro Bullseye ERC777 callback
  drain on `finalizeGame`.
- `solodit-zokyo-2023-08-30-vaultka-2-1` — Vaultka cross-function
  reentrance between unguarded `openPosition` and siblings.
- `solodit-zokyo-2024-02-26-tide-1-3` — Tide `executeRuffle` ERC777
  hook.
- `solodit-zokyo-2024-06-30-devve-0-0` — Devve `refundFromAdminInETH`
  vs `refund` read-only reentrancy on ETH `.transfer`.
- `solodit-zokyo-2024-06-26-starter-0-3` — Reentrancy guard conflict on
  internal `_processVaultRewards`.
- `solodit-zokyo-2024-10-16-isle-finance-1-4` — Missing `nonReentrant`
  around ERC721 `safeMint`/`safeTransferFrom`.
- `solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-3-0` — IPC
  `unstake` cross-function reentrance exposure.
- `solodit-zokyo-2023-12-22-creditswap-1-3` — CreditSwap CreditorNFT
  cross-function/cross-contract reentrancy guidance.
- `solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-3-2` — Licredity
  transient `stagedFungible` cleared after external call.
- `solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-1-9` — Bunni v2
  cross-contract reentrancy between Hub deposit ETH refund and
  BunniToken transfer hooks.
- `solodit-cyfrin-2023-09-06-woosh-deposit-vault-1-0` — Woosh deposit
  not following CEI; ERC777 risk + read-only on `deposits`.
- `solodit-guardian-audits-2023-05-01-key-finance-1-3` — Key Finance
  `onERC721Received` reentrancy desyncing `tokensStaked`/`idToOwner`.
- `solodit-auditone-2022-12-14-unicrow-0-2` — Unicrow cross-contract
  reentrancy: independent `ReentrancyGuard` storage between
  Unicrow/UnicrowClaim.
- `solodit-auditone-2023-06-29-coinlend-0-3` — Coinlend ERC777
  `buyCredits` re-entrancy before `_mint`.
- `solodit-zachobront-2023-06-01-dhedge-1-1` — dHEDGE L1→L2 buyback:
  Cross-Domain Messenger queue + ERC777/upgradeable token risk.
- `rekt-sturdy-rekt` — Sturdy Finance $800k Balancer read-only.
- `rekt-eralend-rekt` — EraLend $3.4M SyncSwap LP callback.
- `rekt-conic-finance-rekt` — Conic $4.2M ($3.3M + $930k).
- `rekt-midas-capital-rekt` — Midas Capital $660k Curve LP.
- `rekt-dforce-network-rekt` — dForce $3.65M Curve LP across L2s.
- `rekt-curve-vyper-rekt` — Curve/Vyper $69M compiler-level guard
  storage misalignment.
- `arxiv-2603.26497` — Reentrancy Detection in the Age of LLMs
  (Solidity 0.8+ benchmark; static analyzers still miss cross-function
  and read-only scenarios).
- `arxiv-2601.06914` — Compositional Generalization for reentrancy
  detection; decomposes into external calls, state updates, data
  dependencies, flow order.
