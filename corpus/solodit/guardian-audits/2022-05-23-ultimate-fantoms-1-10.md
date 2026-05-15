---
affected_contracts: []
derives_from: []
id: solodit-guardian-audits-2022-05-23-ultimate-fantoms-1-10
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2022-05-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md
tags:
- firm:guardian-audits
- report:2022-05-23-ultimate-fantoms
title: RS-2 | Unequal Royalty Rewards
vuln_class: []
---

# RS-2 | Unequal Royalty Rewards

_Section severity (from Solodit section header): Low_  
_Audit firm: Guardian Audits_  
_Source report: [2022-05-23-Ultimate Fantoms.md](https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md)_

---

**Description**

In the `receive` and `fallback` functions, the rewards distribution to `CYBERs` holders can only occur before the second mint and never after.

**Recommendation**

Ensure this is the expected behavior. If it isn’t, refactor the reward logic to more fairly include `CYBERs` holders.

**Resolution**

Ultimate Fantoms: Resolved.
