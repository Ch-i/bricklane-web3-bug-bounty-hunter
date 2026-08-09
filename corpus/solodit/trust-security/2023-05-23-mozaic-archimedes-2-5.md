---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-2-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-L-6 Admin is in control of the funds
vuln_class: []
---

# TRST-L-6 Admin is in control of the funds

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:** 
A malicious or hacked admin account has many different ways to drain user's funds and take 
over governance permanently. This includes, but is not limited to:
1. Using `withdrawToken()` in Vault.sol
2. Setting trusted addresses like the bridge, LP token and plugins in Vault.sol
3. Changing plugin attributes and logic through `configPlugin()`in StargatePlugin.sol
4. Setting trusted remote bridges trough setBridge() in MozBridge 


 ### TRST-L-7 Admin can mint or burn fees
 **Description:** 
The Moz and XMoz tokens expose `mint()`/`burn()` interfaces that an admin can use arbitrarily.
