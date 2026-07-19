---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-stakepet-3-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-stakepet
title: Cache array length outside of loop
vuln_class: []
---

# Cache array length outside of loop

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-stakepet.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md)_

---

If not cached, the solidity compiler will always read the length of the array during each iteration. That is, if it is a storage array, this is an extra sload operation (100 additional extra gas for each iteration except for the first) and if it is a memory array, this is an extra mload operation (3 additional gas for each iteration except for the first).

```solidity
File: StakePet.sol

410:         for (uint256 i = 0; i < _idsOfMajorityThatWantsClosedown.length; i++) {

```

```solidity
File: StakePetManager.sol

73:         for (uint256 i = 0; i < _contractIDs.length; i++) {

75:             for (uint256 j = 0; j < _petIDs[i].length; j++) {

108:         for (uint256 i = 0; i < _contractIDs.length; i++) {

110:             for (uint256 j = 0; j < _petIDs[i].length; j++) {

147:         for (uint256 i = 0; i < _contractIDs.length; i++) {

```

**Client:** Fixed in [627d09c](https://github.com/Ranama/StakePet/commit/627d09c34bb4853418e8c22ed8ce291efd7ad087)

**Cyfrin:** Verified.
