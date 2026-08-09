---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-10-13-thestandard-io-2-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-10-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md
tags:
- firm:zokyo
- report:2022-10-13-thestandard-io
title: Potential DOS from block gas limit in TokenManager.
vuln_class: []
---

# Potential DOS from block gas limit in TokenManager.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-10-13-TheStandard.io.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md)_

---

**Description**

TokenManager.sol
DOS - Block Gas Limit: For large array lengths, the gas usage will be significantly higher and can lead to the failure of a transaction to be included in the blockchain due to Block Gas Limit
https://swcregistry.io/docs/SWC-128

**Recommendation**

Consider mechanisms to handle large arrays to prevent exceeding block gas limit, such as pagination or limiting array size.

**Re-audit comment**

Unresolved
