---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-quantamm-v1-2-3-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-quantamm-v1-2
title: Consider adding a getter for `QuantAMMWeightedPool.poolDetails`
vuln_class: []
---

# Consider adding a getter for `QuantAMMWeightedPool.poolDetails`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-quantamm-v1.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md)_

---

**Description:** [`QuantAMMWeightedPool.poolDetails`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/QuantAMMWeightedPool.sol#L170) is a nested array:
```solidity
string[][] public poolDetails;
```
Nested array needs both indexes to access an element. To query for the whole array a custom getter would be needed. This could be useful for off-chain monitoring.

Reported by the protocol during audit.

**QuantAMM:** Fixed in [`ee1fbb8`](https://github.com/QuantAMMProtocol/QuantAMM-V1/commit/ee1fbb8db9d113f04c0b99fe766800dc80cf1ff2)

**Cyfrin:** Verified.
