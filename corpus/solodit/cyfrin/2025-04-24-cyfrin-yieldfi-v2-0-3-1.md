---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-3-1
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
title: Order not eligible at `eligibleAt`
vuln_class: []
---

# Order not eligible at `eligibleAt`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** Both in [`PerpetualBond::executeOrder`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/PerpetualBond.sol#L411) and [`Manager::executeOrder`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/Manager.sol#L208) there's a check that the order executed is still eligible:
```solidity
require(block.timestamp > order.eligibleAt, "!waitingPeriod");
```
`eligibleAt` indicates that the order should be eligible at this timestamp which is not what the check verifies. Consider changing `>` to `>=`:
```diff
- require(block.timestamp > order.eligibleAt, "!waitingPeriod");
+ require(block.timestamp >= order.eligibleAt, "!waitingPeriod");
```

**YieldFi:** Fixed in commit [`e9c160f`](https://github.com/YieldFiLabs/contracts/commit/e9c160fdfd6dd90650c9537fba73c17cb3c53ea5)

**Cyfrin:** Verified.
