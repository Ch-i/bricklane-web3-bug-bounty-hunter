---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-1-0
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
title: Malicious actors can force vaults to exit if they wish to get rewards
vuln_class: []
---

# Malicious actors can force vaults to exit if they wish to get rewards

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** Rewards are redeemed by iterating over all vaults of an account and calculating the accrued rewards:
```solidity
function redeemRewards(address account) external onlyNotEmergencyMode whenNotPaused returns (uint256) {
    // ...
    for (uint256 i = 0; i < accountVaults.length; i++) {
        // ...
    }
    // ...
}
```

There is no way to receive rewards by specifying a singular vault unless you exit the system completely.

The vaults are pushed upon registration in `StakeManager::registerVault`:
```solidity
function registerVault() external onlyNotEmergencyMode whenNotPaused onlyTrustedCodehash {
    address vault = msg.sender;
    address owner = IStakeVault(vault).owner();

    if (vaultOwners[vault] != address(0)) {
        revert StakeManager__VaultAlreadyRegistered();
    }

    vaultOwners[vault] = owner;
    vaults[owner].push(vault);
    emit VaultRegistered(vault, owner);
}
```

The issue is that anyone can deploy their own vaults (bypassing the factory) using the correct vault implementation address to satisfy `onlyTrustedCodehash` modifier. They can specify any specific owner they are targeting. This will cause the `vaults[victim]` array to be extended and with enough entries, iterating over it will be impossible due to gas limits. Thus, there is no way to redeem rewards unless a legitimate vault exits the system. The fact that some users might have staked for 4 years also makes the issue more serious as they will be forced to wait for the whole period to get any rewards.

The issue also makes functions like `updateAccount` and some other view functions unusable.

**Impact:** Unable to redeem rewards unless you exit out of the system completely.

**Recommended Mitigation:** Consider adding access control that only allows factory to register vaults.

**StatusL2:** Fixed in [5e93ecb](https://github.com/status-im/status-network-monorepo/commit/5e93ecbf02b2038d88cdafcd9eb99ed32872e38e).

**Cyfrin:** Verified.
