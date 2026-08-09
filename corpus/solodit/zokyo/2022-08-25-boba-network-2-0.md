---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-08-25-boba-network-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-08-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-08-25-Boba%20Network.md
tags:
- firm:zokyo
- report:2022-08-25-boba-network
title: Unused function parameters in EthBridge.
vuln_class: []
---

# Unused function parameters in EthBridge.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-08-25-Boba Network.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-08-25-Boba%20Network.md)_

---

**Description**

In contract EthBridge.sol, at lines 126 and 127, variables_srcAddress and_nonce are not being used throughout the function.

**Recommendation**

Make sure the variables are not actually needed and remove them.

**Re-audit comment**

Acknowledged
