---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-25-tokentable-unlockerv2-evm-1-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md
tags:
- firm:codespect
- report:2025-04-25-tokentable-unlockerv2-evm
title: '[L-02] Tracker token’s totalSupply is always incorrect'
vuln_class: []
---

# [L-02] Tracker token’s totalSupply is always incorrect

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-25-TokenTable-UnlockerV2-EVM.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md)_

---

**Files:** [TTTrackerTokenV2](https://github.com/EthSign/tokentable-v2-evm/tree/e27192f627ea849f88e8a4b68382c5ac8808e3a5/contracts/core/TTTrackerTokenV2.sol)

**Description:**

Tracker token is supposed to track an Unlcoker’s claimable project tokens. Specifically, the `totalSupply()` function should track the total number of tokens deposited into the Unlocker awaiting claim.

```solidity
/**
 * @dev Total number of tokens deposited into the unlocker awaiting claim.
 */
function totalSupply() external view returns (uint256) {
    return IERC20Metadata(ttuInstance.getProjectToken()).balanceOf(address(this));
}
```

However, the function is returning the `balanceOf(address(this))`, instead of the balance of the `Unlocker` which holds the project tokens.

**Impact:** Tracker token will return the wrong number of tokens that are deposited in the `Unlocker` as it is tracking the wrong address’ balance.

**Recommendation:** Make the function return the `balanceOf(address(ttuInstance))`.

**Status:** Fixed

**Update from TokenTable:** [0bff495890939f24db93a77b5c03979419b0f2ad](https://github.com/EthSign/tokentable-v2-evm/pull/11/commits/0bff495890939f24db93a77b5c03979419b0f2ad)
