---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-3-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: Optimize gas usage in MozToken
vuln_class: []
---

# Optimize gas usage in MozToken

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

In `getLockedPerAgreement()`, if the **elapsed time = vestPeriod**, it would be best to just set 
**lockedAmount = 0**. 
```solidity
            if (((block.timestamp - vestStart) / 86400) <= currentVest.vestPeriod) {
                      unLockedAmount = currentVest.totalAmount * ((block.timestamp - vestStart) / 86400) /  currentVest.vestPeriod;
            lockedAmount = currentVest.totalAmount - unLockedAmount;
            } else {
            lockedAmount = 0;
        }
```
