---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-2-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-06-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
tags:
- firm:cyfrin
- report:2024-06-17-cyfrin-templedao-v2-1
title: Fee-on-transfer tokens are not supported in spice auction
vuln_class: []
---

# Fee-on-transfer tokens are not supported in spice auction

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-06-17-cyfrin-templedao-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md)_

---

**Description:** Fee-on-transfer tokens are not supported in spice auction contract, which might result in incorrect calculation in auction tokens.

**Recommended Mitigation:** Use pre/post balance difference to calculate actually moved bid token amount.

**Temple DAO:**
Fixed in [PR 1046](https://github.com/TempleDAO/temple/pull/1046)

**Cyfrin:** Verified
