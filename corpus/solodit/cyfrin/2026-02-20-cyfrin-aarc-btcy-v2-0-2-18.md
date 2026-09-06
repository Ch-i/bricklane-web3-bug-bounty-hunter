---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-18
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Enforce `BTCY` vault decimals greater or equal to underlying token decimals
vuln_class: []
---

# Enforce `BTCY` vault decimals greater or equal to underlying token decimals

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** For `ERC4626` vaults it is good defensive practice to enforce at initialization that the vault's decimals are greater than or equal to the underlying token decimals:
```diff
    function initialize(IIBTCY _ibtcy, address _admin) public initializer {
        require(_admin != address(0), ZeroAddress());

        __ERC20_init("BTCY Vault", "BTCY");
        __ERC4626_init(IERC20(address(_ibtcy)));
+       require(_ibtcy.decimals() <= decimals(), AssetDecimalsTooHigh());
        __AccessControlEnumerable_init();
        __UUPSUpgradeable_init();

        // Grant roles to admin
        _grantRole(DEFAULT_ADMIN_ROLE, _admin);
        _grantRole(PAUSER_ROLE, _admin);
        _grantRole(UPGRADER_ROLE, _admin);
        __AllowList_init(_admin);
    }
```

**Aarc:** Fixed in commit [52a5f99](https://github.com/aarc-xyz/btcy-contracts-main/commit/52a5f99831d2343ac7e4c67c34eb81433e0a838f).

**Cyfrin:** Verified.
