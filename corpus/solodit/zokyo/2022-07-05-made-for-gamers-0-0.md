---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-07-05-made-for-gamers-0-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-07-05T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-05-Made%20for%20gamers.md
tags:
- firm:zokyo
- report:2022-07-05-made-for-gamers
title: Anyone is able to upgrade implementation of the contract.
vuln_class: []
---

# Anyone is able to upgrade implementation of the contract.

_Section severity (from Solodit section header): Critical_  
_Audit firm: Zokyo_  
_Source report: [2022-07-05-Made for gamers.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-05-Made%20for%20gamers.md)_

---

**Description**

EXPO.sol and EXPOVO.sol: function_authorizeUpgrade(). Function_authorizeUpgrade() is necessary in order to authorize that upgrading implementation is valid, thus this function should always be implemented and check that msg.sender of upgradeTo() function is valid(Either owner, admin or authorized user).

**Recommendation**

Validate msg.sender in_authorizeUpgrade(). For example, onlyOwner modifier from OZ OwnableUpgradeable can be used.

**Re-audit comment**

Resolved.

Post-audit:

OnlyOwner modifier is used and scenario was also covered with additional unit-tests.
