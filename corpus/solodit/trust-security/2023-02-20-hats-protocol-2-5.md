---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-2-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-L-6 Safe's registered threshold could be below minThreshold
vuln_class: []
---

# TRST-L-6 Safe's registered threshold could be below minThreshold

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:** 
The functions `setTargetThreshold()` and `reconcileSignerCount()` change the safe's registered 
threshold. Both functions do not check the new value is above or equal to **minThreshold**. 
This is not a serious issue if the HSG is defined to be the enforcer of the **minThreshold**. 
However, this was not done correctly as was described in H-2, so it would be best to never 
set the safe's version of the threshold to below **minThreshold**

**Recommended mitigation:**
Recommended mitigation steps

**Team response:**
Acknowledged; not making explicit changes because the Safe contract does not allow 
thresholds below number of owners, so we can't remove all scenarios where threshold is 
below **minThreshold**. Risks associated with this finding should be mitigated by changes done 
applied in other findings
