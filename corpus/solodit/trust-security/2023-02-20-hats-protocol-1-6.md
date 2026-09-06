---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-1-6
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-M-7 Hats can't be renounced when not worn, leading to abuse concerns
vuln_class: []
---

# TRST-M-7 Hats can't be renounced when not worn, leading to abuse concerns

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:**
Hats can be renounced by the owner using `renounceHat()` call. They can only be renounced 
when currently worn, regardless if they have a positive balance. Issues can arise from abuse 
by **toggle or eligibility delegates**. They can temporarily disable or sanction the wearer so 
that it cannot be renounced. At a later point, when the wearer is to be made accountable for 
their responsibilities, they could be toggled back on and penalize an innocent hat wearer.


**Recommended mitigation:**
Allow hats to be renounced even when they are not worn right now. A different event 
parameter can be used to display if they were renounced while worn or not

**Team response:**
Accepted.

**Mitigation review:**
Fixed by applying the suggested mitigation.
