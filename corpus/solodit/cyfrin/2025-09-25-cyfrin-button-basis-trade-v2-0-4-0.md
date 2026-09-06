---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-4-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-09-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-25-cyfrin-button-basis-trade-v2-0
title: Redundant `approve(0)` in `BasisTradeVault::depositToTailor`
vuln_class: []
---

# Redundant `approve(0)` in `BasisTradeVault::depositToTailor`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-25-cyfrin-button-basis-trade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md)_

---

**Description:** `BasisTradeVault::depositToTailor` grants `tailor` an allowance, calls `tailor.deposit(pocket, amount)`, and then sets the allowance back to zero:

```solidity
IERC20(asset()).forceApprove(address(tailor), amount);
tailor.deposit(pocket, amount);
IERC20(asset()).forceApprove(address(tailor), 0); // redundant
```

`BasisTradeTailor::deposit` pulls exactly `amount` via `safeTransferFrom(msg.sender, pocket, amount)`, which consumes the entire allowance. With a standard ERC20, the post-call allowance is already `0`, so the trailing `forceApprove(..., 0)` performs an unnecessary storage write and external call.

Consider removing the final zeroing call.

**Button:** Fixed in commit [`9d8ed75`](https://github.com/buttonxyz/button-protocol/commit/9d8ed75bd5ed4957c7b23f9b06ff362b7bb218a4)

**Cyfrin:** Verified.

\clearpage
