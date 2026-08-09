---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-11-01-tokendistributor-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-TokenDistributor.md
tags:
- firm:pashov-audit-group
- report:2023-11-01-tokendistributor
title: '[L-01] Insufficient input validation'
vuln_class: []
---

# [L-01] Insufficient input validation

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-11-01-TokenDistributor.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-TokenDistributor.md)_

---

In `initializeDistributor` multiple parameters are insufficiently validated:

- `_maxEthContributionPerAddress` is only checked that is > 0, but this seems like too low of a limit
  , maybe use 1e18
- `_distributionStartTimestamp` is checked that it is `>= block.timestamp` but it isn't checked that it isn't too further away in the future
- `_distributionEndTimestamp` is checked that it is `> _distributionStartTimestamp` but it isn't checked that it isn't too further away in the future

For `_maxEthContributionPerAddress` consider using a bigger lower limit, like `1e18` for example. For `_distributionStartTimestamp` check that it isn't more than 1 week or month, or year away in the future, depending on your use case, and for `_distributionEndTimestamp` check that it isn't more than (again) a week or a month or a year away after the start timestamp.
