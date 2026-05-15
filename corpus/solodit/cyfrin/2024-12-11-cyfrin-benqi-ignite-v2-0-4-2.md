---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-4-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Unnecessary conditional block in `Ignite::getTotalRegistrations` can removed
vuln_class: []
---

# Unnecessary conditional block in `Ignite::getTotalRegistrations` can removed

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** The conditional in [`Ignite::getTotalRegistrations`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L483-L494) is intended to handle the case where there are no registrations aside from the default placeholder registration; however, this is unnecessary because the function would still return `0` without this check if the `registrations.length` is `1`, and due to the presence of the default placeholder registration, it should not be possible to reach a state where `registrations.length` is `0`.

```solidity
function getTotalRegistrations() external view returns (uint) {
    if (registrations.length <= 1) {
        return 0;
    }

    // Subtract 1 because the first registration is a dummy registration
    return registrations.length - 1;
}
```

**Recommended Mitigation:** Consider removing the conditional block.

**BENQI:** Fixed in commit [58af671](https://github.com/Benqi-fi/ignite-contracts/pull/16/commits/58af6717bb96410e364f3da3f57a85e7577cac36).

**Cyfrin:** Verified. Validation has been removed.
