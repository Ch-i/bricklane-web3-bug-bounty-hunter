---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Use named mapping parameters to explicitly note the purpose of keys and values
vuln_class: []
---

# Use named mapping parameters to explicitly note the purpose of keys and values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** Use named mapping parameters to explicitly note the purpose of keys and values:
* `Issuance`:
```solidity
vault/StakingVault.sol
37:    mapping(address => UserCooldown) cooldowns;

helpers/Blacklistable.sol
8:    mapping(address => bool) internal _blacklisted;

helpers/Whitelist.sol
6:    /// @notice A mapping of specific user addresses that are allowed to bypass SBT checks
8:    mapping(address => bool) public manualWhitelist;
```

* `Deposit-Registry`:
```solidity
CompliantDepositRegistry.sol
21:    mapping(address => uint) public investorDepositMap;
```

**Syntetika:**
Fixed in commit [6f77988](https://github.com/SyntetikaLabs/monorepo/commit/6f779887cb2ab813c2d15dbc9cca7991a7301367).

**Cyfrin:** Verified.
