---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-29-liberty-finance-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-29-Liberty%20Finance.md
tags:
- firm:zokyo
- report:2024-10-29-liberty-finance
title: Upgradeable ERC20 token
vuln_class: []
---

# Upgradeable ERC20 token

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-10-29-Liberty Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-29-Liberty%20Finance.md)_

---

**Severity**: Informational

**Status**: Acknowledged

**Description**

Contract LibertyFinanceToken is an ERC20 token that is upgradeable as well. It is generally not advised to make an ERC20 token upgradeable as it becomes unpredictable for token holders regarding their token shares and poses a centralization risk.

**Recommendation**: 

Consider not upgrading the ERC20 contract unless required by DAO/Governance and use multi-sig wallet for upgrades.
