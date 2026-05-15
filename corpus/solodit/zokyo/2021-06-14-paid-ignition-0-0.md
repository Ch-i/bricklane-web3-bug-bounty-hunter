---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-14-paid-ignition-0-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2021-06-14T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Paid%20Ignition.md
tags:
- firm:zokyo
- report:2021-06-14-paid-ignition
title: Potentially broken un-finalization
vuln_class: []
---

# Potentially broken un-finalization

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2021-06-14-Paid Ignition.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Paid%20Ignition.md)_

---

**Description**

IgnitionIDO.sol, 60, revert_finalize().
Previous pool’s total amount is restored with the fbck_finalize value. Though, fbck_finalize is
used as a buffer for storing the unsold amount from the last finalized pool. In the general
case, the pool we want to un-finalize does not match the last finalized pool (e.g. we have
finalized pool 1 and pool 2, and now we want to un-finalize pool 1). So the fbck_finalize can
store value from another finalization operation.

**Recommendation**:

Use mapping to get finalization values for every pool, or allow the un-finalization to only the
last finalized pool - add the condition that the next pool is NOT finalized.
