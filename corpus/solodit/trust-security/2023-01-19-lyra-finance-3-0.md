---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-3-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: 'Implement input validation when possible:'
vuln_class: []
---

# Implement input validation when possible:

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

It’s always worthwhile to check for potential run-time issues during assignment time. For 
example, it is clear that **priceVarianceCBPercent > gmxUsageThreshold** should always hold. 
Similarly, **maxLeverage > targetLeverage** must be true. It’s advisable to go through all 
parameter assignments and make sure insensible values are disallowed.
