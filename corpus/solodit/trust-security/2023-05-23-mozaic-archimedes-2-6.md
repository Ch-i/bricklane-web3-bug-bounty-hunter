---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-2-6
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-L-8 Admin can set plugin fee to 100%
vuln_class: []
---

# TRST-L-8 Admin can set plugin fee to 100%

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:** 
The admin can set Mozaic's cut from strategy earnings through setFee(), up to 100%.
```solidity
        function setFee(uint256 _mozaicFeeBP, uint256 _treasuryFeeBP)  external onlyOwner {
             require(_mozaicFeeBP <= BP_DENOMINATOR, "Stargate: fees > 100%");
                require(_treasuryFeeBP <= BP_DENOMINATOR, "Stargate: fees > 100%");
            mozaicFeeBP = _mozaicFeeBP;
        treasuryFeeBP = _treasuryFeeBP;
```
