---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Upgradeable contracts don't call `disableInitializers`
vuln_class: []
---

# Upgradeable contracts don't call `disableInitializers`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** The codebase has a number of upgradeable contracts which use OpenZeppelin Initializable but don't have a constructor which calls `_disableInitializers` per the OpenZeppelin documentation [[1](https://docs.openzeppelin.com/contracts/4.x/api/proxy#Initializable-_disableInitializers--), [2](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#initializing_the_implementation_contract)].

**Impact:** Contract implementations could be initialized when this should not be possible.

**Recommended Mitigation:** All upgradeable contracts should have a constructor like this:
```solidity
/// @custom:oz-upgrades-unsafe-allow constructor
constructor() {
    _disableInitializers();
}
```

**Beefy:**
Fixed in commit [4009179](https://github.com/beefyfinance/experiments/commit/4009179059190b782c63d022d310d14cb18f7781).

**Cyfrin:** Verified.
