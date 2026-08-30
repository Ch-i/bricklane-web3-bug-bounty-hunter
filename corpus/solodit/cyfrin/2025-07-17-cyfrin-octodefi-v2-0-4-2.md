---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-4-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-17T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-17-cyfrin-octodefi-v2-0
title: Array length used in multiple loop iterations can be cached
vuln_class: []
---

# Array length used in multiple loop iterations can be cached

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-17-cyfrin-octodefi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md)_

---

**Description:** When validating strategy steps, the length is retrieved for each loop iteration when it could instead be cached to save gas:

```solidity
function _validateSteps(StrategyStep[] memory steps) internal pure {
    for (uint256 i = 0; i < steps.length; i++) {
        _validateStep(steps[i], steps.length);
    }
}
```

**OctoDeFi:** Fixed in PR [\#23](https://github.com/octodefi/strategy-builder-plugin/pull/23).

**Cyfrin:** Verified. The length is now cached.

\clearpage
