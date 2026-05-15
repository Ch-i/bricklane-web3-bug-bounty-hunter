---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-4-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[I-02] Overcomplicated math calculations'
vuln_class: []
---

# [I-02] Overcomplicated math calculations

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

The following code from `calculateShareFromTime` is overcomplicated and can be simplified in the following way:

```diff
- uint256 requiredRebases = ((_currentTime - startTimestamp) - (_previousTime - startTimestamp)) / 1 days;
+ uint256 requiredRebases = (_currentTime - _previousTime) / 1 days;
```
