---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-2-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-09-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-25-cyfrin-button-basis-trade-v2-0
title: State drift between `BasisTradeVault.totalPendingWithdrawals` and `BasisTradeTailor.withdrawalRequests[pocket]`
vuln_class: []
---

# State drift between `BasisTradeVault.totalPendingWithdrawals` and `BasisTradeTailor.withdrawalRequests[pocket]`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-25-cyfrin-button-basis-trade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md)_

---

**Description:** `BasisTradeVault` tracks pending withdrawals in `totalPendingWithdrawals` while `BasisTradeTailor` keeps its own `withdrawalRequests[pocket]`. These two counters are mutated on different code paths:
* `BasisTradeVault::requestRedeem` bumps the Vault counter and sets the Tailor counter to a new total.
* `BasisTradeVault::processWithdrawal` only reduces the Vault counter.
* `BasisTradeTailor::processWithdrawal` only reduces the Tailor counter.

Although the Vault exposes `updateWithdrawalRequest(uint256 amount)`, it still uses a set-the-total model, which is race-prone and allows the two aggregates to drift with normal operations. Manual re-syncs with “set total” are brittle and can themselves overwrite correct values during concurrent requests.

Consider one of the following redesigns:
* Make the Vault the single source of truth and remove Tailor’s `withdrawalRequests` entirely. Tailor acts only as an executor to move funds; bots and operators read only `vault::totalPendingWithdrawals`.
* Switch from set total to delta-based accounting guarded by the Vault: Have `tailor::processWithdrawal` increase by a delta instead, and have the vault send the delta from `requestRedeem`.

**Button:** Fixed in [``](https://github.com/buttonxyz/button-protocol/commit/9cde24caa4b3f5f37a059bb2fde172cfa374d3a9). Updated to have only the offchain agent set the withdrawal request amount. Will need this to be able to do net settling between deposits and withdrawals.

**Cyfrin:** Verified. `totalPendingWithdrawals` removed in BasisTradeVault`.
