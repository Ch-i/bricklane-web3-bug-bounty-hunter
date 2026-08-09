---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-09-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-25-cyfrin-button-basis-trade-v2-0
title: Combination of Ownable and AccessControl can cause loss of admin functionality
vuln_class: []
---

# Combination of Ownable and AccessControl can cause loss of admin functionality

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-25-cyfrin-button-basis-trade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md)_

---

**Description:** `BasisTradeTailor` and `BasisTradeVault` mix `Ownable(2Step)Upgradeable` with `AccessControlUpgradeable`. Several admin wrappers are `onlyOwner` but internally call `grantRole` / `revokeRole`, which themselves require the caller to hold the role’s admin (usually `DEFAULT_ADMIN_ROLE`). Example:

```solidity
function grantAdmin(address account) external onlyOwner {
    grantRole(ADMIN_ROLE, account); // requires DEFAULT_ADMIN_ROLE too
}
```

This creates a dual requirement: the caller must be both `owner` and `DEFAULT_ADMIN_ROLE`. If those identities diverge (e.g., ownership transferred without also granting default admin), governance gets brittle and confusing.

**Impact:** The “Owner” may be unable to manage roles (grant/revoke admin/agent) and a `DEFAULT_ADMIN_ROLE` holder who isn’t `owner` can’t upgrade (since `_authorizeUpgrade` is `onlyOwner`) as well as extra wrappers duplicate functionality and enlarge the attack surface/bytecode/ABI for no gain.

**Proof of Concept:** Add the following test to `BasisTradeVault.t.sol` (a very similar test would work for Tailor):
```solidity
function test_OwnerLosesGrantAbility() public {
    _setupComplete();

    // owner transfers ownership
    vm.prank(deployer);
    vault.transferOwnership(alice);
    assertEq(vault.owner(), alice);

    // new owner cannot grant admin (or agent) roles
    vm.prank(alice);
    vm.expectRevert(
        abi.encodeWithSelector(
            IAccessControl.AccessControlUnauthorizedAccount.selector,
            alice,
            bytes32(0x00)
        )
    );
    vault.grantAdmin(bob);
}
```

**Recommended Mitigation:** Consider unifying on AccessControl by removing Ownable entirely. Gate privileged functions with `onlyRole(DEFAULT_ADMIN_ROLE)` and authorize upgrades via the same role:

  ```solidity
function grantAdmin(address account) external onlyRole(DEFAULT_ADMIN_ROLE) {
    grantRole(ADMIN_ROLE, account);
}

function _authorizeUpgrade(address impl) internal override onlyRole(DEFAULT_ADMIN_ROLE) {}
```
Then delete the bespoke wrappers `grantAdmin`, `revokeAdmin`, `grantAgent`, `revokeAgent` altogether. `DEFAULT_ADMIN_ROLE` already has authority to call `grantRole` / `revokeRole` directly, so these wrappers are redundant. Removing them shrinks bytecode/ABI, reduces surface area, and tidies the contracts.
To prevent lockout: use `AccessControlEnumerableUpgradeable` and enforce at least one default admin remains:
```solidity
function _revokeRole(bytes32 role, address account) internal override {
    if (role == DEFAULT_ADMIN_ROLE) {
        require(getRoleMemberCount(DEFAULT_ADMIN_ROLE) > 1, "keep >=1 default admin");
    }
    super._revokeRole(role, account);
}
```
Or if keeping `Ownable` is prefered, synchronize roles on ownership changes (grant new owner `DEFAULT_ADMIN_ROLE` and revoke from old).

**Button:** Fixed in commit [`32f8ca9`](https://github.com/buttonxyz/button-protocol/commit/32f8ca9c9e08986a554e12d3581178419b3d71f9) by moving to AccessControlEnumerableUpgradeable only.

**Cyfrin:** Verified. `AccessControlEnumerableUpgradeable` now used for both Tailor and Vault. The grant/revoke calls also removed in favor or AccessControls own calls.

\clearpage
