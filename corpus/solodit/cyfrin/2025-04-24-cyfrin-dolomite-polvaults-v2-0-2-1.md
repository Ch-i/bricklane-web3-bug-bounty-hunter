---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-dolomite-polvaults-v2-0-2-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-dolomite-polvaults-v2-0
title: Reward loss risk when transitioning between reward vault types
vuln_class: []
---

# Reward loss risk when transitioning between reward vault types

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md)_

---

**Description:** When a user's default reward vault type for an asset is changed (e.g., from NATIVE or BGTM to INFRARED) in the `InfraredBGTMetaVault` contract, current logic attempts to claim outstanding rewards before switching the type. However, the implementation fails to retrieve rewards from the user's current vault type, leading to permanent loss of accrued rewards.

The issue occurs in the relationship between `_setDefaultRewardVaultTypeByAsset` and `_getReward` functions:

- When staking tokens via `_stake`, the function calls `_setDefaultRewardVaultTypeByAsset` to ensure the asset uses the INFRARED reward type.
- If the asset's current reward type is not INFRARED, `_setDefaultRewardVaultTypeByAsset` calls `_getReward` to claim pending rewards for the asset before changing the type.
-  However, `_getReward` hardcodes the reward vault type to INFRARED instead of using the user's current reward type

```solidity
function _getReward(address _asset) internal {
    IBerachainRewardsRegistry.RewardVaultType rewardVaultType = IBerachainRewardsRegistry.RewardVaultType.INFRARED;
    IInfraredVault rewardVault = IInfraredVault(REGISTRY().rewardVault(
        _asset,
        rewardVaultType  // Always uses INFRARED, ignoring user's current type
    ));
    // ... claim rewards logic ...
}
```

This means that when transitioning from another reward type (e.g., NATIVE or BGTM) to INFRARED, the contract attempts to claim rewards from the INFRARED vault even though the user's rewards are accrued in a different vault type.

Additionally, the assertion that should prevent changing types when a user has a staked balance is ineffective for non-INFRARED types:

```solidity
assert(getStakedBalanceByAssetAndType(_asset, currentType) == 0);
```

This assertion will always pass for non-INFRARED types because `getStakedBalanceByAssetAndType` only can have non-zero balances for INFRARED due to the `onlyInfraredType` modifier on all staking functions.


**Impact:** While the protocol currently only intends to support the INFRARED reward type, this issue creates a potential risk for future expansion.

If/when the protocol adds support for additional reward types (NATIVE, BGTM) and users accrue rewards in these vaults, they would permanently lose these rewards when transitioning to the INFRARED type. Once the registry is updated to use INFRARED as the default reward type, the rewards in the original vault become inaccessible through normal contract interactions.

The severity of this issue depends on the protocol's roadmap for supporting multiple reward types. If there are definite plans to expand beyond INFRARED, this represents a significant risk of permanent reward loss for users.

**Proof of Concept:** Consider following scenario:
- In a future version, assume a user has accrued rewards in a NATIVE reward vault
- User calls a function that triggers `_setDefaultRewardVaultTypeByAsset` to transition to INFRARED
- The assertion `assert(getStakedBalanceByAssetAndType(_asset, currentType) == 0)` passes because balances in this contract are only tracked for INFRARED
- `_getReward(_asset)` is called but retrieves from INFRARED vault instead of NATIVE vault
- The registry is updated via `REGISTRY().setDefaultRewardVaultTypeFromMetaVaultByAsset(_asset, _type)`
- User's rewards in the NATIVE vault are now inaccessible

**Recommended Mitigation:** If the protocol plans to support multiple reward types in the future, modify the `_getReward` function to claim rewards from the user's current reward vault type.

Additionally, considering implementing proper balance tracking for all reward types if multiple types will be supported, or clearly document that transitioning between reward types requires manual reward claiming first.

If only INFRARED vault is supported, consider removing `_setDefaultRewardVaultTypeByAsset` as it is not serving any purpose. Since this is called in the `stake` function, removing this will simplify the code and save gas.

**Dolomite:**
Acknowledged. We know code will have to change a good bit to allow multiple reward types.

**Cyfrin**
Acknowledged.
