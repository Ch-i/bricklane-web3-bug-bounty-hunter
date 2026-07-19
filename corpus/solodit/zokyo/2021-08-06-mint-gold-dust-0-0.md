---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-08-06-mint-gold-dust-0-0
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
title: Organisation record can be re-written
vuln_class: []
---

# Organisation record can be re-written

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2021-08-06-Mint Gold Dust.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md)_

---

**Description**

MGD.sol, createOrganisation()
Bool flag for the organisation name taken (orgTaken mapping) is never set. Thus, it makes
orgTaken mapping useless. The issue is marked as Medium only because the organisation
creation can be performed only by admin.

**Recommendation**:

Review the functionality, remove unused mapping or add storage setter.
