---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-2-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-L-4 Admin check is overly gas-intensive
vuln_class: []
---

# TRST-L-4 Admin check is overly gas-intensive

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:**
Hats checks for most operations that the caller is an authorized hat admin. The function 
implementing this check is `isAdminOfHat()`. The function loops and checks if the sender is a 
wearer of a lower-level hat.
```solidity
        while (adminHatLevel > 0) {
             if (isWearerOfHat(_user, getAdminAtLevel(_hatId, adminHatLevel))) 
        {
                return true;
            }
        // should not underflow given stopping condition > 0
            unchecked {
                --adminHatLevel;
            }
        }
```
The issue is that calling `getAdminAtLevel()` for every level is very gas intensive. The vast 
majority of the cost of the function is resolving the hat level using `getHatLevel()`, but it is 
implemented recursively. Most of the gas can be saved by refactoring this code, which will 
be used by almost every interaction with Hats.

**Recommended mitigation:**
Refactor some part of the described code flow so that it will be less gas intensive for hats 
with linked trees

**Team response:**
Accepted; refactored to increase efficiency

**Mitigation review:**
Fixed, but introduced new issue. The new implementation checks at the end of 
`isAdminOfHat()` if the hat is linked to another tree.
```solidity
        // if we get here, we're at the top of _hatId's local tree
             linkedTreeAdmin = linkedTreeAdmins[getTophatDomain(_hatId)];
        if (linkedTreeAdmin == 0) {
            // tree is not linked
                return isWearerOfHat(_user, getLocalAdminAtLevel(_hatId, 0));
        } else {
            if (isWearerOfHat(_user, linkedTreeAdmin)) return true; // user  wears the linkedTreeAdmin
            else return isAdminOfHat(_user, linkedTreeAdmin); 
                // check if  user is admin of linkedTreeAdmin (recursion)
        }
```
Importantly, it is never checked if user is wearer of the admin hat at level 0, in the event that 
the tree is linked. The impact is lack of adminship at the top of the tree.
