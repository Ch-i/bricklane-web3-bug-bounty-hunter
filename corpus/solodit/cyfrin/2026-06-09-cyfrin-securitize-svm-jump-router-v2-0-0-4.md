---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-0-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-09-cyfrin-securitize-svm-jump-router-v2-0
title: Swap price events are denormalized using asset decimals instead of liquidity
  decimals
vuln_class: []
---

# Swap price events are denormalized using asset decimals instead of liquidity decimals

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** `calculate_jump_price` returns a WAD-scaled liquidity-per-asset price. In other words, it represents how many liquidity tokens are paid or received per one asset token.

However, when emitting swap events, the code denormalizes both `nbbo_price`, `jump_price`, and event rate using `asset_mint.decimals` instead of `liquidity_mint.decimals`.

```rust
utils::swap_utils::denormalize_price_to_decimals(
    &jump_price,
    swap_accounts.asset_mint.decimals,
)?;
```
Since the price is denominated in liquidity tokens, it should be scaled to the liquidity token’s decimals.

**Impact:** On-chain swap execution and token settlement are not directly affected, but emitted accounting data can be incorrect.

Indexers or downstream integrations relying on `PstRamp.nbbo_price`, `PstRamp.jump_price`, `Swap.rate`, or `RedemptionCompleted.rate` may record materially incorrect prices.

**Recommended Mitigation:** Denormalize liquidity-per-asset prices using `liquidity_mint.decimals` instead of `asset_mint.decimals`:
```rust
let denormalized_nbbo_price = if let Some(nbbo_price) = nbbo_price_opt {
    utils::swap_utils::denormalize_price_to_decimals(
        nbbo_price,
        swap_accounts.liquidity_mint.decimals,
    )?
} else {
    0
};

let denormalized_jump_price = utils::swap_utils::denormalize_price_to_decimals(
    &jump_price,
    swap_accounts.liquidity_mint.decimals,
)?;
```
**Securitize:** Acknowledged; The indexer expects the price is scaled in asset decimals. It's also compatible with the on and off ramp programs.


\clearpage
