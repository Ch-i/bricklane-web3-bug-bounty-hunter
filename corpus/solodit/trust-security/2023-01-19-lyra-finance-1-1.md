---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-1-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-M-2 ShortCollateral settleOptions may fail due to insolvency settled out
  of loop
vuln_class: []
---

# TRST-M-2 ShortCollateral settleOptions may fail due to insolvency settled out of loop

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:**
settleOptions() loops over the input **positionIds** array and either sends proceeds to the user 
or consumes their collateral. If there’s any insolvency, it is appended to 
**baseInsolventAmount/quoteInsolventAmount**. Only after the settlement loop is the entire 
insolvent portion claimed from the liquidity pool. The issue is that delaying the insolvency 
collection may cause ShortCollateral to have insufficient funds to pay for user proceeds.

**Recommended Mitigation:**
Insert `_reclaimInsolvency()` call to the end of the for loop.

**Team Response:**
Not really an issue if insolvent positions are settled in a separate transaction prior to solvent 
positions. Keepers can easily handle this situation. As insolvent positions are very rare (0 in all 
of the 6 months of the Avalon release) no changes to this logic seem appropriate.
