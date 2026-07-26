---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2-0-0-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-06-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2-0
title: Missing `poolStatus` check in `bypassQueue`
vuln_class: []
---

# Missing `poolStatus` check in `bypassQueue`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md)_

---

**Description:** The `bypassQueue` function in `PriorityPool.sol` doesn't check the pool's status before depositing tokens directly into the staking pool.
```solidity
function bypassQueue(
    address _account,
    uint256 _amount,
    bytes[] calldata _data
) external onlyQueueBypassController {
    token.safeTransferFrom(msg.sender, address(this), _amount);

    uint256 canDeposit = stakingPool.canDeposit();
    if (canDeposit < _amount) revert InsufficientDepositRoom();

    stakingPool.deposit(_account, _amount, _data);
}
```
The pool status check is part of the protocol's emergency response system. The [RebaseController](https://github.com/stakedotlink/contracts/blob/4b6b0811835bafa4c8379a39512bfe99bc6c6ebf/contracts/contracts/core/RebaseController.sol#L120-L140) can set the pool status to `CLOSED` during emergency situations, such as when the strategy is leading to a loss of funds. This reason can be seen on `RebaseController` when reopening the pool:
```solidity
@>     * @notice Reopens the priority pool and security pool after they were paused as a result
@>     * of a loss and updates strategy rewards in the staking pool
     * @param _data encoded data to pass to strategies
     */
    function reopenPool(bytes calldata _data) external onlyOwner {
        if (priorityPool.poolStatus() == IPriorityPool.PoolStatus.OPEN) revert PoolOpen();


        priorityPool.setPoolStatus(IPriorityPool.PoolStatus.OPEN);
        if (address(securityPool) != address(0) && securityPool.claimInProgress()) {
            securityPool.resolveClaim();
        }
        _updateRewards(_data);
    }
```
This missing check in the `bypassQueue` function allows user funds to be deposited when the pool is `CLOSED`, potentially causing deposited tokens to be lost during protocol emergency shutdowns.

**Impact:** LINK tokens can be deposited via `LINKMigrator` even when the `PriorityPool` is `CLOSED` or `DRAINING`, effectively bypassing the emergency pause mechanism intended for use during security incidents. This could potentially result in users losing funds. However, this risk is considered low in the context of the Chainlink community pool, as there is no inherent mechanism for loss, slashing only occurs in the operator pool. As such, the scenario would only pose a threat if one of the involved contracts were compromised and a user still migrates to it.

**Recommended Mitigation:** Add a pool status check in the bypassQueue function:
```diff
function bypassQueue(
    address _account,
    uint256 _amount,
    bytes[] calldata _data
) external onlyQueueBypassController {
+    if (poolStatus != PoolStatus.OPEN) revert DepositsDisabled();
    ...
}
```

**stake.link:**
Fixed in [`c595886`](https://github.com/stakedotlink/contracts/commit/c595886faef706a74bc11815b103af6670d7ed4d)

**Cyfrin:** Verified. The recommended mitigation was implemented.
