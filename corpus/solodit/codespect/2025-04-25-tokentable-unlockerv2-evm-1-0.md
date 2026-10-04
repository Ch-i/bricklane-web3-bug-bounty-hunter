---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-25-tokentable-unlockerv2-evm-1-0
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
title: '[L-01] Tracker token’s balanceOf will revert if address owns cancelled actuals'
vuln_class: []
---

# [L-01] Tracker token’s balanceOf will revert if address owns cancelled actuals

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-25-TokenTable-UnlockerV2-EVM.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md)_

---

**Files:** [TTTrackerTokenV2](https://github.com/EthSign/tokentable-v2-evm/tree/e27192f627ea849f88e8a4b68382c5ac8808e3a5/contracts/core/TTTrackerTokenV2.sol)

**Description:**

Tracker token is supposed to track an Unlcoker’s claimable project tokens. Specifically, the `balanceOf(...)` function should display the amount of currently claimable tokens of the given address. However, the call will always revert if the address owns a cancelled actual. This happens because the `cancel(...)` function deletes the `actuals[]` mapping of the actual.

```solidity
function cancel(
    uint256[] calldata actualIds,
    bool[] calldata shouldWipeClaimableBalance,
    uint256 batchId,
    bytes calldata
) external virtual override onlyOwner returns (uint256[] memory pendingAmountClaimables) {
    ..
    delete $.actuals[actualId];
}
_callHook(_msgData());
}
```

This mapping is later used by the `calculateAmountClaimable(...)` function which Tracker Token’s `balanceOf(...)` function calls.

```solidity
function calculateAmountClaimable(uint256 actualId)
    public
    view
    virtual
    override
    returns (uint256 deltaAmountClaimable, uint256 updatedAmountClaimed)
{
    (deltaAmountClaimable, updatedAmountClaimed) = simulateAmountClaimable(actualId, block.timestamp);
}

function simulateAmountClaimable(uint256 actualId, uint256 claimTimestampAbsolute)
    public
    view
    virtual
    override
    returns (uint256 deltaAmountClaimable, uint256 updatedAmountClaimed)
{
    TokenTableUnlockerV2Storage storage $ = _getTokenTableUnlockerV2Storage();
    Actual memory actual = $.actuals[actualId];
    if (actual.presetId == 0) revert ActualDoesNotExist();
    ..
}
```

**Impact:** If a user owns a cancelled actual, calling `balanceOf(...)` on that address will always revert.

**Recommendation:** Consider making the `simulateAmountClaimable(...)` function return 0 if the actual doesn’t exist instead of reverting.

**Status:** Fixed

**Update from TokenTable:** [4652bc40f9300ebd99a5fc2c26ff20a8cc94fb69](https://github.com/EthSign/tokentable-v2-evm/pull/11/commits/4652bc40f9300ebd99a5fc2c26ff20a8cc94fb69)
