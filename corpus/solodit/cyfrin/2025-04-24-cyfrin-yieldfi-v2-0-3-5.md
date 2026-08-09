---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-3-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: Lack of `_disableInitializers` in upgradeable contracts
vuln_class: []
---

# Lack of `_disableInitializers` in upgradeable contracts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** YieldFi utilizes upgradeable contracts. It's [best practice](https://docs.openzeppelin.com/upgrades-plugins/writing-upgradeable#initializing_the_implementation_contract) to disable the ability to initialize the implementation contracts.

Consider adding a constructor with the OpenZeppelin `_disableInitializers` in all the upgradeable contracts:
```solidity
constructor() {
    _disableInitializers();
}
```

**YieldFi:** Fixed in commit [`584b268`](https://github.com/YieldFiLabs/contracts/commit/584b268a75a8f7c7f10eda46efaaa3ebbe4f0159)

**Cyfrin:** Verified. Constructor with `_disableInitializers` added to all upgradeable contracts.
