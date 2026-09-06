---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-3-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-11-06T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-06-cyfrin-securitize-global-registry-v2-0
title: Remove redundant calls to `EnumerableSet::contains`
vuln_class: []
---

# Remove redundant calls to `EnumerableSet::contains`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-06-cyfrin-securitize-global-registry-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md)_

---

**Description:** `EnumerableSet::_add` and `_remove` already [call](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/structs/EnumerableSet.sol#L75) `_contains` (or perform similar logic), hence there is no need to call this prior to adding or removing elements in:
* `BlackListManager::_addToBlacklist, _removeFromBlacklist`

**Recommended Mitigation:** Call `EnumerableSet::add` or `remove` directly and revert if they return `false`.

**Securitize:** Fixed in commit [a878a41](https://github.com/securitize-io/dstoken/commit/a878a41be5769dc3282c8646f6d145946be7d5ff).

**Cyfrin:** Verified.
