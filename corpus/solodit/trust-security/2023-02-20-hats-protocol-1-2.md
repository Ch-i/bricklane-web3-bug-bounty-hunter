---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-1-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-M-3 Linking of hat trees can freeze hat operations
vuln_class: []
---

# TRST-M-3 Linking of hat trees can freeze hat operations

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:**
Hats support tree-linking, where hats from one node link to the first level of a different 
domain. This way, the amount of levels for the linked-to tree increases by the linked-from 
level count. This is generally fine, however lack of checking of the new total level introduces 
severe risks. 
```solidity
        /// @notice Identifies the level a given hat in its hat tree
        /// @param _hatId the id of the hat in question
        /// @return level (0 to type(uint8).max)
     function getHatLevel(uint256 _hatId) public view returns (uint8) {
```
The `getHatLevel()` function can only return up to level 255. It is used by the `checkAdmin()` call 
used in many of the critical functions in the Hats contract. Therefore, if for example, 17 hat
domains are joined together in the most stretched way possible, It would result in a correct 
hat level of 271, making this calculation revert:
```solidity
        if (treeAdmin != 0) {
                 return 1 + uint8(i) + getHatLevel(treeAdmin);
            }
```
The impact is that intentional or accidental linking that creates too many levels would freeze 
the higher hat levels from any interaction with the contract.

**Recommended Mitigation:**
It is recommended to add a check in `_linkTopHatToTree()`, that the new accumulated level 
can fit in uint8. Another option would be to change the maximum level type to uint32.

**Team Response:**
Accepted; increased max level type to uint32.

**Mitigation review:**
Fixed.
