---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-15-penguin-karts-3-7
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2022-03-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-15-Penguin%20Karts.md
tags:
- firm:zokyo
- report:2022-03-15-penguin-karts
title: Centralization risk
vuln_class: []
---

# Centralization risk

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-15-Penguin Karts.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-15-Penguin%20Karts.md)_

---

**Description**

Token.sol. Contract uses onlyOwner modifier to control access to admin’s functionality. In case
of losing access to the owner's address or sharing access with an unwanted person, admin
can lose access to admin’s functionality.

**Recommendation**:

Consider using multisig as an owner’s address.

**Post-audit**:

By the client, ownable functionality will be used single time after the listing
