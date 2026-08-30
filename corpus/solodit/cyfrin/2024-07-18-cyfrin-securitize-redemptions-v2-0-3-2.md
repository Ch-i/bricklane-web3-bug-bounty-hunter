---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-3-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-07-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-18-cyfrin-securitize-redemptions-v2-0
title: Bad practice to have multiple initializers
vuln_class: []
---

# Bad practice to have multiple initializers

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-18-cyfrin-securitize-redemptions-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md)_

---

**Description:** We found that the contract `SecuritizeSwap` has two functions named `initialize()`.
Both functions are public and behind the modifier `initializer` and `forceInitializeFromProxy` and the main initializer (assuming the test suite shows the typical usecase) is the function with four params and it calls the other one.
This is not a good practice and we strongly recommend fix it.
We recommend changing the `initialize()` function with three parameters into an internal function with a proper name (maybe `_initialize()`) and the modifiers to be applied to only the main public initializer.

**Securitize:** Fixed in commit [b09460](https://bitbucket.org/securitize_dev/securitize-swap/commits/b094604b341123a49c8abbd6e1c3d53d7c102f28)

**Cyfrin:** Verified.
