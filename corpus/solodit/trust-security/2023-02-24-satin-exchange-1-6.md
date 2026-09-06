---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-1-6
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-M-7 It’s possible to freely detach tokens from a gauge
vuln_class: []
---

# TRST-M-7 It’s possible to freely detach tokens from a gauge

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
`withdrawToken()` is a public function that takes as an input an **amount** and a **tokenId**. It then 
proceeds to detach the token from the gauge it’s associated with and withdraw the amount. 
A user could pass 0 as an amount with the tokenId he wants to detach, which will withdraw
nothing and detach the token. The function was meant to be called by `withdraw()` internally
which only detaches the token if the full amount deposited is being withdrawn.
In addition to this, `withdrawToken()` doesn’t emit the Withdraw event.

**Recommended mitigation:**
Make `withdrawToken()` internal instead of public.

**Team response:**
Fixed

**Mitigation Review:**
The issue has been resolved as suggested, now `withdrawToken()` is declared as an internal 
function.
