---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-05-06-shield-finance-0-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2021-05-06T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-06-Shield%20Finance.md
tags:
- firm:zokyo
- report:2021-05-06-shield-finance
title: Missing total amount calculation
vuln_class: []
---

# Missing total amount calculation

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2021-05-06-Shield Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-06-Shield%20Finance.md)_

---

**Description**

Line 83, No calculations and checks for the total amount added through the addAllocations()
method.
There are no checks if the total amount exceeds the current supply, or if the new portion of
allocations added to the same vesting type exceeds the allocations, or if the next vesting type
amount added will exceed the total supply. This is the crucial point because there is no logic
for changing the frozen wallet with the allocation.

**Recommendation**:

Finish the total amount checking logic.

**Post-audit**:
After the conversation with the Shield Finance team, auditors verified the functionality and its
coverage with tests. The issue is marked as resolved.
