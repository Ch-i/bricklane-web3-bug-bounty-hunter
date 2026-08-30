---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-2-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Missing check if `receiver` is whitelisted in `StakingVault::mint, deposit`
vuln_class: []
---

# Missing check if `receiver` is whitelisted in `StakingVault::mint, deposit`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** `StakingVault::mint, deposit` only validates that `msg.sender` is whitelisted but fails to check if the receiver parameter is whitelisted. Since non-whitelisted addresses cannot withdraw, redeem, or transfer shares, any shares minted to non-whitelisted receivers become permanently locked and unusable.
```solidity
 function mint(
        uint256 shares,
        address receiver //@audit receiver could be not whitelisted?
    ) public override onlyWhitelisted(msg.sender) returns (uint256 assets) {
        ...
    }
```

**Impact:** Permanent loss of user funds or temporary if owner give whitelisted permissions.

**Proof of Concept:** Run the next proof of concept in `StakingVault.sol`:
```solidity
function test_mint_non_whitelist_receiver() public {
        uint256 amount = 100 ether;

        vm.startPrank(user1);
        asset.approve(address(vault), amount);

        //create a non whitelisted receiver
        address bob = makeAddr("receiver");

        // 1. Alice (whitelisted) mints shares to Bob (non-whitelisted)
        vault.mint(1000 * 1e8, bob); // Success - only checks Alice is whitelisted

        vm.stopPrank();

        // 2. Bob tries to withdraw - REVERTS
        vm.prank(bob);
        vault.withdraw(1000 * 1e8, bob, bob); // Reverts: not whitelisted
        // Result: 1000 shares worth of HilBTC permanently locked
    }

```

**Recommended Mitigation:** Add a whitelist check for the receiver in the mint() function:

```diff
function mint(
    uint256 shares,
    address receiver
+ ) public override onlyWhitelisted(msg.sender) onlyWhitelisted(receiver) returns (uint256 assets) {
-   ) public override onlyWhitelisted(msg.sender) returns (uint256 assets) {
 ...
}
// Similar fix to `deposit`
```

**Syntetika:**
Fixed in commit [86384fe](https://github.com/SyntetikaLabs/monorepo/commit/86384fe1504780338649d25f720fb78b25132875) by removing the whitelist functionality entirely from `StakingVault` to resolve finding L-4.

**Cyfrin:** Verified.
