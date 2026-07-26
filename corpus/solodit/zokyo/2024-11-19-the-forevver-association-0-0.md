---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-11-19-the-forevver-association-0-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-11-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-19-The%20Forevver%20Association.md
tags:
- firm:zokyo
- report:2024-11-19-the-forevver-association
title: Addresses Should Not Be Hardcoded
vuln_class: []
---

# Addresses Should Not Be Hardcoded

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-11-19-The Forevver Association.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-19-The%20Forevver%20Association.md)_

---

**Severity** - Low

**Status** - Acknowledged

**Description**

In the Fias2.sol addresses such as FOREVERR_MINTER and LITCRAFT_MINTER have been hardcoded , it is possible that on different chains the addresses corresponding to these roles are different and hence instead of hardcoding the addresses they should be assigned in the initializer.

**Recommendation**:

It is recommended that addresses should be assigned in the initializer instead of being hardcoded.

**Client comment**: 

no impact because we are only using this contract on ETH and not other chains with other Forevver/LitCraft/Admin addresses.
