---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-0-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-12-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-19-cyfrin-lido-earn-v2-0
title: '`ERC4626Adapter::maxMint` doesn''t consider pending fees to be harvested which
  leads to under-calculating the real shares that can be minted'
vuln_class: []
---

# `ERC4626Adapter::maxMint` doesn't consider pending fees to be harvested which leads to under-calculating the real shares that can be minted

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-19-cyfrin-lido-earn-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md)_

---

**Description:** The ERC4626Adapter::maxMint function computes the maximum quantity of shares that the Vault may mint by converting the maximum depositable assets in the underlying TARGET_VAULT into corresponding vault shares. However, this conversion process does not account for any pending fees.

As a consequence, the returned share amount underestimates the actual maximum mintable shares on the Vault. Specifically, upon harvesting the pending fees, additional shares are minted, thereby increasing the total supply and the effective conversion rate from assets to shares. This results in a post-harvest scenario where a greater number of shares can be minted for the same quantity of deposited assets than what `maxMint` initially indicates.

**Impact:** `maxMint` won't accurately report the actual maximum number of shares that can be minted.

**Proof of Concept:** Add the next test to `ERC4626Adapter.MaxDeposit.t.sol` test file
```solidity
    function test_PoC_MaxMint_DoesNotConsiderPendingYield() public {
        uint256 yield = 50_00e6;
        targetVault.setLiquidityCap(500_000e6);

        _seedVaults(yield);

        //@audit-info => Vault has pending yield

        uint256 snapshot = vm.snapshot();
            uint256 maxDeposit = vault.maxDeposit(alice);
            vm.prank(alice);
            vault.deposit(maxDeposit, alice);
            assertEq(vault.maxDeposit(alice), 0);
            assertEq(vault.maxMint(alice), 0);
        vm.revertTo(snapshot);

        //@audit-info => Given that Vault has pending yield, maxMint() is not accurate and will mint less shares than the actual maxMint post harvesting fees
        uint256 maxMintShares = vault.maxMint(alice);
        vm.prank(alice);
        vault.mint(maxMintShares, alice);
        assertGt(vault.maxDeposit(alice), 0);
        assertGt(vault.maxMint(alice), 0);

        //@audit-info => After attempting to mint the maxShares reported by the vault (and fees have been harvested during the mint), a second mint is possible when it shouldn't be because the previous mint was supposed to mint the max
        maxMintShares = vault.maxMint(alice);
        vm.prank(alice);
        vault.mint(maxMintShares, alice);
        assertEq(vault.maxDeposit(alice), 0);
        assertEq(vault.maxMint(alice), 0);
    }

    function _seedVaults(uint256 yield) internal {
        vm.prank(alice);
        vault.deposit(100_000e6, alice);

        vm.startPrank(bob);
        usdc.approve(address(targetVault), 100_000e6);
        targetVault.deposit(100_000e6, bob);
        vault.deposit(100_000e6, alice);
        vm.stopPrank();

        // mint yield to targetVault
        usdc.mint(address(targetVault), yield);
    }

```

**Recommended Mitigation:** Consider calculating the amount of shares by taking into account the pending fees to be harvested, similar to how the `previewMint` and `previewDeposit` functions do.

**Lido:** Fixed in commit [fc15b10](https://github.com/lidofinance/defi-interface/commit/fc15b104d3859955ed341e2785059e2806c6aa36).

**Cyfrin:** Verified. `maxMint` calls `previewDeposit` forwarding the `maxAssets` that can be deposited on the `TARGET_VAULT`. `previewDeposit` correctly accounts for any pending fees, meaning the calculated number of shares for the `maxAssets` correctly represents the actual maximum shares that can be minted post-harvesting pending fees.

\clearpage
