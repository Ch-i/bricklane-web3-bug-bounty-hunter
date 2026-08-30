---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-1-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Users can easily bypass collateral `depositCap` limit using multiple deposits
  under the limit
vuln_class: []
---

# Users can easily bypass collateral `depositCap` limit using multiple deposits under the limit

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** Margin collateral has a `depositCap` configuration to limit the total deposited amount for a particular collateral type.

But validation in `_requireEnoughDepositCap()` reverts when the current amount being deposited is greater than `depositCap`.

```solidity
function _requireEnoughDepositCap(address collateralType, UD60x18 amount, UD60x18 depositCap) internal pure {
    if (amount.gt(depositCap)) {
        revert Errors.DepositCap(collateralType, amount.intoUint256(), depositCap.intoUint256());
    }
}
```

As it doesn't check the total deposited amount for that collateral type, users can deposit as much as they want by using separate transactions each being under `depositCap`.

**Impact:** Users can deposit more margin collateral than `depositCap`.

**Recommended Mitigation:** `_requireEnoughDepositCap` should check if the total deposited amount for that collateral type plus the new deposit is not greater than `depositCap`.

**Zaros:** Fixed in commit [0d37299](https://github.com/zaros-labs/zaros-core/commit/0d37299f6d5037afc9863dc6f0ae3871784ce376).

**Cyfrin:** Verified.
