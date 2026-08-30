---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-1-9
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: Centralized Control and Lack of Transparency
vuln_class: []
---

# Centralized Control and Lack of Transparency

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Severity**: Low

**Status**:  Unresolved

**Description**:

The presale contract contains functions (`emergencyWithdrawFunds`, `burnUnsoldTokens`, `setUsersDiscount`) that provide the owner with significant control over the contract's operation and token distribution. While necessary for administration and emergency situations, these functions could be misused or lead to centralization concerns.

**Scenario:**

The contract owner could withdraw tokens or funds unexpectedly, change discount rates arbitrarily, or burn unsold tokens in a manner that affects the presale outcome. Such actions could undermine trust in the presale process and potentially harm participants.

**Recommendation:**

Implement a multi-signature wallet or a decentralized autonomous organization (DAO) mechanism for critical functions, requiring consensus among multiple stakeholders.
