---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-0-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-H-4 It’s possible to DOS the distribution of weekly emissions, and as
  a consequence the whole protocol
vuln_class: []
---

# TRST-H-4 It’s possible to DOS the distribution of weekly emissions, and as a consequence the whole protocol

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
The function `updatePeriod()`, responsible for the weekly distribution of emissions, internally 
calls `distributeAll()` on SatinVoter.sol which loops over all of the existing gauges, updates 
them and distribute rewards if necessary. This can be an issue when the number of gauges is 
so high that the execution would cost more gas than the maximum amount permitted in a 
block, thus making the function call to`updatePeriod()` always revert.

**Recommended Mitigation:**
Call distribute() only for the Satin/$CASH LP gauge.

**Team response:**
Fixed

**Mitigation Review:**
The issue has been resolved as suggested, `updatePeriod()` now only updates and distributes 
emissions to the Satin / $CASH LP gauge.
