---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-quantamm-v1-2-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-quantamm-v1-2
title: Missing weight sum validation in `setWeightsManually` function
vuln_class: []
---

# Missing weight sum validation in `setWeightsManually` function

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-quantamm-v1.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md)_

---

**Description:** The `UpdateWeightRunner::setWeightsManually` allows privileged users (DAO, pool manager, or admin based on pool registry) to manually set weights of the pool without validating if the weights sum to 1. This check is correctly enforced the first time when weights are initialized in `_setInitialWeights`:

```solidity
// In QuantAMMWeightedPool.sol - _setInitialWeights
// Ensure that the normalized weights sum to ONE
if (uint256(normalizedSum) != FixedPoint.ONE) {
    revert NormalizedWeightInvariant();
}
```

A similar validation is missing in setWeightsManually in UpdateWeightRunner.sol, creating an inconsistency in how weight validations are handled when weights are entered manually.


**Impact:** While this function is access controlled, allowing privileged users to set weights that don't sum to 1 could cause:

- Incorrect pool valuation
- Unfair trading due to miscalculated swap amounts

It is noteworthy that although `setInitialWeights` also has privileged access, weight sum check exists in that function.


**Recommended Mitigation:** Consider adding a weight sum validation in `setWeightsManually`


**QuantAMM:** In practice and in theory the weights do not have to sum to one. Trading is done on the ratio not the absolute values of the weights. Everyone does it but if you set it to 50/50 instead of 0.5/0.5 nothing would change in what swaps were accepted by the mathematics of the pool. Our general practice with break glass measures is to include no validation as which glass needs breaking could be an unknown unknown. However, we reviewed the potential issues and actually given we use fixed point math libs that expect 1>x>0 (especially greater than 0) it does make sense to add the check so really maybe just a change in description of the issue. We will not check guard rails as that could be a valid break glass in some strange unknown.

**Cyfrin:** Acknowledged.
