---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-3-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: The period check in `getNextUnstake()` always returns true
vuln_class: []
---

# The period check in `getNextUnstake()` always returns true

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** The function `getNextUnstake()` is used to get the next unstake request in the queue, while also verifying if the request can be fulfilled. One of the condition to make the request fulfillable is `unstake.period <= reportPeriod`.

```solidity
function getNextUnstake() public view returns (Unstake memory unstake, bool fulfillable) {
    if (unstakeQueue.length > 0) {
        unstake = unstakeQueue[0];
        fulfillable = unstake.period <= reportPeriod && unstake.amount <= getWithdrawableBalance();
    }
}
```

However, given the current codebase, the `unstake.period` will always less or equal to `reportPeriod`. This is because the ``unstake.period` will be assigned with `reportPeriod` when the unstake request is created/queued but the value of `reportPeriod` is intended to be only increasing overtime.

```solidity
unstakeQueue.push(Unstake({userAddress: msg.sender, amount: amount, period: reportPeriod}));
...
reportPeriod++;
```

**Impact:** The check `unstake.period <= reportPeriod` has no effect since it always returns true.

**Recommended Mitigation:** Consider reviewing the logic in function `getNextUnstake()` and removing the period check if it is unnecessary.

**Casimir:**
Mitigated in [28baa81](https://github.com/casimirlabs/casimir-contracts/commit/28baa8191a1b5a27d3ee495dee0d993177bf7e5f).

**Cyfrin:** Verified.
