---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-14-ondo-finance-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-06-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-14-Ondo%20Finance.md
tags:
- firm:zokyo
- report:2023-06-14-ondo-finance
title: Claim excess is paused
vuln_class: []
---

# Claim excess is paused

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-14-Ondo Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-14-Ondo%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**

At the contract deployment the claimExcess function of the RWAHubInstantMints is paused by default which may lead to an excess call to `unpause` function before it actually starts working

**Recommendation**: 

initialize the instantRedemptionPaused with the false if claims need to be ready right after deployment
​
