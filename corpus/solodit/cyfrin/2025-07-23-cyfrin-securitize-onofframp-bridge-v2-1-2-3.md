---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-2-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Missing storage gap on upgradeable base contracts
vuln_class: []
---

# Missing storage gap on upgradeable base contracts

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** The contract `/contracts/utils/BaseContract` of `bc-securitize-bridge-sc` repository is upgradeable (inherits from `UUPSUpgradeable`, `OwnableUpgradeable`, and `PausableUpgradeable`) but does not include a storage gap.

Storage gaps are essential for ensuring that new state variables can be added to the base contracts in future upgrades without affecting the storage layout of inheriting child contracts.

**Impact:** Any addition of new state variables in future versions of `BaseContract` can lead to storage collisions in the children contracts.

**Recommendation:**
Add a storage gap to the `BaseContract`.
```solidity
uint256[50] private __gap;
```

**Securitize:** Fixed in commit [1da35c](https://bitbucket.org/securitize_dev/bc-securitize-bridge-sc/commits/1da35cde31a53e7b2de56de0d313ebdcb80cbfa3).

**Cyfrin:** Verified.
