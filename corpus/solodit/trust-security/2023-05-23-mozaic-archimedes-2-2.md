---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-2-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-L-3 XMozToken cannot be added to its own whitelist
vuln_class: []
---

# TRST-L-3 XMozToken cannot be added to its own whitelist

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:**
By design, XMozToken should always be in the whitelist. However, `updateTransferWhitelist()`
implementation forbids both removal and insertion of XMozToken to the whitelist.
```solidity 
            function updateTransferWhitelist(address account, bool add) external  onlyMultiSigAdmin {
                    require(account != address(this), "updateTransferWhitelist: 
                          Cannot remove xMoz from whitelist");
                    if(add) _transferWhitelist.add(account);
                 else _transferWhitelist.remove(account);
            emit SetTransferWhitelist(account, add);
            }
```

**Recommended Mitigation:**
Move the **require** statement into the **else** clause.

**Team response:**
Fixed.

**Mitigation review:**
The issue has been addressed by manually adding the contract to the transfer whitelist in the 
constructor.
