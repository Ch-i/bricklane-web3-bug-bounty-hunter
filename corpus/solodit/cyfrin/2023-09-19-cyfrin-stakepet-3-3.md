---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-stakepet-3-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-stakepet
title: '`++i` costs less gas than `i++`, especially when it''s used in `for`-loops
  (`--i`/`i--` too)'
vuln_class: []
---

# `++i` costs less gas than `i++`, especially when it's used in `for`-loops (`--i`/`i--` too)

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-stakepet.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md)_

---

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

127:         for (uint256 i = 1; i <= currentPetId; i++) {

131:                 j++;

137:         for (uint256 i = 0; i < j; i++) {

147:         for (uint256 i = 0; i < _contractIDs.length; i++) {

```

**Client:** Fixed in [27225c2](https://github.com/Ranama/StakePet/commit/27225c256c3173cc306045949584b66be7f60c0f)

**Cyfrin:** Verified.
