---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-11-cyfrin-securitize-evm-whitelister-v2-0-0-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-02-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-11-cyfrin-securitize-evm-whitelister-v2-0
title: '`PermissionFlags::hasFlag` can''t be used to check for `PermissionFlag::NONE`'
vuln_class: []
---

# `PermissionFlags::hasFlag` can't be used to check for `PermissionFlag::NONE`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md)_

---

**Description:** `PermissionFlags.sol` defines some operator functions, constants and a `hasFlag` function; examining these last two:
```solidity
    PermissionFlag constant NONE = PermissionFlag.wrap(0x0000);
    PermissionFlag constant SWAP_ALLOWED = PermissionFlag.wrap(0x0001);
    PermissionFlag constant LIQUIDITY_ALLOWED = PermissionFlag.wrap(0x0002);
    PermissionFlag constant ALL_ALLOWED = PermissionFlag.wrap(0xFFFF);

    function hasFlag(PermissionFlag permissions, PermissionFlag flag) internal pure returns (bool) {
        return PermissionFlag.unwrap(and(permissions, flag)) != 0;
    }
```

One side-effect of this implementation is that `hasFlag(ANY_VALUE, PermissionFlags.NONE)` always returns `false` since:
```solidity
hasFlag(ANY_VALUE, PermissionFlags.NONE)
// return ANY_VALUE & 0x0000 = 0x0000
// return 0x0000 != 0 → false
```

**Recommended Mitigation:** * Add a separate function in `PermissionFlags` to check this using direct equality:
```solidity
function hasNoPermissions(PermissionFlag permissions) internal pure returns (bool) {
    return permissions == NONE;
}
```

* Revert in `hasFlag` if the input `flag` is `NONE` to prevent this erroneous use case:
```diff
+ error InvalidFlagCheck();

function hasFlag(PermissionFlag permissions, PermissionFlag flag) internal pure returns (bool) {
+   if (flag == NONE) revert InvalidFlagCheck();
    return PermissionFlag.unwrap(and(permissions, flag)) != 0;
}
```

**Securitize:** Remove this functionality in commit [0b8d506](https://github.com/securitize-io/bc-allowlist-checker-sc/commit/0b8d5061582f9dcac3b3eb2e24d37aba1de5e5bf) as it was not being used.

**Cyfrin:** Verified.
