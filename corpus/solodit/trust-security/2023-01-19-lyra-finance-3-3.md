---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-3-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: Redundant event parameters
vuln_class: []
---

# Redundant event parameters

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

Some events have unuseful parameters. For example, in `cancelPendingOrder()`, the event 
OrderCanceled can only be emitted if **success** is true (otherwise the transaction would revert).
