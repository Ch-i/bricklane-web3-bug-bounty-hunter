---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-3-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-09-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-25-cyfrin-button-basis-trade-v2-0
title: Consider implementing `ERC4626::mint`
vuln_class: []
---

# Consider implementing `ERC4626::mint`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-25-cyfrin-button-basis-trade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md)_

---

**Description:** `BasisTradeVault` currently disables `mint()` and `previewMint()` (both revert), which reduces interoperability with ERC-4626 tooling, routers, vault aggregators, and simulators that rely on the “mint for exact shares” flow (e.g., slippage-aware deposits or migrators). Consider implementing:

* `previewMint(shares)` that **grosses up** the net asset requirement by adding the deposit fee on top (so the return is the *gross* assets a user must provide to mint `shares`), and
* enabling `mint(shares, receiver)` so it uses the standard ERC-4626 path (which will call the new `previewMint`), while enforcing the same controls as `deposit` (whitelist/TVL cap).
  This preserves your fee semantics (fee extracted from the provided gross amount) and materially improves compatibility with existing ERC-4626 integrations and tooling.

```solidity
/**
 * @notice Preview the *gross* assets required to mint `shares`
 * @dev We gross-up the net assets (from base ERC4626 math) by adding the deposit fee on top.
 */
function previewMint(uint256 shares) public view virtual override returns (uint256) {
    require(shares > 0, "Cannot mint 0 shares");

    // Net assets required by base ERC4626 math (what must end up in the vault)
    uint256 netAssets = super.previewMint(shares);

    // Fee is charged on top of the net assets
    uint256 fee = _calculateFeeAmount(netAssets, depositFeeBps);
    return netAssets + fee; // gross = net + fee
}

/**
 * @notice Mint `shares` to `receiver`, charging the deposit fee on top
 * @dev Enforces the same whitelist/TVL checks as `deposit`.
 *      `super.mint` will use `previewMint` (gross) and enforce `maxMint(receiver)`.
 */
function mint(uint256 shares, address receiver) public virtual override checkDepositWhitelist(receiver) returns (uint256 assets) {
    return super.mint(shares, receiver);
}

/**
 * @notice Maximum shares that can be minted for `receiver`
 * @dev Derived from the gross-asset TVL cap (`maxDeposit`) by converting gross→net (remove fee),
 *      then net→shares using base ERC4626 math. Uses Floor rounding to stay within cap.
 */
function maxMint(address receiver) public view virtual override returns (uint256) {
    // Respect deposit whitelist if enabled
    if (depositWhitelistEnabled && !depositWhitelist[receiver]) {
        return 0;
    }

    // `maxDeposit(receiver)` returns the remaining *gross* capacity (fee included)
    uint256 grossCap = maxDeposit(receiver);
    if (grossCap == 0) return 0;

    // Convert gross -> net by extracting the fee portion from the gross amount
    uint256 feeFromGross = _extractFeeFromTotal(grossCap, depositFeeBps);
    uint256 netCap = grossCap - feeFromGross;

    // Convert the net-asset capacity to shares
    return _convertToShares(netCap, Math.Rounding.Floor);
}
```
And tests for the same in `BasisTradeVault.t.sol` (added test for `maxDeposit` as well):
```solidity
function test_MintNoFees() public {
    // Setup the vault completely (already has 0% fees)
    _setupComplete();

    // Setup alice for deposits
    vm.prank(admin);
    vault.addToDepositWhitelist(alice);
    vm.prank(admin);
    vault.setTvlCap(100000 * 10**6);

    // Test 1: Alice deposits 10,000 USDC with 0% fee
    uint256 depositShares = 10000 * 10**6;

    vm.startPrank(alice);
    usdc.approve(address(vault), depositShares);
    uint256 actualAssets = vault.mint(depositShares, alice);
    vm.stopPrank();

    // With 0% fee, expect exactly 1:1 ratio
    assertEq(actualAssets, 10000 * 10**6); // Exactly 10,000 shares
    assertEq(actualAssets, depositShares);
    assertEq(vault.balanceOf(alice), depositShares);
    assertEq(vault.totalSupply(), 1000 * 10**6 + actualAssets); // Initial 1000 + alice's 10,000

    // Test 2: Bob deposits 5,000 USDC - still 1:1 with no fees
    vm.prank(admin);
    vault.addToDepositWhitelist(bob);

    uint256 bobShares = 5000 * 10**6;

    vm.startPrank(bob);
    usdc.approve(address(vault), bobShares);
    uint256 bobActualAssets = vault.mint(bobShares, bob);
    vm.stopPrank();

    // Still expect 1:1 with no fees
    assertEq(bobActualAssets, 5000 * 10**6);
    assertEq(bobActualAssets, bobShares);
    assertEq(vault.balanceOf(bob), bobShares);
}

function test_MintWithFees() public {
    // Setup the vault completely
    _setupComplete();

    // Set deposit fee to 1%
    vm.prank(admin);
    vault.setDepositFee(100);

    // Add alice to whitelist and increase TVL cap
    vm.prank(admin);
    vault.addToDepositWhitelist(alice);
    vm.prank(admin);
    vault.setTvlCap(100000 * 10**6);

    // Check initial state
    assertEq(vault.depositFeeBps(), 100); // 1% fee
    assertEq(vault.totalSupply(), 1000 * 10**6); // Initial deposit
    assertEq(vault.totalAssets(), 1000 * 10**6); // Initial assets

    // Alice mints 10,000 shares
    uint256 sharesAmount = 1000 * 10**6;

    // Preview how many shares alice should get
    uint256 expectedAssets = vault.previewMint(sharesAmount);

    // Execute the deposit
    vm.startPrank(alice);
    usdc.approve(address(vault), expectedAssets);
    uint256 actualAssets = vault.mint(sharesAmount, alice);
    vm.stopPrank();

    // Verify shares minted
    assertEq(actualAssets, expectedAssets);
    assertEq(actualAssets, 1010 * 10**6); // Exact amount, roughly 100bps less
    assertEq(vault.balanceOf(alice), sharesAmount);

    // Verify total supply increased by shares minted
    assertEq(vault.totalSupply(), 1000 * 10**6 + sharesAmount);

    // Verify funds are still in the vault (not moved to pocket yet)
    assertEq(usdc.balanceOf(address(vault)), 1000 * 10**6 + actualAssets);
}

function test_MintNoFees() public {
    // Setup the vault completely (already has 0% fees)
    _setupComplete();

    // Setup alice for deposits
    vm.prank(admin);
    vault.addToDepositWhitelist(alice);
    vm.prank(admin);
    vault.setTvlCap(100000 * 10**6);

    // Test 1: Alice deposits 10,000 USDC with 0% fee
    uint256 depositShares = 10000 * 10**6;

    vm.startPrank(alice);
    usdc.approve(address(vault), depositShares);
    uint256 actualAssets = vault.mint(depositShares, alice);
    vm.stopPrank();

    // With 0% fee, expect exactly 1:1 ratio
    assertEq(actualAssets, 10000 * 10**6); // Exactly 10,000 shares
    assertEq(actualAssets, depositShares);
    assertEq(vault.balanceOf(alice), depositShares);
    assertEq(vault.totalSupply(), 1000 * 10**6 + actualAssets); // Initial 1000 + alice's 10,000

    // Test 2: Bob deposits 5,000 USDC - still 1:1 with no fees
    vm.prank(admin);
    vault.addToDepositWhitelist(bob);

    uint256 bobShares = 5000 * 10**6;

    vm.startPrank(bob);
    usdc.approve(address(vault), bobShares);
    uint256 bobActualAssets = vault.mint(bobShares, bob);
    vm.stopPrank();

    // Still expect 1:1 with no fees
    assertEq(bobActualAssets, 5000 * 10**6);
    assertEq(bobActualAssets, bobShares);
    assertEq(vault.balanceOf(bob), bobShares);
}

function test_MintWithFees() public {
    // Setup the vault completely
    _setupComplete();

    // Set deposit fee to 1%
    vm.prank(admin);
    vault.setDepositFee(100);

    // Add alice to whitelist and increase TVL cap
    vm.prank(admin);
    vault.addToDepositWhitelist(alice);
    vm.prank(admin);
    vault.setTvlCap(100000 * 10**6);

    // Check initial state
    assertEq(vault.depositFeeBps(), 100); // 1% fee
    assertEq(vault.totalSupply(), 1000 * 10**6); // Initial deposit
    assertEq(vault.totalAssets(), 1000 * 10**6); // Initial assets

    // Alice mints 10,000 shares
    uint256 sharesAmount = 1000 * 10**6;

    // Preview how many shares alice should get
    uint256 expectedAssets = vault.previewMint(sharesAmount);

    // Execute the deposit
    vm.startPrank(alice);
    usdc.approve(address(vault), expectedAssets);
    uint256 actualAssets = vault.mint(sharesAmount, alice);
    vm.stopPrank();

    // Verify shares minted
    assertEq(actualAssets, expectedAssets);
    assertEq(actualAssets, 1010 * 10**6); // Exact amount, roughly 100bps less
    assertEq(vault.balanceOf(alice), sharesAmount);

    // Verify total supply increased by shares minted
    assertEq(vault.totalSupply(), 1000 * 10**6 + sharesAmount);

    // Verify funds are still in the vault (not moved to pocket yet)
    assertEq(usdc.balanceOf(address(vault)), 1000 * 10**6 + actualAssets);
}
```

**Button:** Fixed by the Cyfrin team in commit [`d38f046`](https://github.com/buttonxyz/button-protocol/commit/d38f046befbc5deba426eb6cabac65703cd643b5)

**Cyfrin:** Verified. `mint` is implemented.
