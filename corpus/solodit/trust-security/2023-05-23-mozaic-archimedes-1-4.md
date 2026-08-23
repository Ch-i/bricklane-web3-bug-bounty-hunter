---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-1-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-M-5 MozStaking does not reserve Moz tokens for redemptions, leading to
  unfulfillable redemptions.
vuln_class: []
---

# TRST-M-5 MozStaking does not reserve Moz tokens for redemptions, leading to unfulfillable redemptions.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:** 
When users call `redeem()` in MozStaking, they are scheduling a future redemption for a specific 
Moz amount. However, that amount is not set aside for them. Other users can "cut in line", 
request a redemption for a lower duration and empty the Moz bank. The original user would 
have to cancel redemption or wait until new users stake their Moz. 
The assumption that **Moz supply > XMoz supply** in the staking contract does not hold, as there 
is an initial XMoz supply minted in XMozToken. 

**Recommended Mitigation:**
Another state variable should be introduced to account for the reserved Moz amount. 
MozStaking should not allow new redemptions if there is currently insufficient Moz.

**Team response:**
Fixed.

**Mitigation review:**
The staking contract mints and burns tokens, ensuring it cannot run out of them.
