---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-11-15-milestonebased-0-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2021-11-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-11-15-milestoneBased.md
tags:
- firm:zokyo
- report:2021-11-15-milestonebased
title: Function setUrl should do sanity checks even if the caller is the owner, the
  owner can make mistakes too.
vuln_class: []
---

# Function setUrl should do sanity checks even if the caller is the owner, the owner can make mistakes too.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-11-15-milestoneBased.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-11-15-milestoneBased.md)_

---

**Recommendation**:

Do a sanity check where you are checking if the new uri has a different value from the old one,
to not be able to set the same value twice and consume gas.
