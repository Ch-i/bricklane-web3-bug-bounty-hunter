---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-0-8
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-H-9 Anybody can withdraw the admin fees in the 4pool for themselves
vuln_class: []
---

# TRST-H-9 Anybody can withdraw the admin fees in the 4pool for themselves

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
The admin-only function `withdrawAdminFees()` is responsible for collecting the 4pool admin 
fees, the way this is done is by withdrawing the excess amount of tokens in the contract 
relative to the variables tracking the token balances. The function `skim()` does the same 
thing as `withdrawAdminFees()` but it’s a public function, meaning anybody can withdraw the 
admin fees to an arbitrary address.

**Recommended Mitigation:**
Because skim() is supposed to be called by the team and/or a trusted address to collect 
$CASH rebase restricting access to the skim() function only to the team and/or trusted 
addresses solves the issue. 
Important to note that when collecting the $CASH rebase the function withdrawAdminFees() 
should be called first, then the rebase should be distributed, and then `skim()` should be 
followed. If the order is not followed the rebase might be collected as admin fees or the 
admin fees might be collected as rebase.

**Team response:**
Fixed

**Mitigation Review:**
The issue has been resolved as suggested, a modifier `onlyOwnerOrRebaseHandler()` which 
allows calls only from the owner and the rebase handler contract has been applied to both 
the `withdrawAdminFees()` and `skim()` functions.
