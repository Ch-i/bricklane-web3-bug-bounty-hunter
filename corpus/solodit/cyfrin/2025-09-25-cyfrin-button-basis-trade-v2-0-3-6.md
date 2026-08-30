---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-3-6
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-09-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-25-cyfrin-button-basis-trade-v2-0
title: Missing SPDX License Identifiers
vuln_class: []
---

# Missing SPDX License Identifiers

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-25-cyfrin-button-basis-trade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md)_

---

**Description:** All Solidity source files are missing an SPDX license identifier. Add a license header at the very top of each file to clarify licensing and silence tooling warnings (Solc/linters/CI):

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;
```

Without this, some tools treat files as unlicensed or emit warnings, which can hinder downstream reuse and compliance.

**Button:** Acknowledged. Have not decided our licensing yet, but will add these headers before we make the repo public.
