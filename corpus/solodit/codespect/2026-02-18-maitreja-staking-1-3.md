---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-18-maitreja-staking-1-3
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-02-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-18-Maitreja-Staking.md
tags:
- firm:codespect
- report:2026-02-18-maitreja-staking
title: '[I-04] Withdrawal requests that are canceled or executed cannot be distinguished'
vuln_class: []
---

# [I-04] Withdrawal requests that are canceled or executed cannot be distinguished

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-18-Maitreja-Staking.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-18-Maitreja-Staking.md)_

---

**Original severity:** Best Practices

**Files:** [ProgressiveStaking.sol](https://github.com/whaleden-mjtd/maitme-contracts-staking/blob/ce61102843ceb1c27d875b394490ff859577016c/src/ProgressiveStaking.sol#L330)

**Description:**

Calling the `executeWithdraw(...)` function to process a withdrawal request sets the `executed` field to `true`.

```solidity
function executeWithdraw(uint256 stakeId) external nonReentrant {
    //...
    request.executed = true;
    //...
}
```

Calling the `cancelWithdrawRequest(...)` function to cancel a withdrawal request also sets the `executed` field to `true`.

```solidity
function cancelWithdrawRequest(uint256 stakeId) external nonReentrant {
    //...
    request.executed = true; // Mark as executed to prevent reuse
    //...
}
```

There is no other field to distinguish canceled and executed withdrawal requests in the history.

**Impact:** The historical withdrawal records returned by the `getPendingWithdrawals(...)` function cannot distinguish between canceled and executed requests.

**Recommendation:** It is recommended to add a field to distinguish between canceled and executed withdrawal requests.

**Status:** Fixed
