---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-2-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-L-5 Lack of zero-address check for important parameters
vuln_class: []
---

# TRST-L-5 Lack of zero-address check for important parameters

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:** 
Hats allows admin hats to change the **toggle** and **eligibility** set for a given hat. For example:
```solidity
    function changeHatToggle(uint256 _hatId, address _newToggle) external 
    {
        _checkAdmin(_hatId);
             Hat storage hat = _hats[_hatId];
    if (!_isMutable(hat)) {
            revert Immutable();
        }
         hat.toggle = _newToggle;
             emit HatToggleChanged(_hatId, _newToggle);
     }
```
The code lacks a zero-address check for _newToggle. There is no good reason why this value 
might need to be set to zero, and it's a standard best practice for fault-detection.
**Recommended mitigation:**
Add a zero-address check for both address parameters.

**Team response:**
Accepted

**Mitigation review:**
Fixed.
