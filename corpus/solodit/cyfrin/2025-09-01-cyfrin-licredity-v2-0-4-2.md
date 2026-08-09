---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-4-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-licredity-v2-0
title: Missing valid bounds check in clamp
vuln_class: []
---

# Missing valid bounds check in clamp

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-licredity-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md)_

---

**Description:** The `FixedPointMath::clamp` function is intended to bound `x` between `minValue` and `maxValue`. However, if `minValue > maxValue`, the assembly logic first sets `z = max(x, minValue)` (which will be at least `minValue`), then caps `z` at `maxValue`. This means the function will always return `maxValue`, regardless of the input `x`. There is no revert or warning if the bounds are invalid, so the function silently assumes `minValue <= maxValue`.

**Impact:** If called with invalid bounds (`minValue > maxValue`), the function will not behave as expected and will always return `maxValue`. This can lead to subtle bugs or incorrect logic in contracts relying on proper clamping, potentially causing unexpected values to propagate through the system. The lack of input validation makes it harder to detect and debug such issues.

**Recommended Mitigation:** Add an explicit check at the start of the function to ensure that `minValue <= maxValue`. If not, revert with a clear error message. For example:

```solidity
require(minValue <= maxValue, "FixedPointMath: minValue > maxValue");
```

This ensures the function only operates on valid bounds and prevents silent errors.

Alternatively, document that `clamp` expects bounds to be correct and does not perform a check.

**Licredity:** FIxed in [PR#17](https://github.com/Licredity/licredity-v1-oracle/pull/17/files), commit [`4394467`](https://github.com/Licredity/licredity-v1-oracle/commit/43944676b458a95df19461298b5c3507a7a43055)

**Cyfrin:** Verified. Check omitted due to gas saving but the nuance documented in natspec.
