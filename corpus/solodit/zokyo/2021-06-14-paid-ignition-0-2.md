---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-14-paid-ignition-0-2
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
title: Incorrect max check
vuln_class: []
---

# Incorrect max check

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2021-06-14-Paid Ignition.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Paid%20Ignition.md)_

---

**Description**

IgnitionCore.sol, buyTokensETH() and buyTokensQuoteAsset().
The check if the max raised is exceeded is performed without including the currently
purchased value. So the max amount can be exceeded at least once.

**Recommendation**:

Include the currently purchased value into the check, that max amount is exceeded.
