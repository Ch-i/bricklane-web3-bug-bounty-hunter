---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-18-maitreja-staking-1-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-18-Maitreja-Staking.md
tags:
- firm:codespect
- report:2026-02-18-maitreja-staking
title: '[I-03] Withdrawals for web2 users may be delayed'
vuln_class: []
---

# [I-03] Withdrawals for web2 users may be delayed

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-18-Maitreja-Staking.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-18-Maitreja-Staking.md)_

---

**Files:** [ProgressiveStaking.sol](https://github.com/whaleden-mjtd/maitme-contracts-staking/blob/ce61102843ceb1c27d875b394490ff859577016c/src/ProgressiveStaking.sol#L253)

**Description:**

The document mentions that for web2 users in the system, tokens are managed in a single admin account. However, a single account can have at most 10 pending withdrawal requests within 90 days.

```solidity
function requestWithdraw(uint256 stakeId, uint256 amount) external nonReentrant whenNotPaused {
    //...
    if (pendingWithdrawCount[msg.sender] >= MAX_PENDING_WITHDRAWALS) revert TooManyPendingWithdrawals();
    //...
}
```

This makes it difficult for a single account to manage too many users, as their withdrawal requests may be delayed due to the admin account reaching the maximum number of pending requests.

**Impact:** Designing the system to manage all web2 users’ tokens in a single admin account may be unfeasible.

**Recommendation:** It is recommended to delegate web2 users in batches to multiple accounts or to implement a dedicated withdrawal function for this special case.

**Status:** Fixed
