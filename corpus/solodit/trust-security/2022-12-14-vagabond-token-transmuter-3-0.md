---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-14-vagabond-token-transmuter-3-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2022-12-14T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md
tags:
- firm:trust-security
- report:2022-12-14-vagabond-token-transmuter
title: Immutable-only variables
vuln_class: []
---

# Immutable-only variables

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2022-12-14-Vagabond Token Transmuter.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md)_

---

The contract currently makes use of two immutable variables. However, there are several 
more variables which do not change throughout the lifetime of the contract. It is very 
advisable to make them immutable as it saves gas and protects against future errors.
