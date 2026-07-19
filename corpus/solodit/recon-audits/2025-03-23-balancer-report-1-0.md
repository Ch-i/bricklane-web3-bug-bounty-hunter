---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-balancer-report-1-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Balancer_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-balancer-report
title: '[G-01] Gas Optimization: Can skip check to save 200 gas'
vuln_class: []
---

# [G-01] Gas Optimization: Can skip check to save 200 gas

_Section severity (from Solodit section header): Gas_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Balancer_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Balancer_Report.md)_

---

**Impact**

`performUpkeep` has a check to verify if there's any re-lockable balance

https://github.com/onchainification/aura_locker_v2/blob/07294ae3638909ecd768a6a0f831fa513abe91a0/src/AuraLockerModule.sol#L112-L113

```solidity
    /// @notice The actual execution of the action determined by the `checkUpkeep` method (AURA locking)
    function performUpkeep(bytes calldata /* _performData */ ) external override onlyKeeper {
        if (!_isModuleEnabled()) revert ModuleNotEnabled();

        (, uint256 unlockable,,) = AURA_LOCKER.lockedBalances(address(SAFE));
        if (unlockable == 0) revert NothingToLock(block.timestamp);
```

If the check fails, the call will revert.

However, vlAURA already has this check

https://etherscan.io/address/0x3Fa73f1E5d8A792C80F426fc8F84FBF7Ce9bBCAC#code
```solidity
    function _processExpiredLocks(
        address _account,
        bool _relock,
        address _rewardAddress,
        uint256 _checkDelay
    ) internal updateReward(_account) {
/// OMITTED

require(length > 0, "no locks"); /// @audit Reverts here
```

Meaning you can skip the call to save around 200 gas

**Mitigation**

Consider removing the check to save 200 gas

----
