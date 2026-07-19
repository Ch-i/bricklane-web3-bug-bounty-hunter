---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-10-cyfrin-thermae-4-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-01-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md
tags:
- firm:cyfrin
- report:2024-01-10-cyfrin-thermae
title: Don't initialize variables with default value
vuln_class: []
---

# Don't initialize variables with default value

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-10-cyfrin-thermae.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md)_

---

**Description:** Don't initialize variables with default value, eg in `TickMath::getTickAtSqrtRatio()`:

```solidity
uint256 msb = 0;
```

**Impact:** Gas optimization.

**Wormhole:**
`TickMath` is no longer used as on chain slippage calculations are not being done anymore.
