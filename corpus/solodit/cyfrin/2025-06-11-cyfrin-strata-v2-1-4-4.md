---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-4-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: '`PreDepositVault` checks should fail early'
vuln_class: []
---

# `PreDepositVault` checks should fail early

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** `PreDepositVault` implements after deposit/withdrawal checks to enforce several invariants; however, it is only necessary to check the minimum shares violation after execution of the calling functions. To consume less gas, it is better to split these checks into separate before/after functions and revert early if either deposits or withdrawals are disabled.

```solidity
function onAfterDepositChecks () internal view {
    if (!depositsEnabled) {
        revert DepositsDisabled();
    }
}
function onAfterWithdrawalChecks () internal view {
    if (!withdrawalsEnabled) {
        revert WithdrawalsDisabled();
    }
    if (totalSupply() < MIN_SHARES) {
        revert MinSharesViolation();
    }
}
```

**Strata:** Acknowledged, as the pause state is considered an edge case, so in normal use users would instead benefit from a single method call for all the required checks.

**Cyfrin:** Acknowledged.
