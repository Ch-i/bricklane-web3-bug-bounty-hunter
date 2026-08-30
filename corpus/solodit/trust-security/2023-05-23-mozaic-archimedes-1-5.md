---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-1-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-M-6 MozToken will have a much larger fixed supply than intended.
vuln_class: []
---

# TRST-M-6 MozToken will have a much larger fixed supply than intended.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:** 
MozToken is planned to be deployed on all supported chains. Its total supply will be 1B. 
However, its constructor will mint 1B tokens on each deployment.
```solidity
        constructor( address _layerZeroEndpoint, uint8 _sharedDecimals
            ) OFTV2("Mozaic Token", "MOZ", _sharedDecimals, _layerZeroEndpoint) {
            _mint(msg.sender, 1000000000 * 10 ** _sharedDecimals);
                isAdmin[msg.sender] = true;
            }
```

**Recommended Mitigation:**
Pass the minted supply as a parameter. Only on the main chain, mint 1B tokens.

**Team response:**
Fixed.

**Mitigation review:**
According to Mozaic, Moz and XMoz tokens will be deployed on base chain with the contracts 
audited. When deploying on additional chains, they will remove the `_mint()` call.
