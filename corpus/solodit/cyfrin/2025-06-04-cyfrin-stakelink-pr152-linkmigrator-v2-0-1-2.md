---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2-0-1-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-06-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2-0
title: Consider renaming `LINKMigrator::_isUnbonded` for clarity
vuln_class: []
---

# Consider renaming `LINKMigrator::_isUnbonded` for clarity

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md)_

---

**Description:** In the `LINKMigrator` contract, the function [`_isUnbonded`](https://github.com/stakedotlink/contracts/blob/0bd5e1eecd866b2077d6887e922c4c5940a6b452/contracts/linkStaking/LINKMigrator.sol#L132-L137) checks whether a user is currently within the claim period for Chainlink staking:

```solidity
function _isUnbonded(address _account) private view returns (bool) {
    uint256 unbondingPeriodEndsAt = communityPool.getUnbondingEndsAt(_account);
    if (unbondingPeriodEndsAt == 0 || block.timestamp < unbondingPeriodEndsAt) return false;

    return block.timestamp <= communityPool.getClaimPeriodEndsAt(_account);
}
```

While functionally correct, the name `_isUnbonded` may not clearly convey its purpose, as it specifically checks whether a user is in the claim period. For improved clarity and consistency with Chainlink’s naming convention—such as in [`StakingPoolBase::_inClaimPeriod`](https://etherscan.io/address/0xbc10f2e862ed4502144c7d632a3459f49dfcdb5e#code)—renaming it could make the intent more immediately clear:

```solidity
function _inClaimPeriod(Staker storage staker) private view returns (bool) {
  if (staker.unbondingPeriodEndsAt == 0 || block.timestamp < staker.unbondingPeriodEndsAt) {
    return false;
  }

  return block.timestamp <= staker.claimPeriodEndsAt;
}
```

**Recommended Mitigation:** Consider renaming `_isUnbonded` to `_inClaimPeriod` to better reflect its logic and improve code readability.

**stake.link:**
Fixed in [`9d710bf`](https://github.com/stakedotlink/contracts/commit/9d710bf35304e9b45ed1ad8468714915817904a1)

**Cyfrin:** Verified.

\clearpage
