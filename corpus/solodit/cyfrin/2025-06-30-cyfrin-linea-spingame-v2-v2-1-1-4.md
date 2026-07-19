---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-30-cyfrin-linea-spingame-v2-v2-1-1-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-06-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-30-cyfrin-linea-spingame-v2-v2-1
title: '`GelatoVRFConsumerBase` is not upgrade-safe'
vuln_class: []
---

# `GelatoVRFConsumerBase` is not upgrade-safe

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-30-cyfrin-linea-spingame-v2-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md)_

---

**Description:** The `SpinGame` contract has been changed to be upgradeable. But, the contract inherits from `GelatoVRFConsumerBase`, which is not upgrade-safe as it lacks a reserved storage gap (`uint256[x] private __gap`) to prevent future storage collisions. This poses a risk if the `GelatoVRFConsumerBase` contract is modified upstream (e.g. adds state variables), it could lead to storage layout corruption during upgrades.

Since `GelatoVRFConsumerBase` is an external dependency outside the control of the audited codebase, this risk cannot be addressed directly within that contract.

However to mitigate the risk, consider adding a storage buffer to account for potential future changes in `GelatoVRFConsumerBase`. This can be done by:

1. Adding a `_gap` in `SpinGame` itself:

   ```solidity
   uint256[x] private __gelatoBuffer;
   ```

2. Alternatively, inserting an intermediate "buffer" contract in the inheritance chain that exists solely to reserve storage space:

   ```solidity
   contract GelatoVRFGap {
       uint256[x] private __gap;
   }

   contract SpinGame is ..., GelatoVRFConsumerBase, GelatoVRFGap
   ```

This ensures that even if `GelatoVRFConsumerBase` adds storage in the future, it won't overwrite critical storage slots in `SpinGame`.

**Linea:** Fixed in commit [`9f9d9fd`](https://github.com/Consensys/linea-hub/pull/554/commits/9f9d9fd76d2672f572e31079b5811bf6f0f48eed)

**Cyfrin:** Verified, first storage slots in the contract now is `uint256[50] private __gelatoBuffer`
