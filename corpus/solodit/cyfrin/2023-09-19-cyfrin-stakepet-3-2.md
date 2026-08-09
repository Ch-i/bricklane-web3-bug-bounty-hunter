---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-stakepet-3-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-stakepet
title: Don't initialize variables with default value
vuln_class: []
---

# Don't initialize variables with default value

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-stakepet.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md)_

---

```solidity
File: StakePet.sol

128:     uint256 public s_closedAtTimestamp = 0; // The timestamp that the contract was closed down

409:         uint256 _totalValueWantsClosedown = 0;

410:         for (uint256 i = 0; i < _idsOfMajorityThatWantsClosedown.length; i++) {

```

```solidity
File: StakePetManager.sol

73:         for (uint256 i = 0; i < _contractIDs.length; i++) {

75:             for (uint256 j = 0; j < _petIDs[i].length; j++) {

108:         for (uint256 i = 0; i < _contractIDs.length; i++) {

110:             for (uint256 j = 0; j < _petIDs[i].length; j++) {

123:         uint256 j = 0;

137:         for (uint256 i = 0; i < j; i++) {

147:         for (uint256 i = 0; i < _contractIDs.length; i++) {

```

**Client:** Fixed in [970b71c](https://github.com/Ranama/StakePet/commit/970b71cfe73760dc694b0c0e1e5a3a77dc704c8c)

**Cyfrin:** Verified.
