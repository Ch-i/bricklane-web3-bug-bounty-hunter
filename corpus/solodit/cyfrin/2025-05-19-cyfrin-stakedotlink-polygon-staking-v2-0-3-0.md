---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0-3-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-05-19T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0
title: Validate total fees in `PolygonStrategy::updateFee` only if the `_feeBasisPoints
  > 0`
vuln_class: []
---

# Validate total fees in `PolygonStrategy::updateFee` only if the `_feeBasisPoints > 0`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md)_

---

**Description:** While updating the fee in `PolygonStrategy::updateFee`, if `_feeBasisPoints == 0`, the fee at the index is replaced with the fee at the last index of the array, and the last element is popped from the array.

Since fees is a non-negative value, there is no need to perform the total fee check in this scenario. It is worth highlighting that the check is gas heavy as it involves looping over a fee array.

```solidity
if (_totalFeesBasisPoints() > 3000) revert FeesTooLarge();
```

**Recommended Mitigation:** Consider moving the check into the `else` block.

**Stake.Link:** Resolved in [PR 151](https://github.com/stakedotlink/contracts/pull/151/commits/44a8f032e5ae9697440f3b7d83a10538ab88e877)

**Cyfrin:** Resolved.
