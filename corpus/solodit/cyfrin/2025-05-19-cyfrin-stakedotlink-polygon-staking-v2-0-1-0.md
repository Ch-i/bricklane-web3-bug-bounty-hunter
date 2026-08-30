---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-05-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0
title: '`PolygonStrategy::upgradeVaults` does not verify if vaults to upgrade are
  the same as the ones stored in strategy'
vuln_class: []
---

# `PolygonStrategy::upgradeVaults` does not verify if vaults to upgrade are the same as the ones stored in strategy

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md)_

---

**Description:** `PolygonStrategy::upgradeVaults` takes an input of `_vaults` array and upgrades them to the latest `vaultImplementation` as follows:

```solidity
 function upgradeVaults(address[] calldata _vaults, bytes[] memory _data) external onlyOwner {

        for (uint256 i = 0; i < _vaults.length; ++i) { //@audit no check if the _vault address is actually one locally stored
            if (_data.length == 0 || _data[i].length == 0) {
                IPolygonVault(_vaults[i]).upgradeTo(vaultImplementation);
            } else {
                IPolygonVault(_vaults[i]).upgradeToAndCall(vaultImplementation, _data[i]);
            }
        }
        emit UpgradedVaults(); //@audit does not emit the list of vaults actually updated
    }
```

Current implementation has several issues:

1. There is no check to verify if the input addresses actually match the ones locally stored in the contract. Owner can send totally different addresses and still can trigger the `UpgradedVaults` event
2. `UpgradedVaults` event does not contain the list of vault addresses actually updated. This prevents off-chain listeners from detecting which vaults were actually upgraded.
3. Passing specific vaults as input can lead to a scenario where a section of vaults are running on the latest implementation while another batch correspond to an older vault implementation. Not only can this create confusion among protocol admins but it can also make the upgrade process risky, specially when a bug is discovered in the vault implementation contract.


**Impact:** Lack of transparency around vault upgrades can lead to human errors associated with contract upgrades.

**Recommended Mitigation:** Consider making following changes:
1. Upgrade all vaults in the strategy at once to new implementation
2. In the event there are too many vaults and 1. is not feasible, then emit the vault indices that are upgraded. In addition, instead of passing the vault addresses as input, pass the vault indices as input to the `upgradeVaults` function.

**Stake.Link:** Resolved in [PR 151](https://github.com/stakedotlink/contracts/pull/151/commits/c62e94ca962f7ba732f1a74396e5319dd5014697)

**Cyfrin:** Resolved.
