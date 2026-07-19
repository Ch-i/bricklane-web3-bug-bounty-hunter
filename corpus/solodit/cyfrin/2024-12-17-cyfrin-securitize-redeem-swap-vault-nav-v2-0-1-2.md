---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0-1-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0
title: Ambiguous owner terminology creates confusion in access control of SecuritizeVault
vuln_class: []
---

# Ambiguous owner terminology creates confusion in access control of SecuritizeVault

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md)_

---

**Description:** SecuritizeVault implements two different ownership concepts that create confusion in access control. It uses a custom `OWNER_ROLE` for vault operations (deposit/redeem) while inheriting `OwnableUpgradeable` which provides its own `owner()` function. This creates a situation where the term "owner" refers to different addresses depending on the context - the `OWNER_ROLE` holder can perform vault operations but cannot execute `onlyOwner` functions like `pause()`, while the Ownable owner can pause but cannot perform vault operations.

**Impact:** This ambiguity could lead to security issues if developers or users misunderstand which "owner" has what permissions, potentially resulting in failed operations or incorrect access control implementations in dependent contracts.

**Proof Of Concept:**
```solidity
function testPause() public {
    // admin (the deployer) is Ownable owner - can pause/unpause
    vm.startPrank(admin);
    vault.pause();
    assertTrue(vault.paused());
    vault.unpause();
    vm.stopPrank();

    // OWNER_ROLE holder cannot pause
    vm.startPrank(owner);
    vm.expectRevert(abi.encodeWithSelector(OwnableUpgradeable.OwnableUnauthorizedAccount.selector, owner));
    vault.pause();
    vm.stopPrank();

    // Demonstrating the confusion:
    assertTrue(vault.isOwner(owner));     // True: has OWNER_ROLE
    assertFalse(vault.isOwner(admin));    // False: doesn't have OWNER_ROLE
    assertTrue(vault.owner() == admin);    // True: is Ownable owner
}
```

**Recommended Mitigation:**
1. Consolidate ownership model to use either roles or Ownable pattern exclusively
2. If both are needed, rename functions/roles to be more explicit:
```solidity
// Instead of OWNER_ROLE
bytes32 public constant VAULT_OPERATOR_ROLE = keccak256("VAULT_OPERATOR_ROLE");

// Instead of isOwner()
function isVaultOperator(address account) public view returns (bool) {
    return hasRole(VAULT_OPERATOR_ROLE, account);
}
```
3. Add clear documentation explaining the distinction between different types of ownership

**Securitize:** Fixed in commit [887554](https://bitbucket.org/securitize_dev/bc-securitize-vault-sc/commits/8875544d6d3c5e20cec43ba06f3cce157a7cfcec).

**Cyfrin:** Verified.


\clearpage
