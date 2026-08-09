---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-M-2 Multisig could become permanently locked
vuln_class: []
---

# TRST-M-2 Multisig could become permanently locked

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:**
As described, the senate can remove council members. It can also adjust the threshold for 
quorum using the **TYPE_ADJ_THRESHOLD** proposal type. Both remove and adjust operations 
do not perform an important security validation, that the new council member count and 
threshold number allow future proposal to pass.

**Recommended Mitigation:**
Verify that **councilMembers.length >= threshold**, after execution of the proposal.

**Team Response:**
Fixed.

**Mitigation review:**
The TYPE_ADJ_THRESHOLD proposal now checks the new threshold is safe. However it is not 
checked during owner removal.
