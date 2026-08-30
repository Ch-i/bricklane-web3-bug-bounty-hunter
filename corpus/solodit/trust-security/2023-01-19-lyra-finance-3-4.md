---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-3-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: Adopt single-validation pattern
vuln_class: []
---

# Adopt single-validation pattern

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

Some parameters are checked in multiple places for the same conditions, but are only 
changeable from a single gateway. It is preferable to move the check to the gateway and avoid 
SLOAD checks at runtime. For example, **staticSwapFeeEstimate** is checked in 
`_estimateExchangeFee()` and `exchangeFromExactBase()`, but it’s only set at 
`setMarketPricingParams()`.
