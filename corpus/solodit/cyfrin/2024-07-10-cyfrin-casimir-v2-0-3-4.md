---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-3-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: '`getUserStake` function failure for non-staker accounts'
vuln_class: []
---

# `getUserStake` function failure for non-staker accounts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** The function `getUserStake` in the smart contract throws an error when invoked for an address that does not have any stakes. Specifically, the function fails due to a division by zero error. This occurs because the divisor, `users[userAddress].rewardStakeRatioSum0`, can be zero if `userAddress` has never staked, leading to an unhandled exception in the `Math.mulDiv` operation.

````solidity
function getUserStake(address userAddress) public view returns (uint256 userStake) {
    userStake = Math.mulDiv(users[userAddress].stake0, rewardStakeRatioSum, users[userAddress].rewardStakeRatioSum0);
}
````

**Recommended Mitigation:** Consider modifying the `getUserStake` function to include a check for a zero divisor before performing the division. If `users[userAddress].rewardStakeRatioSum0` is zero, the function should return a stake of 0 to avoid the division by zero error.

**Casimir:**
Fixed in [27c09f5](https://github.com/casimirlabs/casimir-contracts/commit/27c09f548d6d73222a087f2ef237335353cdfefa)

**Cyfrin:** Verified.

\clearpage
