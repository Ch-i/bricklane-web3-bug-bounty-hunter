---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-07-21-itrustfinance-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2021-07-21T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-07-21-ITrustFinance.md
tags:
- firm:zokyo
- report:2021-07-21-itrustfinance
title: Public functions should be declared external to save gas.
vuln_class: []
---

# Public functions should be declared external to save gas.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-07-21-ITrustFinance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-07-21-ITrustFinance.md)_

---

**Description**

iTrustInsecureV2.sol, onERC721Received(), line 269.

**Recommendation**:

Function should be declared as external.
