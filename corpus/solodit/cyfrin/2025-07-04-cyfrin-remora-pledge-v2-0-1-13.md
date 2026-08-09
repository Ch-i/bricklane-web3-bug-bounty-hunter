---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-1-13
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Pledge can't successfully complete unless `RemoraToken` is paused
vuln_class: []
---

# Pledge can't successfully complete unless `RemoraToken` is paused

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** When the funding goal has been reached, `PledgeManager::checkPledgeStatus` calls `RemoraToken::unpause`:
```solidity
function checkPledgeStatus() public returns(bool pledgeNowConcluded) {
    if (pledgeRoundConcluded) return true;

    uint32 curTime = SafeCast.toUint32(block.timestamp);
    if (tokensSold >= fundingGoal) {
        pledgeRoundConcluded = true;
        IRemoraRWAToken(propertyToken).unpause();
        emit PledgeHasConcluded(curTime);
        return true;
```

But if `RemoraToken` is not paused, this [reverts](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/master/contracts/utils/PausableUpgradeable.sol#L128) since `PausableUpgradeable::_unpause` has the `whenPaused` modifier.

**Impact:** Pledge can't successfully complete unless `RemoraToken` is paused.

**Proof of Concept:**
```solidity
function test_pledge(uint256 userIndex, uint32 numTokensToBuy) external {
    address user = _getRandomUser(userIndex);
    numTokensToBuy = uint32(bound(numTokensToBuy, 1, DEFAULT_FUNDING_GOAL));

    // fund buyer with stablecoin
    (uint256 finalStablecoinAmount, uint256 fee)
        = pledgeManager.getCost(numTokensToBuy);
    stableCoin.transfer(user, finalStablecoinAmount);

    // fund this with remora tokens
    remoraTokenProxy.mint(address(this), numTokensToBuy);
    assertEq(remoraTokenProxy.balanceOf(address(this)), numTokensToBuy);

    // allow PledgeManager to spend our remora tokens
    remoraTokenProxy.approve(address(pledgeManager), numTokensToBuy);

    PledgeManagerState memory pre = _getState(address(this), user);

    remoraTokenProxy.pause();

    vm.startPrank(user);
    stableCoin.approve(address(pledgeManager), finalStablecoinAmount);
    pledgeManager.pledge(numTokensToBuy, bytes32(0x0), bytes(""));
    vm.stopPrank();

    PledgeManagerState memory post = _getState(address(this), user);

    // verify remora token balances
    assertEq(post.holderRemoraBal, pre.holderRemoraBal - numTokensToBuy);
    assertEq(post.buyerRemoraBal, pre.buyerRemoraBal + numTokensToBuy);

    // verify stablecoin balances
    assertEq(post.pledgeMgrStableBal, pre.pledgeMgrStableBal + finalStablecoinAmount);
    assertEq(post.buyerStableBal, pre.buyerStableBal - finalStablecoinAmount);

    // verify PledgeManager storage
    assertEq(post.pledgeMgrTokensSold, pre.pledgeMgrTokensSold + numTokensToBuy);
    assertEq(post.pledgeMgrTotalFee, pre.pledgeMgrTotalFee + fee);
    assertEq(post.pledgeMgrBuyerFee, pre.pledgeMgrBuyerFee + fee);
    assertEq(post.pledgeMgrTokensBought, pre.pledgeMgrTokensBought + numTokensToBuy);
}
```

**Recommended Mitigation:** The `RemoraToken` contract should remain in the `paused` state until the pledge completes, though this may not be convenient. Alternatively change `PledgeManager::checkPledgeStatus` to only unpause `RemoraToken` if it is paused.

**Remora:** Fixed in commit [dddde02](https://github.com/remora-projects/remora-smart-contracts/commit/dddde029b97f33bcb91d0353632a3aa5f028c684).

**Cyfrin:** Verified.
