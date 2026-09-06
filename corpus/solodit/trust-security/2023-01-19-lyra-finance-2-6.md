---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-2-6
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-L-8 Owner can drain liquidity pool instantly
vuln_class: []
---

# TRST-L-8 Owner can drain liquidity pool instantly

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:** 
In LiquidityPool, `transferQuoteToHedge()` allows the defined poolHedger to pull up to the 
entire available liquidity. Since poolHedger can be set instantly using `setPoolHedger()`, it 
represents significant damage potential. The recommendation is to impose a timelock, either 
at the contract level or at the owner level (time-locked governance contract).
