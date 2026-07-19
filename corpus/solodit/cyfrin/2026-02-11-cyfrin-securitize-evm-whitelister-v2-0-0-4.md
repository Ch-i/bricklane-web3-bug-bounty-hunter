---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-11-cyfrin-securitize-evm-whitelister-v2-0-0-4
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
title: '`PermissionFlags::and` function will encode the permission for `SWAP_ALLOWED`
  AND `LIQUIDITY_ALLOWED` as if the account would have `NONE` permissions'
vuln_class: []
---

# `PermissionFlags::and` function will encode the permission for `SWAP_ALLOWED` AND `LIQUIDITY_ALLOWED` as if the account would have `NONE` permissions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md)_

---

**Description:** Using `PermissionFlags::and` function to compute the combined permission for an account expecting to enforce that the account must have BOTH permissions incorrectly encodes the bits corresponding to the `NONE` permission.

```
`SWAP_ALLOWED` & `LIQUIDITY_ALLOWED` => `NONE`
0x0001 & 0x0002 => 0x0000
```

**Recommended Mitigation:** Taking into consideration the recommendation to fix issue [*`PermissionFlags::hasFlag` incorrectly grants `ALL_PERMISSIONS` to `PermissionFlag::LIQUIDITY_ALLOWED` and `PermissionFlag::SWAP_ALLOWED` *](#permissionflagshasflag-incorrectly-grants-allpermissions-to-permissionflagliquidityallowed-and-permissionflagswapallowed-) . Consider avoiding `and` when combining flags to assign permissions to an account. Instead, if the wanted result is to verify if an account has both permissions, then do it as follows:
```solidity
    function test_hasFlag_LIQUIDITY_or_SWAP() public pure {
        PermissionFlag p = PermissionFlags.LIQUIDITY_ALLOWED | PermissionFlags.SWAP_ALLOWED;
        // 0x0002          | 0x0001           = 0x0003
        assertTrue(_has(p, p));        // "Does the permission set p contain ALL the bits that are set in p?"
    }
```
So when we call `p.hasFlag(p)`:
- `permissions = p = 0x0003`
- `flag       = p = 0x0003`

Compute:
```
(permissions & flag) == flag
(0x0003 & 0x0003)    == 0x0003
0x0003               == 0x0003   → true!
```

**Securitize:** Remove this functionality in commit [0b8d506](https://github.com/securitize-io/bc-allowlist-checker-sc/commit/0b8d5061582f9dcac3b3eb2e24d37aba1de5e5bf) as it was not being used.

**Cyfrin:** Verified.
