---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-3-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: '`DEFAULT_ADMIN_ROLE` can be mistakenly granted to an account when granting
  permission to call `fallback` on any contract'
vuln_class: []
---

# `DEFAULT_ADMIN_ROLE` can be mistakenly granted to an account when granting permission to call `fallback` on any contract

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** `AccessControlManager` is in charge of managing roles and permissions for accounts to determine what users can call on which contracts.

Permissions are granted at the selector level, and is possible to grant permissions to only one contract at a time, or authorize an account to call the same selector on any contract.

There is an edge case when permitting an account to call the `fallback()` function whose selector is `bytes4(0)` on any account (address(0)).
- The combination of those two inputs results in calculating the role as bytes(0), which is the exact value assigned for the DEFAULT_ADMIN_ROLE.

```solidity
    function grantCall(address contractAddress, bytes4 sel, address accountToPermit) public {
//@audit-issue => The calculated role for `address(0)` and `bytes4(0)` is bytes32(0)`
        bytes32 role = roleFor(contractAddress, sel);
//@audit-issue => Granting bytes32(0) to the account results in granting the DEFAULT_ADMIN_ROLE
        grantRole(role, accountToPermit);
        emit PermissionGranted(accountToPermit, contractAddress, sel);
    }

    function roleFor(address contractAddress, bytes4 sel) internal pure returns (bytes32 role) {
//@audit-issue => The calculated role for `address(0)` and `bytes4(0)` is bytes32(0)`
        role = (bytes32(uint256(uint160(contractAddress))) << 96) | bytes32(uint256(uint32(sel)));
    }

```

**Impact:** Users can be mistakenly granted the DEFAULT_ADMIN_ROLE, which they can then use to authorize other users to call restricted functions.

**Proof of Concept:** Add the next PoC to `CDO.t.sol` test file:
1. Alice gets DEFAULT_ADMIN_ROLE by mistake when she was meant to receive permission to call fallback() on any contract
2. Once Alice has DEFAULT_ADMIN_ROLE, he authorizes Bob to call other functions on a different contract.
```solidity
    function test_grantsDefaultAdminByMisstake() public {
        bytes32 DEFAULT_ADMIN_ROLE = acm.DEFAULT_ADMIN_ROLE();

        address contractAddress = address(0);
        bytes4 selector = bytes4(0);

        address alice = makeAddr("Alice");

        assertFalse(acm.hasRole(DEFAULT_ADMIN_ROLE, alice));

        //@audit-issue => Granting permission to alice to call fallback function on any contract results on granting Alice the DEFAULT_ADMIN_ROLE
        acm.grantCall(contractAddress, selector, alice);
        assertTrue(acm.hasRole(DEFAULT_ADMIN_ROLE, alice));

        address contractA = makeAddr("contractA");
        address bob = makeAddr("bob");
        bytes4 withdrawSelector = bytes4(keccak256(bytes("withdraw(address,uint256)")));

        assertFalse(acm.hasPermission(bob, contractA, withdrawSelector));

        //@audit-info => Alice w/ DEFAULT_ADMIN can grant permissions to other accounts
        vm.startPrank(alice);
        acm.grantCall(contractA, withdrawSelector, bob);
        assertTrue(acm.hasPermission(bob, contractA, withdrawSelector));
    }

```

**Recommended Mitigation:** Validate that the computed role is not the DEFAULT_ADMIN_ROLE; otherwise, revert the tx.
```diff
    function grantCall(address contractAddress, bytes4 sel, address accountToPermit) public {
        bytes32 role = roleFor(contractAddress, sel);
+       require(role != DEFAULT_ADMIN_ROLE, "Granting DEFAULT_ADMIN_ROLE");
        grantRole(role, accountToPermit);
        emit PermissionGranted(accountToPermit, contractAddress, sel);
    }
```

**Strata:**
Fixed in commit [e6ad2d](https://github.com/Strata-Money/contracts-tranches/commit/e6ad2d59f1ad9abab0a9af685aeea8d510e9169d) by adding a check to revert when `contractAddress` is `address(0)` or `selector` is `bytes(0)`

**Cyfrin:** Verified. New change prevents from mistakenly assign DEFAULT_ADMIN_ROLE.
Permissions are granted on a per-contract per-selector basis.


\clearpage
