---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-3-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Missing zero address validation in `BoostedIncentiveLogic`
vuln_class: []
---

# Missing zero address validation in `BoostedIncentiveLogic`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** Unlike in the `BaseIncentiveLogic` constructor, `BoostedIncentiveLogic` fails to validate `_boostingPowerAdaptor` against the zero address which could result in Dos if erroneously configured in this way.

**Recommended Mitigation:**
```diff
    constructor(address _incentiveManager, uint256 _defaultFee, address _boostingPowerAdaptor)
        BaseIncentiveLogic(_incentiveManager, _defaultFee)
    {
++      if (_boostingPowerAdaptor == address(0)) revert();
        boostingPowerAdaptor = IBoostingPowerAdapter(_boostingPowerAdaptor);
    }
```

**Paladin:** Fixed by commit [`c3ee9d5`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/c3ee9d5bf57ccc0b479d2604f4725cd0fb604c57).

**Cyfrin:** Verified. The constructor argument is now validated against the zero address.
