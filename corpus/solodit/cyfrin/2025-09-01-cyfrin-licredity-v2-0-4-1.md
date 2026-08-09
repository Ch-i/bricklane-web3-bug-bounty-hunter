---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-4-1
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
title: Missing array length check
vuln_class: []
---

# Missing array length check

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-licredity-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md)_

---

**Description:** The `ChainlinkOracle::quoteFungibles` function assumes that the `fungibles` and `amounts` arrays passed as arguments are of equal length. It iterates over `fungibles.length` and accesses `amounts[i]` for each index. If `amounts.length` is less than `fungibles.length`, the function will try to read out-of-bounds memory, leading to a revert. If `amounts.length` is greater than `fungibles.length`, the extra values in `amounts` will be ignored.

**Impact:** If `amounts.length < fungibles.length`, the function will revert with an out-of-bounds error, causing the transaction to fail. This can lead to unexpected reverts and denial of service for users or contracts interacting with this function. The lack of input validation may also make the contract harder to use correctly and more error-prone for integrators.

**Recommended Mitigation:** Add an explicit check at the start of the function to ensure that `fungibles.length == amounts.length`. Revert with a clear error message if the lengths do not match. For example:

```solidity
require(fungibles.length == amounts.length, "Input length mismatch");
```

**Licredity:** Fixed in [PR#60](https://github.com/Licredity/licredity-v1-core/pull/60/files), commit [`a5ba70b`](https://github.com/Licredity/licredity-v1-core/commit/a5ba70b56f987de11694d0414b79319445ea11e8)

**Cyfrin:** Verified. NatSpec updated.
