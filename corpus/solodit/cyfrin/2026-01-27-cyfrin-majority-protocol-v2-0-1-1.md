---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: '`DepositManager::getRewards` always includes `REFERRER_FEE` resulting in 2
  percent of every games'' rewards not being distributed to winners when there were
  no referrers'
vuln_class: []
---

# `DepositManager::getRewards` always includes `REFERRER_FEE` resulting in 2 percent of every games' rewards not being distributed to winners when there were no referrers

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** `DepositManager::getRewards` always includes `REFERRER_FEE` when calculating the percentage of `totalCollectedAmount` available to distribute to winners:
```solidity
function getRewards(uint256 gameId) public view returns (uint256) {
    return gamePools[gameId].totalCollectedAmount
        * (BASIS_POINTS - (gamePools[gameId].creatorFee + gamePools[gameId].protocolFee + REFERRER_FEE)) / BASIS_POINTS;
}
```

**Impact:** If no referral rewards were accrued for a game, this calculation results in the game rewards being less than they should since the `REFERRER_FEE` basis points are still used to deduct from the `totalCollectedAmount`.

The missing 2% of rewards are permanently stuck in the contract unable to be paid out to game winners or retrieved by the sponsor.

**Recommended Mitigation:** Rather than using `REFERRER_FEE`, change `DepositManager::_payEntryFee, _refundEntryFee` to increment/decrement the total amount of referral rewards in a new storage variable.

Then in `DepositManager::getRewards` deduct the total amount of referral rewards from `gamePools[gameId].totalCollectedAmount`.

**Majority Games:**
Fixed in commit [e090f2e](https://github.com/Engage-Protocol/engage-protocol/commit/e090f2e1b5f42eb212fdbda7be94ccf295281075) by introducing a `CLAIMER_ROLE` which can collect referral fees assigned to `address(0)`, such that referral fees are always collected. `Registry::setReferrer` has been modified to prevent an address having `CLAIMER_ROLE` from becoming a referrer since then they couldn't collect fees associated with their address.

**Cyfrin:** Verified. We note that `AccessControl::grantRole` has not been overridden such that a referrer could be granted `CLAIMER_ROLE` which would prevent them from claiming referrals associated with their address.
