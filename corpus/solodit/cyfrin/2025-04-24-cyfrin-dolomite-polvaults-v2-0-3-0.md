---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-dolomite-polvaults-v2-0-3-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-dolomite-polvaults-v2-0
title: Redundant check for non-zero reward amount in `_handleRewards` function
vuln_class: []
---

# Redundant check for non-zero reward amount in `_handleRewards` function

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md)_

---

**Description:** In `InfraredBGTIsolationModeTokenVaultV1.sol`, the `_handleRewards` function includes a redundant check for positive reward amounts, as shown below:

```solidity
//InfraredBGTIsolationModeTokenVaultV1.sol
function _handleRewards(IInfraredVault.UserReward[] memory _rewards) internal {
    IIsolationModeVaultFactory factory = IIsolationModeVaultFactory(VAULT_FACTORY());
    for (uint256 i = 0; i < _rewards.length; ++i) {
        if (_rewards[i].amount > 0) {  // <-- This check is redundant
            if (_rewards[i].token == UNDERLYING_TOKEN()) {
                _setIsDepositSourceThisVault(true);
                factory.depositIntoDolomiteMargin(
                    DEFAULT_ACCOUNT_NUMBER,
                    _rewards[i].amount
                );
                assert(!isDepositSourceThisVault());
            } else {
                // ... rest of function
            }
        }
    }
}
```

This check is redundant because the getAllRewardsForUser function in the [InfraredVault](https://berascan.com/address/0x67b4e6721ad3a99b7ff3679caee971b07fd85cd1#code) only returns rewards with a positive amount:

```solidity
// InfraredVault.sol
function getAllRewardsForUser(address _user) external view returns (UserReward[] memory) {
    uint256 len = rewardTokens.length;
    UserReward[] memory tempRewards = new UserReward[](len);
    uint256 count = 0;
    for (uint256 i = 0; i < len; i++) {
        uint256 amount = earned(_user, rewardTokens[i]);
        if (amount > 0) {  // @audit <-- Already filtering for positive amounts
            tempRewards[count] = UserReward({token: rewardTokens[i], amount: amount});
            count++;
        }
    }
    // Create a new array with the exact size of non-zero rewards
    UserReward[] memory userRewards = new UserReward[](count);
    for (uint256 j = 0; j < count; j++) {
        userRewards[j] = tempRewards[j];
    }
    return userRewards;
}
```

**Recommended Mitigation:** Consider removing the redundant check.

**Dolomite:**
No longer applicable. Code changed a good bit because of bricked rewards fix

**Cyfrin**
Acknowledged.
