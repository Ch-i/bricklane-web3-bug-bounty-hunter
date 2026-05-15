---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-11-cyfrin-securitize-evm-whitelister-v2-0-0-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-02-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-11-cyfrin-securitize-evm-whitelister-v2-0
title: '`PermissionFlags::hasFlag` inconsistent validation for combined flags'
vuln_class: []
---

# `PermissionFlags::hasFlag` inconsistent validation for combined flags

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md)_

---

**Description:** `PermissionFlags` allows checking for multiple combinations of flags and verifying whether an account has at least one (OR), or all of them (ALL).

The problem is that `PermissionFlags::hasFlag` doesn't correctly verify the combination of `SWAP_ALLOWED` and `LIQUIDITY_ALLOWED`, it returns false when should return true.

**Impact:** Using `PermissionFlags::hasFlag` to validate combined flags can lead to incorrect validation, allowing execution when it should not.

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

    function test_hasFlag_SWAP_and_LIQUIDITY() public pure {
        PermissionFlag p = PermissionFlags.SWAP_ALLOWED & PermissionFlags.LIQUIDITY_ALLOWED;
        assertFalse(_has(p, PermissionFlags.NONE));
        assertFalse(_has(p, PermissionFlags.SWAP_ALLOWED));
        assertFalse(_has(p, PermissionFlags.LIQUIDITY_ALLOWED));
        assertFalse(_has(p, PermissionFlags.ALL_ALLOWED));

        assertTrue(p == p);
        //@audit-issue => hasFlag incapable of validating combined flags using AND
        assertTrue(_has(p, p));
    }
}
```

**Recommended Mitigation:** Consider restricting the use of `PermissionFlags::hasFlag` to validate individual flags; that is, revert execution when the value of the first parameter (`PermissionFlag permissions`) doesn't match any of the expected individual flags.

**Securitize:** Remove this functionality in commit [0b8d506](https://github.com/securitize-io/bc-allowlist-checker-sc/commit/0b8d5061582f9dcac3b3eb2e24d37aba1de5e5bf) as it was not being used.

**Cyfrin:** Verified.
