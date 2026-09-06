---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-3-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: '`PerpetualBond.epoch` not updated after yield distribution'
vuln_class: []
---

# `PerpetualBond.epoch` not updated after yield distribution

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** In [`PerpetualBond::distributeBondYield`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/PerpetualBond.sol#L215-L241) the caller is supposed to provide a `nonce` that matches [`epoch + 1`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/PerpetualBond.sol#L220-L221):
```solidity
function distributeBondYield(uint256 _yieldAmount, uint256 nonce) external notPaused onlyRewarder {
    require(nonce == epoch + 1, "!epoch");
```
However, `epoch` is never incremented afterwards, consider incrementing `epoch`.

**YieldFi:** Fixed in commit [`5c1f0e7`](https://github.com/YieldFiLabs/contracts/commit/5c1f0e7a805caf1d0fddbc5a15c8b6797a424467)

**Cyfrin:** Verified. `epoch` now is incremented with the new `nonce`.
