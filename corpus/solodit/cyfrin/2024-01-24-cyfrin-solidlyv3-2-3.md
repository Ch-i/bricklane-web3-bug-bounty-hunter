---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-2-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md
tags:
- firm:cyfrin
- report:2024-01-24-cyfrin-solidlyv3
title: Functions not used internally could be marked external
vuln_class: []
---

# Functions not used internally could be marked external

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** Functions not used internally could be marked external:

```solidity
File: SolidlyV3Factory.sol

87:     function enableFeeAmount(uint24 fee, int24 tickSpacing) public override {

```

**Solidly:**
Acknowledged.
