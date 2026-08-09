---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-2-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: 2-step ownership transfer
vuln_class: []
---

# 2-step ownership transfer

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In Contract VaultETH_V2, method `transferOwnership()` allows the current DEFAULT_ADMIN_ROLE to set a new DEFAULT_ADMIN_ROLE. If the wrong address is set for the `newOwner`, it will be irreversible.
Instead, opt for a 2-step ownership transfer. In the first step, the current DEFAULT_ADMIN_ROLE sets the pendingNewOwner followed by pendingNewOwner accepting the ownership.

**Recommendation**: 

Update the ownership transfer to 2-step process as suggested.
