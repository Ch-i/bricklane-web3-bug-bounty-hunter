---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-14-impossible-finance-1-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2021-06-14T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Impossible%20Finance.md
tags:
- firm:zokyo
- report:2021-06-14-impossible-finance
title: Hardcoded address
vuln_class: []
---

# Hardcoded address

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2021-06-14-Impossible Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Impossible%20Finance.md)_

---

**Description**

StableXPair.sol, line 189
The governance address has unique permissions to change the setter and collect the fees.
Though there is no way to change that address and the address is hardcoded, so the contract
has no ability to change that permission in case of governance change or compromise.

**Recommendation**:

Add the governance address to the arguments of the initialize function and/or add the ability
in the StableXFactory.sol contract to change this address and pass the required one.
