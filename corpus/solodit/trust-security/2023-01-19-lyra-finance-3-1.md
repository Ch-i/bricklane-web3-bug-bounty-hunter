---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-3-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: Improve future-proofing by explicitly matching types
vuln_class: []
---

# Improve future-proofing by explicitly matching types

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

There are some instances in the code base where a long if/else clause ends with an else that 
assumes the enum value is the remaining value after matching all other options. This pattern 
is prone to future errors as additional types are added, and the existing code would not throw 
any warnings but behave incorrectly. For example, in `_updateExposure()` the last else clause 
catches OptionType.SHORT_PUT_QUOTE, but if new options are added this would introduce 
a bug.
