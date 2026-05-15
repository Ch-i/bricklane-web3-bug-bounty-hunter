---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-2-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Incorrect operator when validating subsidisation cap
vuln_class: []
---

# Incorrect operator when validating subsidisation cap

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** When a new registration is created, `Ignite::_registerWithChecks` [validates](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L925-L928) that the subsidisation amount for the registration does not cause the maximum to be exceeded when added to the existing total subsidised amount:

```solidity
require(
    totalSubsidisedAmount + subsidisationAmount < maximumSubsidisationAmount,
    "Subsidisation cap exceeded"
);
```

However, the incorrect operator is used when performing this comparison.

**Impact:** Registrations that cause the maximum subsidization amount to be met exactly will revert.

**Recommended Mitigation:**
```diff
    require(
-       totalSubsidisedAmount + subsidisationAmount < maximumSubsidisationAmount,
+       totalSubsidisedAmount + subsidisationAmount <= maximumSubsidisationAmount,
        "Subsidisation cap exceeded"
    );
```

**BENQI:** Fixed in commit [37446f6](https://github.com/Benqi-fi/ignite-contracts/pull/16/commits/37446f681d9f09000bb22682a9a153a0c7b23548).

**Cyfrin:** Verified. The operator has been changed.
