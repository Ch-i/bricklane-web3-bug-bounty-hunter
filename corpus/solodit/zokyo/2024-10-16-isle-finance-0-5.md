---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-16-isle-finance-0-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-10-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md
tags:
- firm:zokyo
- report:2024-10-16-isle-finance
title: Governable is an abstract upgradeable contract but doesn’t contain any storage
  gaps which could result in collisions on upgrade
vuln_class: []
---

# Governable is an abstract upgradeable contract but doesn’t contain any storage gaps which could result in collisions on upgrade

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-10-16-Isle Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Location**: Governable.sol

**Description**: 

The Governable.sol contract is a part of the Receivable and IsleGlobals contracts. For Upgradeable contracts, there must be a storage gap in order to freely add new state variables in future versions without compromising the integrity of the storage compatibility. The absence of storage gaps can result in the overwriting of variables in the child contract if new variables are added to the Goverenable contract. 

**Recommendation**

It’s recommended that storage gaps are added to the Governable contract in order to avoid risk of storage collisions.

**Fix**:  Client addressed and fixed the issue at commit  0a7741f  .
