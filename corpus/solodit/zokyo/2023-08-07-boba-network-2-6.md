---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-08-07-boba-network-2-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-08-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba%20Network.md
tags:
- firm:zokyo
- report:2023-08-07-boba-network
title: '`sourceChainId` Can Be Converted to Save One Slot'
vuln_class: []
---

# `sourceChainId` Can Be Converted to Save One Slot

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-08-07-Boba Network.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba%20Network.md)_

---

**Description**

In the contract, Teleportation.sol', the variable 'sourceChainId can be converted to save gas. 'sourceChainId may benefit from being reduced from uint256 to smaller size such as uint32. By changing sourceChainId', the slot size will be lowered by one.

**Recommendation**

If converting 'sourceChainId to uint32 is within the protocol specification, then we recommend making this change.

**Re-audit comment**

Resolved
