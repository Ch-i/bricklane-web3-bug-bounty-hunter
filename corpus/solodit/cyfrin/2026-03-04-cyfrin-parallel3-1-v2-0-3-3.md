---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-3-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: Incorrect link to Angle contracts across protocol
vuln_class: []
---

# Incorrect link to Angle contracts across protocol

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** Parallelizer protocol is fork of Angle, it always refers origin implementation. However link pattern doesn't work anymore. It uses `parallelizer` folder, however there is no such folder in Angle's GitHub.
```solidity
/// @dev This contract is an authorized fork of Angle's `AccessControlModifiers` contract
/// https://github.com/AngleProtocol/angle-transmuter/blob/main/contracts/parallelizer/facets/AccessControlModifiers.sol
```

**Recommended Mitigation:** Update folder name from `parallelizer` to `transmuter` in all such links to make them work. It should be done across all forked contracts.

**Parallel:** Fixed in commit [08bc292](https://github.com/parallel-protocol/parallel-parallelizer/commit/08bc292d52bee8505e6f67883b3059e8faf1696f).
