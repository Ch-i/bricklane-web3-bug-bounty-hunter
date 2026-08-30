---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-4-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Unnecessary validation in `Ignite::getRegistrationsByAccount`
vuln_class: []
---

# Unnecessary validation in `Ignite::getRegistrationsByAccount`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** In [`Ignite::getRegistrationsByAccount`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L512-L536), there is [validation](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L526-L527) performed on the indices passed as arguments to the function:

```solidity
require(from < to, "From value must be lower than to value");
require(to <= numRegistrations, "To value must be at most equal to the number of registrations");
```

This is not necessary as the call will revert due to underflow [here](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L529) or index out-of-bounds [here](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L532). In the case `to == from`, an empty array would be returned.

**Recommended Mitigation:** Consider removing the validation shown above.

**BENQI:** Fixed in commit [82cf4fc](https://github.com/Benqi-fi/ignite-contracts/pull/16/commits/82cf4fc9f753339460e41bc240a572d89c6fd7a8).

**Cyfrin:** Verified. Validation has been removed.
