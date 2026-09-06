---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-02-06-zunami-protocolv2-3-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-02-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md
tags:
- firm:oxorio
- report:2024-02-06-zunami-protocolv2
title: '[ACKNOWLEDGED] Floating pragma'
vuln_class: []
---

# [ACKNOWLEDGED] Floating pragma

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-02-06-Zunami ProtocolV2.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md)_

---

##### Description
All contracts across the codebase use the following pragma statement:
```solidity
pragma solidity ^0.8.22;
```
Contracts should be deployed with the same compiler version and flags used during development and testing. An outdated pragma version might introduce bugs that affect the contract system negatively or recent compiler versions may have unknown security vulnerabilities.
##### Recommendation
We recommend locking the pragma to a specific version of the compiler.
