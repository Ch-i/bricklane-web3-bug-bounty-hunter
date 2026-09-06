---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[H-02] Wrong check in `claimCalculation` will result in less rewards received
  for users'
vuln_class: []
---

# [H-02] Wrong check in `claimCalculation` will result in less rewards received for users

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

**Impact:**
High, as this will lead to a monetary loss for users

**Likelihood:**
Medium, as it happens only for the pool with an ID of 1

**Description**

The first `if` statement in `claimCalculation` checks `if (_poolNumber == 1)` and does not factor in any inflation for that particular pool. The problem is that (it is also explained in the comment above the `if` statement) the intention was to check if there was only 1 pool (or if it was the first pool) then there is no need to do inflation calculations, which result in a higher reward. But when you have `_poolNumber == 1` this means that you have at least 2 pools, as arrays start from an index of 0, so 1 is actually for the second pool in the `pool` array. This will result in all claimers of the rewards for staking in the pool with an ID of 1 missing out on their inflation rewards.

**Recommendations**

Change the code in the following way:

```diff
- if (_poolNumber == 1) {
+ if (_poolNumber == 0) {
```
