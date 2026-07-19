---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-2-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-L-5 Controller doesn't initialize supported chains properly
vuln_class: []
---

# TRST-L-5 Controller doesn't initialize supported chains properly

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:** 
Controller manages a list of **supportedChainIds** where the protocol is deployed. The 
**mainChainId** is the base chain where controller is deployed. For settling and snapshotting, 
there is different handing in case the current chainID is **mainChainId**:
```solidity
            if(mainChainId == supportedChainIds[i]) {
                   MozBridge.Snapshot memory _snapshot = mozBridge.takeSnapshot();
             _updateSnapshot(mainChainId, _snapshot);
                         } else {
                    mozBridge.requestSnapshot(supportedChainIds[i], payable(master));
                }
```
In fact, the **mainChainId** is not inserted to the list by default and needs to be manually added. 
For the protocol to function, it must be part of the list.

**Recommended mitigation:**
During construction, add **mainChainId** to the list of supported chains.

**Team response:**
Acknowledged.
