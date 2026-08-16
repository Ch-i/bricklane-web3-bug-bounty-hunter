---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-11-15-milestonebased-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2021-11-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-11-15-milestoneBased.md
tags:
- firm:zokyo
- report:2021-11-15-milestonebased
title: Function setTrustedSigner should do sanity checks even if the caller is the
  owner, the owner can make mistakes too.
vuln_class: []
---

# Function setTrustedSigner should do sanity checks even if the caller is the owner, the owner can make mistakes too.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-11-15-milestoneBased.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-11-15-milestoneBased.md)_

---

**Recommendation**:

Do a sanity check where you are checking if the new trusted signer has a different value from
the old one, to not set the same value twice and consume gas.
