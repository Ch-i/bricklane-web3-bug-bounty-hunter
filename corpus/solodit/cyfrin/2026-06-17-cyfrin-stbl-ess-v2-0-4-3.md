---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-4-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`STBL_T1e_Vault::iEmergencyWithdraw` NatSpec describes a deposit-accounting
  update that the function intentionally does not perform'
vuln_class: []
---

# `STBL_T1e_Vault::iEmergencyWithdraw` NatSpec describes a deposit-accounting update that the function intentionally does not perform

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_T1e_Vault::iEmergencyWithdraw` (reached through the in-scope `STBL_XLayer_Asset_Vault::EmergencyWithdraw`) transfers the vault's entire token balance to the treasury and intentionally leaves `VaultData.assetDepositNet` and `VaultData.depositValueUSD` at their pre-drain values, since the asset is being decommissioned and the on-vault accounting is no longer used for any subsequent flow:

```solidity
function iEmergencyWithdraw() internal virtual {
    AssetDefinition memory AssetData = registry.fetchAssetData(assetID);
    address treasury = registry.fetchTreasury();
    if (treasury == address(0)) revert STBL_InvalidTreasury();
    if (AssetData.status != AssetStatus.EMERGENCY_STOP) revert STBL_AssetActive();
    uint256 balance = IERC20(AssetData.token).balanceOf(address(this));
    IERC20(AssetData.token).safeTransfer(treasury, balance);
    emit EmergencyFundsWithdraw(balance);
}
```

The NatSpec on the function says the opposite:

> "Reduces the net asset deposit tracking by the withdrawn amount"

A reader following the comment will expect `VaultData.assetDepositNet` to be decremented, which is the convention every other balance-moving path actually follows (`STBL_T1e_Vault::depositERC20` increments, `STBL_T1e_Vault::withdrawERC20` decrements, `STBL_T1e_Vault::iDistributeYield` decrements). The mismatch between the stated and actual behavior is a documentation defect, not a code bug.

**Impact:** Misleading NatSpec only. Future readers and downstream integrators may rely on the stated decrement and write code or tests that assume the post-drain accounting is zeroed, which it is not.

**Recommended Mitigation:** Update the NatSpec on `STBL_T1e_Vault::iEmergencyWithdraw` so it matches the function's actual behaviour:

```diff
 /**
  * @notice Drains a specified amount of tokens from the vault to treasury during emergency situations
  * @dev Emergency function that transfers tokens directly to treasury when asset is disabled
  * @dev Can only be executed when the asset status is not ENABLED for security purposes
- * @dev Reduces the net asset deposit tracking by the withdrawn amount
+ * @dev Vault deposit accounting (`assetDepositNet`, `depositValueUSD`) is intentionally
+ *      left untouched: the asset is moving to EMERGENCY_STOP and the vault's accounting
+ *      is no longer consumed by any subsequent flow.
  * @custom:event EmergencyFundsWithdraw Emitted with the amount of tokens withdrawn
  * @custom:security Only callable when asset is disabled and treasury address is valid
  */
 function iEmergencyWithdraw() internal virtual {
```

**STBL:** Acknowledged. This is part of asset life cycle management. (i.e if `haircut` utilization of the asset is between 25-75% in use then asset becomes disabled but if `haircut` utilization is over 75% then asset goes into emergency stop and protocol treasury takes ownership of asset to liquidate and admin will do the task of redemption to YLD holder provided they deposit USST)
