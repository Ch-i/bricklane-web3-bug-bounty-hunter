---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Centralized entities with excessive permissions
vuln_class: []
---

# Centralized entities with excessive permissions

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Medium

**Status**: Acknowledged

**Description**

The  setHandler function from Vester.sol and VesteNPL.sol contracts allows a governance to set a new handler address and activate or deactivate it. The entity with this privilege can e.g. claim users' reward for arbitrary address (claimForAccount), deposit his assets (depositForAccount) or influence the vesting reward calculations (settransferredCumulativeRewards). These abilities can significantly impact the protocol’s operation, potentially affecting its performance and outcomes.

**Recommendation**: 

Consider limiting the handler’s abilities.

Partially fixed: Protocol will add a timelock.
