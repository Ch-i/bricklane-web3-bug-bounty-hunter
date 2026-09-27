---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-25-tokentable-unlockerv2-evm-2-3
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-04-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md
tags:
- firm:codespect
- report:2025-04-25-tokentable-unlockerv2-evm
title: '[I-04] Tracker token’s balanceOf doesn’t account for cancelled actuals'
vuln_class: []
---

# [I-04] Tracker token’s balanceOf doesn’t account for cancelled actuals

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-25-TokenTable-UnlockerV2-EVM.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md)_

---

**Files:** [TTTrackerTokenV2.sol](https://github.com/EthSign/tokentable-v2-evm/tree/e27192f627ea849f88e8a4b68382c5ac8808e3a5/contracts/core/TTTrackerTokenV2.sol)

**Description:**

Tracker token is supposed to track an Unlcoker’s claimable project tokens. Specifically, the `balanceOf(...)` function should display the amount of currently claimable tokens of the given address.

```solidity
/**
 * @dev Number of currently claimable tokens of the given address.
 */
function balanceOf(address account) external view returns (uint256) {
    uint256 amountClaimable;
    ITTFutureTokenV2 nftInstance = ttuInstance.futureToken();
    uint256[] memory tokenIdsOfOwner = nftInstance.tokensOfOwner(account);
    for (uint256 i = 0; i < tokenIdsOfOwner.length; i++) {
        (uint256 deltaAmountClaimable,) = ttuInstance.calculateAmountClaimable(tokenIdsOfOwner[i]);
        amountClaimable += deltaAmountClaimable;
    }
    return amountClaimable;
}
```

However, this function doesn’t account for cancelled actuals. A cancelled actual may still have a claimable amount ready to be claimed which is stored in the `pendingAmountClaimableForCancelledActuals` mapping. The `balanceOf(...)` function only returns the claimable amount of active actuals.

**Impact:** The `balanceOf(...)` will return incorrect claimable amount for addresses that have cancelled actuals with claimable balance.

**Recommendation:** Also call the `pendingAmountClaimableForCancelledActuals(...)` function to retrieve this amount for cancelled actuals.

**Status:** Fixed

**Update from TokenTable:** [881e65e4ff8fa35daf4c6d2d04c6a1b2f65fd026](https://github.com/EthSign/tokentable-v2-evm/pull/11/commits/881e65e4ff8fa35daf4c6d2d04c6a1b2f65fd026)
