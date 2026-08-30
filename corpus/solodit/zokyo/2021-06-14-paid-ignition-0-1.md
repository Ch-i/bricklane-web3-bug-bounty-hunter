---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-14-paid-ignition-0-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2021-06-14T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Paid%20Ignition.md
tags:
- firm:zokyo
- report:2021-06-14-paid-ignition
title: Unclear behavior
vuln_class: []
---

# Unclear behavior

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2021-06-14-Paid Ignition.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Paid%20Ignition.md)_

---

**Description**

IgnitionCore.sol, recover_token().
There is no documentation or explanation of what token is recovered (is it a pool token or
payment token etc). And since that, there is no clarity if pool’s tokenTotalAmount should be
increased (in case pool token is recovered).

**Recommendation**:

Verify the functionality, add the documentation and add the total pool token amount
re-calculation if needed.
