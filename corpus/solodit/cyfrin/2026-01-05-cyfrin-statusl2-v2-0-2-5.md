---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: User can lose accrued rewards during migration
vuln_class: []
---

# User can lose accrued rewards during migration

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** User can migrate his staking position to new vault. However it will overwrite his `rewardsAccrued` in that new vault:
```solidity
    function migrateToVault(address migrateTo)
        external
        onlyNotEmergencyMode
        whenNotPaused
        onlyTrustedCodehash
        onlyRegisteredVault
    {
        if (vaultOwners[migrateTo] == address(0)) {
            revert StakeManager__InvalidVault();
        }

        if (vaultData[migrateTo].stakedBalance > 0) {
            revert StakeManager__MigrationTargetHasFunds();
        }

        _updateGlobalState();
        _updateVault(msg.sender, false);

        VaultData storage oldVault = vaultData[msg.sender];
        VaultData storage newVault = vaultData[migrateTo];

        // migrate vault data to new vault
        newVault.stakedBalance = oldVault.stakedBalance;
        newVault.rewardIndex = oldVault.rewardIndex;
        newVault.mpAccrued = oldVault.mpAccrued;
        newVault.maxMP = oldVault.maxMP;
        newVault.lastMPUpdateTime = oldVault.lastMPUpdateTime;
@>      newVault.rewardsAccrued = oldVault.rewardsAccrued;

        IStakeVault.MigrationData memory migrationData = IStakeVault.MigrationData({
            lockUntil: IStakeVault(msg.sender).lockUntil(),
            depositedBalance: IStakeVault(msg.sender).depositedBalance()
        });

        IStakeVault(migrateTo).migrateFromVault(migrationData);

        delete vaultData[msg.sender];

        emit VaultMigrated(msg.sender, migrateTo);
    }
```

Consider following example:
1) User has staking in old vault
2) New vault version is released
3) User creates stake in new vault
4) Unstakes from new vault
5) Migrates stake from old vault to the new one
6) User loses unclaimed rewards in that new vault, which were earned between steps 3 and 4.

**Impact:** User can lose accrued rewards during migration

**Recommended Mitigation:** Ensure user migrates to empty vault:
```diff
    function migrateToVault(address migrateTo)
        external
        onlyNotEmergencyMode
        whenNotPaused
        onlyTrustedCodehash
        onlyRegisteredVault
    {
        if (vaultOwners[migrateTo] == address(0)) {
            revert StakeManager__InvalidVault();
        }

-       if (vaultData[migrateTo].stakedBalance > 0) {
+       if (vaultData[migrateTo].stakedBalance > 0 || vaultData[migrateTo].rewardsAccrued > 0) {
            revert StakeManager__MigrationTargetHasFunds();
        }

        ...
    }
```

**StatusL2:** Fixed in [e038ece](https://github.com/status-im/status-network-monorepo/commit/e038ece7ff3df9936af0d8bdf920bbf31c0d8e80).

**Cyfrin:** Verified.
