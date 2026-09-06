---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-01-16-nord-finance-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2021-01-16T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-01-16-Nord%20Finance.md
tags:
- firm:zokyo
- report:2021-01-16-nord-finance
title: ClaimRewardProxy.removeRewardDistributor, FundDivisionStrategy.unwhitelistStrategy
  methods are using nonoptimal removal approach.
vuln_class: []
---

# ClaimRewardProxy.removeRewardDistributor, FundDivisionStrategy.unwhitelistStrategy methods are using nonoptimal removal approach.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-01-16-Nord Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-01-16-Nord%20Finance.md)_

---

**Recommendation**:

Reassign last element to position of element to be deleted and call method pop on that array.
