---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-9
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: Operator is not removed in Registry when validator has `owedAmount == 0`
vuln_class: []
---

# Operator is not removed in Registry when validator has `owedAmount == 0`

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** `CasimirManager::withdrawValidator()` function is designed to remove a validator after a full withdrawal. It checks whether the final effective balance of the removed validator is sufficient to cover the initial 32 ETH deposit. If for some reason such as slashing, the final effective balance is less than 32 ETH, the operators must recover the missing portion by calling `registry.removeOperatorValidator()`.


```solidity
uint256 owedAmount = VALIDATOR_CAPACITY - finalEffectiveBalance;
if (owedAmount > 0) {
    uint256 availableCollateral = registry.collateralUnit() * 4;
    owedAmount = owedAmount > availableCollateral ? availableCollateral : owedAmount;
    uint256 recoverAmount = owedAmount / 4;
    for (uint256 i; i < validator.operatorIds.length; i++) {
        // @audit if owedAmount == 0, this function is not called
        registry.removeOperatorValidator(validator.operatorIds[i], validatorId, recoverAmount);
    }
}
```

However, the `removeOperatorValidator()` function also has the responsibility to update other operators' states, such as `operator.validatorCount`. If this function is only called when `owedAmount > 0`, the states of these operators will not be updated if the validator fully returns 32 ETH.

**Impact:** The `operator.validatorCount` will not decrease in the `CasimirRegistry` when a validator is removed. As a result, the operator cannot withdraw the collateral for this validator, and the collateral will remain locked in the `CasimirRegistry` contract.

**Recommended Mitigation:** The function `registry.removeOperatorValidator()` should also be called  with `recoverAmount = 0` when `owedAmount == 0`. This will free up collateral for operators.

**Casimir:**
Fixed in [d7b35fc](https://github.com/casimirlabs/casimir-contracts/commit/d7b35fce9925bfa2133fd4e16ae11e483ab4daa4)

**Cyfrin:** Verified.
