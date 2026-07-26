---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-08-25-boba-network-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2022-08-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-08-25-Boba%20Network.md
tags:
- firm:zokyo
- report:2022-08-25-boba-network
title: Pragma version lock
vuln_class: []
---

# Pragma version lock

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2022-08-25-Boba Network.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-08-25-Boba%20Network.md)_

---

**Description**

It's recommended to have the same compiler version that the contracts were tested with the most. This way it reduces the risk of introducing unknown bugs. There are also different versions used throughout the project, for example ^0.8.0 in LzApp.sol and ^0.8.9 in EthBridge.sol.

**Recommendation**

Lock pragma versions.

**Re-audit comment**

Acknowledged
