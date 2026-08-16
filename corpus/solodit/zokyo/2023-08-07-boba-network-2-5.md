---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-08-07-boba-network-2-5
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-08-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba%20Network.md
tags:
- firm:zokyo
- report:2023-08-07-boba-network
title: SafeMath Not Needed
vuln_class: []
---

# SafeMath Not Needed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-08-07-Boba Network.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba%20Network.md)_

---

**Description**

In the contract, 'Teleportation.sol', the codebase uses SafeMath. This causes unnecessary overflow and underflow checks that are reverted by default. By removing this library and using built in arithmetic, users can save gas for not unnecessary checks.

**Recommendation**

We recommend removing SafeMath as the compiler version is above 0.8.0.

**Re-audit comment**

Resolved
