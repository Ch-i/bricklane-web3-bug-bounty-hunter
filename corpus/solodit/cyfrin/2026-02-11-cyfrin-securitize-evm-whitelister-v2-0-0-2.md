---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-11-cyfrin-securitize-evm-whitelister-v2-0-0-2
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
title: '`PermissionFlags::hasFlag` incorrectly grants `ALL_PERMISSIONS` to `PermissionFlag::LIQUIDITY_ALLOWED`
  and `PermissionFlag::SWAP_ALLOWED`'
vuln_class: []
---

# `PermissionFlags::hasFlag` incorrectly grants `ALL_PERMISSIONS` to `PermissionFlag::LIQUIDITY_ALLOWED` and `PermissionFlag::SWAP_ALLOWED`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md)_

---

**Description:** `PermissionFlags::hasFlag` returns true when checking the flag `LIQUIDITY_ALLOWED` against the flag `ALL_ALLOWED`; This means, when checking if an account allowed ONLY to add liquidity has permissions to do any operation (ALL_ALLOWED), `PermissionFlags::hasFlag` would incorrectly signal that the account indeed has permissions to do any operation.
- The same affects the `SWAP_ALLOWED` flag.
- The same affects validating the combination of `SWAP_ALLOWED` or `LIQUIDITY_ALLOWED`, `hasFlag` signals this combination as if it would be the `ALL_ALLOWED` flag.

**Impact:** Accounts flagged only to add liquidity or do swaps would receive ALL permissions, allowing them to perform operations they should not be allowed to.

**Proof of Concept:**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import {PermissionFlag, PermissionFlags} from "../../contracts/uniswap/permissionedPools/libraries/PermissionFlags.sol";

contract PermissionFlagsTest is Test {
    using PermissionFlags for PermissionFlag;

    // Helper to make tests more readable
    function _has(PermissionFlag permissions, PermissionFlag flag) internal pure returns (bool) {
        return permissions.hasFlag(flag);
    }

    function test_hasFlag_SWAP_ALLOWED() public pure {
        PermissionFlag p = PermissionFlags.SWAP_ALLOWED;
        // assertFalse(_has(p, PermissionFlags.NONE));
        // assertTrue(_has(p, PermissionFlags.SWAP_ALLOWED));
        // assertFalse(_has(p, PermissionFlags.LIQUIDITY_ALLOWED));

        //@audit-issue => SWAP_ALLOWED flag is given ALL_ALLOWED permissions!
        assertTrue(_has(p, PermissionFlags.ALL_ALLOWED)); // single flag != ALL
    }

    function test_hasFlag_LIQUIDITY_ALLOWED() public pure {
        PermissionFlag p;

        p = PermissionFlags.LIQUIDITY_ALLOWED;
        // assertFalse(_has(p, PermissionFlags.NONE));
        // assertFalse(_has(p, PermissionFlags.SWAP_ALLOWED));
        // assertTrue(_has(p, PermissionFlags.LIQUIDITY_ALLOWED));

        //@audit-issue => LIQUIDITY_ALLOWED flag is given ALL_ALLOWED permissions!
        assertTrue(_has(p, PermissionFlags.ALL_ALLOWED));
    }

    // Combined Flags //
    function test_hasFlag_SWAP_or_LIQUIDITY() public pure {
        PermissionFlag p = PermissionFlags.SWAP_ALLOWED | PermissionFlags.LIQUIDITY_ALLOWED;
        assertFalse(_has(p, PermissionFlags.NONE));
        assertTrue(_has(p, PermissionFlags.SWAP_ALLOWED));
        assertTrue(_has(p, PermissionFlags.LIQUIDITY_ALLOWED));

        //@audit-issue => returns true as if it had ALL_ALLOWED permissions
        assertTrue_has(p, PermissionFlags.ALL_ALLOWED));

    }
}
```

**Recommended Mitigation:** Consider refactoring the `hasFlag` function as follows:
```solidity
    function hasFlag(PermissionFlag permissions, PermissionFlag flag) internal pure returns (bool) {
        if (PermissionFlag.unwrap(flag) == 0) return false;

        return and(permissions, flag) == flag;
    }
}
```

The fix accounts for the case when the provided flag is `NONE`, and also correctly decodes the provided `permissions` to verify the specified `flag` is a subset of the `permissions`.

**Securitize:** Remove this functionality in commit [0b8d506](https://github.com/securitize-io/bc-allowlist-checker-sc/commit/0b8d5061582f9dcac3b3eb2e24d37aba1de5e5bf) as it was not being used.

**Cyfrin:** Verified.
