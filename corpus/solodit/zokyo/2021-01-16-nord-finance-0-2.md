---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-01-16-nord-finance-0-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2021-01-16T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-01-16-Nord%20Finance.md
tags:
- firm:zokyo
- report:2021-01-16-nord-finance
title: Calling twice safeApprove or approve methods and passing first time 0 and second
  time amount of tokens does not solve potential double spending problem as they should
  be executed as separate transactions and after first transaction mined to
vuln_class: []
---

# Calling twice safeApprove or approve methods and passing first time 0 and second time amount of tokens does not solve potential double spending problem as they should be executed as separate transactions and after first transaction mined to block, user has to verify that spender did not spend any tokens approved before.

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2021-01-16-Nord Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-01-16-Nord%20Finance.md)_

---

**Recommendation**:

Reimplement mitigation of double spend problem or remove approval to 0 as it does not
handle double spending problem.
