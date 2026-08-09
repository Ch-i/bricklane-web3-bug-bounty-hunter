---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-3-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`ArmadaTreasuryGov::removeStewardBudgetToken` deletes history, allowing rolling-window
  bypass via remove-then-add'
vuln_class: []
---

# `ArmadaTreasuryGov::removeStewardBudgetToken` deletes history, allowing rolling-window bypass via remove-then-add

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ArmadaTreasuryGov::removeStewardBudgetToken` calls `delete _stewardSpendHistory[token]`, clearing the rolling-window records in addition to clearing `stewardBudgets[token]`. A subsequent `addStewardBudgetToken` initializes an empty `StewardBudget` with no prior history. The steward can then spend the full per-window budget again even though prior spends within the window should still count. The aggregate `_outflowHistory` persists and caps absolute drain, so the true ceiling remains the outflow limit.

**Impact:** Per-cycle bypass of the steward-specific cap via a timelock remove/add pair. The outflow limit still bounds the total drain.

**Recommended Mitigation:** Preserve the history across remove/add cycles:

```solidity
function removeStewardBudgetToken(address token) external onlyOwner {
    delete stewardBudgets[token];
    // intentionally do NOT delete _stewardSpendHistory[token];
    emit StewardBudgetTokenRemoved(token);
}
```

**Armada:** Fixed in commit [447e6cb](https://github.com/ship-armada/armada-poc/commit/447e6cbb8833f92dffa517ea24423e9945f3ee4d).

**Cyfrin:** Verified.
