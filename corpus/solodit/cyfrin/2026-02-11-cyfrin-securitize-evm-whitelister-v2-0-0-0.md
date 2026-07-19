---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-11-cyfrin-securitize-evm-whitelister-v2-0-0-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-02-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-11-cyfrin-securitize-evm-whitelister-v2-0
title: Incorrect pragma as support for defining operators on user-defined value types
  was added in Solidity 0.8.19
vuln_class: []
---

# Incorrect pragma as support for defining operators on user-defined value types was added in Solidity 0.8.19

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md)_

---

**Description:** These files have the following pragma:
* `contracts/uniswap/permissionedPools/libraries/PermissionFlags.sol`
* `contracts/uniswap/permissionedPools/BaseAllowListChecker.sol`
```solidity
pragma solidity ^0.8.0;
```

However this is incorrect as support for defining operators on user-defined value types was [added](https://www.soliditylang.org/blog/2023/02/22/user-defined-operators/) in Solidity 0.8.19.

**Recommended Mitigation:** Use the correct pragma:
```diff
- pragma solidity ^0.8.0;
+ pragma solidity ^0.8.19;
```

**Securitize:** Fixed in commit [f938341](https://github.com/securitize-io/bc-allowlist-checker-sc/commit/f9383415cfab4a1de5372212cd131ef0d1b9fb22) by using 0.8.22 consistent with the other contracts.

**Cyfrin:** Verified.
