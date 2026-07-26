---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-4-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: Unused Import of `OwnableUpgradeable` in `Accounting.sol`
vuln_class: []
---

# Unused Import of `OwnableUpgradeable` in `Accounting.sol`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** `OwnableUpgradeable` is imported but not used directly in this file.

**Recommended Mitigation:** Remove the unused import to improve code cleanliness:
```diff
- import { OwnableUpgradeable} from "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
```


**Strata:**
Fixed in commit [cfc5117b](https://github.com/Strata-Money/contracts-tranches/commit/cfc5117b07d639d95319153b82c299972dfdedd9).

**Cyfrin:** Verified.
