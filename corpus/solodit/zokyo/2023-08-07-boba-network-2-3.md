---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-08-07-boba-network-2-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-08-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba%20Network.md
tags:
- firm:zokyo
- report:2023-08-07-boba-network
title: Lack of NatSpec in 'EntryPointWrapper.sol'
vuln_class: []
---

# Lack of NatSpec in 'EntryPointWrapper.sol'

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-08-07-Boba Network.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba%20Network.md)_

---

**Description**

In the contract, EntryPointWrapper.sol', the codebase lacks documentation that might be useful to developers. For example: documentation for structs such as 'FailOpStatus` might be useful for developers without having to guess the intended functionality.

**Recommendation**

We recommend that documentation is added throughout EntryPointWrapper.sol to ensure external reviewers and developers understand intended meaning.

**Re-audit comment**

Resolved
