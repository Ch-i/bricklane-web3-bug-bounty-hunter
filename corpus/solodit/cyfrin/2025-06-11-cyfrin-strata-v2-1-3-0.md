---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-3-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: Use named mappings to explicitly denote the purpose of keys and values
vuln_class: []
---

# Use named mappings to explicitly denote the purpose of keys and values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** Use named mappings to explicitly denote the purpose of keys and values:
```solidity
predeposit/MetaVault.sol
23:    // Track the assets in the mapping for easier access
24:    mapping(address => TAsset) public assetsMap;

predeposit/pUSDeDepositor.sol
35:    mapping (address => TAutoSwap) autoSwaps;

test/MockStakedUSDe.sol
20:  mapping(address => UserCooldown) public cooldowns;
```

**Strata:** Fixed in commit [ab231d9](https://github.com/Strata-Money/contracts/commit/ab231d99e4ba6c7c82c4928515775a39dc008808).

**Cyfrin:** Verified.
