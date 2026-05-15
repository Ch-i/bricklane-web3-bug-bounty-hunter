---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-M-1 Removal of Multisig members will corrupt data structures
vuln_class: []
---

# TRST-M-1 Removal of Multisig members will corrupt data structures

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:**
The Mozaic Multisig (the senate) can remove council members using the **TYPE_DEL_OWNER**
operation:
```solidity
        if(proposals[_proposalId].actionType == TYPE_DEL_OWNER) {
                (address _owner) = abi.decode(proposals[_proposalId].payload, (address));
        require(contains(_owner) != 0, "Invalid owner address");
            uint index = contains(_owner);
                for (uint256 i = index; i < councilMembers.length - 1; i++) {
            councilMembers[i] = councilMembers[i + 1];
        }
            councilMembers.pop();
                 proposals[_proposalId].executed = true;
                     isCouncil[_owner] = false;
          }
```
The code finds the owner's index in the councilMembers array, copies all subsequent 
members downwards, and deletes the last element. Finally, it deletes the **isCouncil[_owner]**
entry. 
The issue is actually in the contains() function.
 ```solidity
        function contains(address _owner) public view returns (uint) {
              for (uint i = 1; i <= councilMembers.length; i++) {
        if (councilMembers[i - 1] == _owner) {
                 return i;
             }
         }
         return 0;
         }
 ```
The function returns the index following the owner's index. Therefore, the intended **owner** is 
not deleted from **councilMembers**, instead the one after it is. The `submitProposal()` and 
`confirmTransaction()` privileged functions will not be affected by the bug, as they filter by 
**isCouncil**. However, the corruption of councilMembers will make deleting the member 
following the currently deleted owner fail, as deletion relies on finding the member in 
**councilMembers**.

**Recommended Mitigation:**
Fix the `contains()` function to return the correct index of **_owner**

**Team Response:**
Fixed.

**Mitigation review:**
Index is calculated correctly.
