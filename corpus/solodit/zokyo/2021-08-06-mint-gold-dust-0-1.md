---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-08-06-mint-gold-dust-0-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2021-08-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md
tags:
- firm:zokyo
- report:2021-08-06-mint-gold-dust
title: Use fixed version of Solidity
vuln_class: []
---

# Use fixed version of Solidity

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2021-08-06-Mint Gold Dust.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md)_

---

**Description**

The project utilises Solidity ^0.8.0 version. Though, the standard auditor s checklist states for
the usage of the fixed version of the Solidity. So it is preferable to use the 0.8.6 version of
Solidity (the latest stable release).

**Recommendation**:

Use a fixed version of the Solidity (e.g. the latest stable release 0.8.6).
