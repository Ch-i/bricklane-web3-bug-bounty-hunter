---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: Malicious actors can get free rewards if contract gets paused
vuln_class: []
---

# Malicious actors can get free rewards if contract gets paused

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** The `StakeVault` contract has a leave functionality with a try/catch block:
```solidity
function leave(address _destination) external onlyOwner validDestination(_destination) {
    hasLeft = true;
    try stakeManager.leave() {
        if (lockUntil <= block.timestamp) {
            depositedBalance = 0;
            bool success = STAKING_TOKEN.transfer(_destination, STAKING_TOKEN.balanceOf(address(this)));
            if (!success) {
                revert StakeVault__FailedToLeave();
            }
        }
    } catch {
        if (lockUntil <= block.timestamp) {
            depositedBalance = 0;
            bool success = STAKING_TOKEN.transfer(_destination, STAKING_TOKEN.balanceOf(address(this)));
            if (!success) {
                revert StakeVault__FailedToLeave();
            }
        }
    }
}
```
It aims to handle bad staking managers that revert, causing a DoS. The issue is that if a legitimate revert can happen (or a forced one, by the caller), then the state in the staking manager will be inconsistent as it will still consider the caller staked, even though he actually withdrew his tokens. This will also allow him to get a part of the rewards even though he has not staked at all. The most obvious way where a revert can happen is if the contract is paused.

For example, the following can happen:
1. The staking manager will be paused for any reason, transaction is submitted.
2. Alice, a malicious actor, frontruns the pause and stakes a huge amount with a 0 lock time.
3. Step 1 transaction executes, contract is paused.
4. Alice immediately leaves after that, it reverts and we end up in the catch block where she simply gets her tokens back.
5. She gets rewards for free as she can keep calling `StakeManager::redeemRewards()`.

No way to force reverts has been found yet (e.g. 63/64 rule abuse is very unlikely to work, also no other reverts that can be forced to trigger).

**Impact:** Users can get free rewards at the expense of others.

**Recommended Mitigation:** Best way is to remove the try/catch and simply do not do bad upgrades.

**StatusL2:** Fixed in [d813449](https://github.com/status-im/status-network-monorepo/commit/d8134493d8cc9f86f36744cf308c3c8a18a09c7f).

**Cyfrin:** Verified.
