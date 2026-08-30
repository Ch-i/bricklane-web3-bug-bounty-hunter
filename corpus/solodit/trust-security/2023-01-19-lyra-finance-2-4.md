---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-2-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-L-5 Slippage in hedger may be double what is set in slippage parameter
vuln_class: []
---

# TRST-L-5 Slippage in hedger may be double what is set in slippage parameter

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:** 
`_decreasePosition()` in GMXFuturesPoolHedger calls the GMX `createDecreasePosition()` entry 
point, passing **minOut** = 0. According to docs, 0 should only be used if there are no swaps. But 
in the case of a long position, there is a swap (base to quote). The swap direction has the same 
exposure to base/quote as position decrease exposure. This means the slippage is applied 
twice. Therefore, acceptableSpotSlippage needs to be set to half of the intended slippage. 
Similar situation for createIncreasePosition, again with double the exposure. 

**Recommended mitigation:**
Make sure acceptableSpotSlippage is set so that the protocol is satisfied with losing the 
slippage amount twice per cycle.

**Team response:**
Acknowledged.
