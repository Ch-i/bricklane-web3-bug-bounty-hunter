---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-1-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-M-4 Admin can transfer hat to a non-eligible target, potentially burning
  the hat
vuln_class: []
---

# TRST-M-4 Admin can transfer hat to a non-eligible target, potentially burning the hat

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:**
Hat admins may transfer child hats using `transferHat()`. It checks the hat receiver does not 
currently have a balance for this **hatId**.
```solidity
        // Check if recipient is already wearing hat; also checks storage to  maintain balance == 1 invariant
        if (_balanceOf[_to][_hatId] > 0) {
            revert AlreadyWearingHat(_to, _hatId);
         }
 ```
The issue is that it does not also check that the recipient is eligible for the **hatId**. Therefore, 
an admin could transfer a hat and then it could be immediately burnt by anyone using the 
`checkHatWearerStatus()` call.

**Recommended mitigation:**
Verify the recipient is eligible for the **hatId** before transferring it

**Team response:**
Accepted.

**Mitigation review:**
Fixed
