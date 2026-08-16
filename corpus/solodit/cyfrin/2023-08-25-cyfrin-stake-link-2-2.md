---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-08-25-cyfrin-stake-link-2-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-08-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-08-25-cyfrin-stake-link.md
tags:
- firm:cyfrin
- report:2023-08-25-cyfrin-stake-link
title: Functions not used internally could be marked external
vuln_class: []
---

# Functions not used internally could be marked external

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-08-25-cyfrin-stake-link.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-08-25-cyfrin-stake-link.md)_

---

```solidity
File: PriorityPool.sol

89:     function initialize(

278:     function depositQueuedTokens() public {

```

**Client:**
Acknowledged.

**Cyfrin:** Acknowledged.
