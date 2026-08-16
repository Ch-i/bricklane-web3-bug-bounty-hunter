---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-7
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: Hardcoded cluster size in `withdrawValidator` can cause losses to operators
  or protocol for strategies with larger cluster sizes
vuln_class: []
---

# Hardcoded cluster size in `withdrawValidator` can cause losses to operators or protocol for strategies with larger cluster sizes

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** `CasimirManager::withdrawValidator` calculates the owed balance on withdrawal, ie. shortfall from the initial 32 ether. It then tries to recover the owed amount from the operators tagged to the validator. However, while calculating recovery amount, a hardcoded cluster size of `4` is used.

```solidity
function withdrawValidator(
    uint256 stakedValidatorIndex,
    WithdrawalProofs memory proofs,
    ISSVClusters.Cluster memory cluster
) external {
    onlyReporter();

    // ... more code

    uint256 owedAmount = VALIDATOR_CAPACITY - finalEffectiveBalance;
    if (owedAmount > 0) {
        uint256 availableCollateral = registry.collateralUnit() * 4;
        owedAmount = owedAmount > availableCollateral ? availableCollateral : owedAmount;
>       uint256 recoverAmount = owedAmount / 4; //@audit hardcoded operator size
        for (uint256 i; i < validator.operatorIds.length; i++) {
            registry.removeOperatorValidator(validator.operatorIds[i], validatorId, recoverAmount);
        }
    }

    // .... more code

```

**Impact:** This has 2 side effects:
1. Operators lose higher % of collateral balance in strategies with large cluster sizes
2. On the other hand, since `owedAmount` is capped to `4 * collateralUnit`, it is also likely that protocol ends up recovering less than it should.

**Recommended Mitigation:** Consider using the `clusterSize` of the strategy instead of a hardcoded number.

**Casimir:**
Fixed in [7497e8c](https://github.com/casimirlabs/casimir-contracts/commit/7497e8cefae018a46606b4722c9bc20d03d0d23c).

**Cyfrin:** Verified.
