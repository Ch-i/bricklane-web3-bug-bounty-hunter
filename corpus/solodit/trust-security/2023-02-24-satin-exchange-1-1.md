---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-M-2 Anybody can forfeit partner fees if there are no partners
vuln_class: []
---

# TRST-M-2 Anybody can forfeit partner fees if there are no partners

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
The protocol accumulates fees for partners whenever a `swap()` happens and there’s at least 
one partner account. The fees can later be claimed for every partner by calling 
`claimPartnerFee()` which distributes the fees to the accounts listed as partners at the 
moment the function is called. If `claimPartnerFee()` is called when there are no partners it zeroes **partnerClaimable0** and **partnerClaimable1** without any distribution occurring, which effectively locks the fees in the contract.

**Recommended Mitigation:**
In `claimPartnerFee()` revert if the number of partners is 0.

**Team Response:**
Fixed

**Mitigation Review:**
The issue has been resolved in a different, but correct, way than the suggested one. The 
function `claimPartnerFee()` still succeeds if called when there are 0 partners, but 
**partnerClaimable0** and **partnerClaimable1** are not zeroed.
