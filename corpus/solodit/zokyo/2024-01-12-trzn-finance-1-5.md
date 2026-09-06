---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-1-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Missing Fallback Function to reject accidental Ether transfers to contract
  StableSwap_V2
vuln_class: []
---

# Missing Fallback Function to reject accidental Ether transfers to contract StableSwap_V2

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Recommendations**:

Consider implementing a non-payable fallback function with appropriate logging to handle any unexpected Ether transfers to this contract in order to prevent Ether from being stuck in the contract.
