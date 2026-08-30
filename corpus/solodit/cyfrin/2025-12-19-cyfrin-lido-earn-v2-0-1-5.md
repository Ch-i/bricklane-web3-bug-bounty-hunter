---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-1-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-12-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-19-cyfrin-lido-earn-v2-0
title: Not including `_decimalsOffset` when calculating the fee shares
vuln_class: []
---

# Not including `_decimalsOffset` when calculating the fee shares

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-19-cyfrin-lido-earn-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md)_

---

**Description:** Formulas converting assets to shares across the codebase utilize the virtual supply to prevent rate manipulation. However, when calculating the number of shares to be minted for accrued fees, the conversion formula does not call `_calculateFeeShares()` and omits `_decimalsOffset()` when calculating the fee shares.

Add the next PoC to `ERC4626Adapter.Fees.t.sol`.

```solidity
    function test_PoC_InflateRatioViaFees() public {
        vm.prank(alice);
        uint256 alice_receivedShares = vault.deposit(1, alice);

        emit log_named_uint("totalAssets", vault.totalAssets());
        emit log_named_uint("totalSupply", vault.totalSupply());

        emit log_named_uint("assets per wei of share", vault.convertToAssets(alice_receivedShares));

        usdc.mint(address(targetVault), 1_000e18); //
        vault.harvestFees();

        emit log_named_uint("totalSupply", vault.totalSupply());
        emit log_named_uint("assets per wei of share", vault.convertToAssets(alice_receivedShares));

        vm.prank(bob);
        uint256 bob_receivedShares = vault.deposit(100e18, bob);

        uint256 bobAssetsBeforeRedeem = usdc.balanceOf(bob);

        vm.prank(bob);
        vault.redeem(bob_receivedShares, bob, bob);

        uint256 bobAssetsAfterRedeem = usdc.balanceOf(bob);

        emit log_named_uint("bob assets withdrawn", bobAssetsAfterRedeem
         - bobAssetsBeforeRedeem);
        assertTrue(bobAssetsAfterRedeem - bobAssetsBeforeRedeem > 99e18);

        // @audit //
        // With current formula, bob withdraws: 99999880924647933225 [9.999e19])

        // With formula using _decimalsOffset(): val: 99999803787934739453 [9.999e19])

        // @audit => Difference is neglegible for the required amount to donate to inflate the ratio //

    }

```

**Lido:** Acknowledged. Precision loss doesn't exceed one wei, no impact to the value received by the fee receiver.

\clearpage
