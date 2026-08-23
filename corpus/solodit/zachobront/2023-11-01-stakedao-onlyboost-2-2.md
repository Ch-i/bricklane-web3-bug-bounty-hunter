---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-11-01-stakedao-onlyboost-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-StakeDAO-Onlyboost.md
tags:
- firm:zachobront
- report:2023-11-01-stakedao-onlyboost
title: '[L-03] `setGauge()` and `setRewardDistributor()` should revoke old approvals'
vuln_class: []
---

# [L-03] `setGauge()` and `setRewardDistributor()` should revoke old approvals

_Section severity (from Solodit section header): Low_  
_Audit firm: ZachObront_  
_Source report: [2023-11-01-StakeDAO-Onlyboost.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-StakeDAO-Onlyboost.md)_

---

When `setGauge()` or `setRewardDistributor()` is called, we set the local mappings, and then approve the corresponding token for transfers.

In `setGauge()`, we approve the Curve gauge to spend the LP token from the locker:
```solidity
function setGauge(address token, address gauge) external onlyGovernanceOrFactory {
    if (token == address(0)) revert ADDRESS_NULL();
    if (gauge == address(0)) revert ADDRESS_NULL();

    gauges[token] = gauge;

    /// Approve trough the locker.
    locker.safeExecute(token, 0, abi.encodeWithSignature("approve(address,uint256)", gauge, 0));
    locker.safeExecute(token, 0, abi.encodeWithSignature("approve(address,uint256)", gauge, type(uint256).max));
}
```
In `setRewardDistributor()`, we approve the reward distributor to spend CRV:
```solidity
function setRewardDistributor(address gauge, address rewardDistributor) external onlyGovernanceOrFactory {
    if (gauge == address(0) || rewardDistributor == address(0)) revert ADDRESS_NULL();
    rewardDistributors[gauge] = rewardDistributor;

    /// Approve the rewardDistributor to spend token.
    SafeTransferLib.safeApproveWithRetry(rewardToken, rewardDistributor, type(uint256).max);
}
```
It would be safer to explicitly revoke old approvals to ensure that there are no lingering approvals to old gauges.

**Recommendation**

```diff
function setGauge(address token, address gauge) external onlyGovernanceOrFactory {
    if (token == address(0)) revert ADDRESS_NULL();
    if (gauge == address(0)) revert ADDRESS_NULL();

+   address oldGauge = gauges[token];
+   if (oldGauge != address(0)) {
+     locker.safeExecute(token, 0, abi.encodeWithSignature("approve(address,uint256)", oldGauge, 0));
+   }

    gauges[token] = gauge;

    /// Approve trough the locker.
    locker.safeExecute(token, 0, abi.encodeWithSignature("approve(address,uint256)", gauge, 0));
    locker.safeExecute(token, 0, abi.encodeWithSignature("approve(address,uint256)", gauge, type(uint256).max));
}
```
```diff
function setRewardDistributor(address gauge, address rewardDistributor) external onlyGovernanceOrFactory {
    if (gauge == address(0) || rewardDistributor == address(0)) revert ADDRESS_NULL();

+   address oldRewardDistributor = rewardDistributors[gauge];
+   if (oldRewardDistributor != address(0)) {
+     SafeTransferLib.safeApprove(rewardToken, rewardDistributor, 0);
+   }

    rewardDistributors[gauge] = rewardDistributor;

    /// Approve the rewardDistributor to spend token.
    SafeTransferLib.safeApproveWithRetry(rewardToken, rewardDistributor, type(uint256).max);
}
```

**Review**

Fixed as recommended in commit [bfea1a1247100b11ce1b1455eba178a706d64b96](https://github.com/stake-dao/only-boost/commit/bfea1a1247100b11ce1b1455eba178a706d64b96).
