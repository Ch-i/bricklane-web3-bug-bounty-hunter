// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title ERC-4626 Tokenized Vault with Inflation Guard
/// @notice Reference implementation of the universal vault standard.
///         Demonstrates share/asset accounting and the first-depositor
///         inflation attack defense.
///
/// @dev KEY LOGIC PATTERN: A vault holds an underlying asset and issues
///      shares representing proportional ownership. The exchange rate
///      between shares and assets is:
///
///          assetsPerShare = totalAssets / totalShares
///
///      This is the most composable primitive in DeFi — lending pools,
///      yield aggregators, and staking contracts all use this interface.
///
///      THE INFLATION ATTACK:
///      1. Attacker deposits 1 wei → gets 1 share (they are first depositor)
///      2. Attacker donates 1000 USDC directly to the vault contract
///      3. Now 1 share = 1001 USDC (inflated exchange rate)
///      4. Victim deposits 999 USDC → gets 0 shares (999 * 1 / 1001 = 0)
///      5. Attacker redeems 1 share → gets all 2000 USDC
///
///      DEFENSE: Virtual shares and virtual assets (offset).
///      By pretending there's always 1 virtual share and 1 virtual asset,
///      the exchange rate starts at 1:1 and donation attacks become
///      economically impractical.

import {IERC20} from "./interfaces/IERC20.sol";

contract VaultERC4626 {
    IERC20 public immutable asset;

    uint256 public totalShares;
    mapping(address => uint256) public shares;

    // DEFENSE: Virtual offset to prevent inflation attack
    // OpenZeppelin uses _decimalsOffset() = 0 by default.
    // Setting offset = 1e6 means the attacker must donate >1M tokens
    // to steal 1 token from the next depositor.
    uint256 private constant VIRTUAL_SHARES = 1e6;
    uint256 private constant VIRTUAL_ASSETS = 1;

    event Deposit(address indexed caller, address indexed owner, uint256 assets, uint256 shares);
    event Withdraw(address indexed caller, address indexed receiver, uint256 assets, uint256 shares);

    constructor(address _asset) {
        asset = IERC20(_asset);
    }

    // -----------------------------------------------------------------------
    // PATTERN: Asset → Share conversion
    //
    // The fundamental accounting equation. Every vault operation reduces
    // to converting between assets and shares at the current rate.
    //
    // With virtual offset:
    //   shares = assets * (totalShares + VIRTUAL_SHARES) / (totalAssets + VIRTUAL_ASSETS)
    //
    // Without offset, first depositor can manipulate the rate.
    // -----------------------------------------------------------------------

    function convertToShares(uint256 assets) public view returns (uint256) {
        return (assets * (totalShares + VIRTUAL_SHARES)) / (_totalAssets() + VIRTUAL_ASSETS);
    }

    function convertToAssets(uint256 shareAmount) public view returns (uint256) {
        return (shareAmount * (_totalAssets() + VIRTUAL_ASSETS)) / (totalShares + VIRTUAL_SHARES);
    }

    function _totalAssets() internal view returns (uint256) {
        return asset.balanceOf(address(this));
    }

    // -----------------------------------------------------------------------
    // PATTERN: Deposit
    //
    // 1. Compute shares BEFORE transferring assets (Checks-Effects-Interactions)
    // 2. Transfer assets in
    // 3. Mint shares
    //
    // The CEI ordering here prevents reentrancy: state is updated
    // before the external call to transferFrom.
    // -----------------------------------------------------------------------

    function deposit(uint256 assets, address receiver) external returns (uint256 mintedShares) {
        require(assets > 0, "ZERO_ASSETS");

        // Checks: compute shares at current rate
        mintedShares = convertToShares(assets);
        require(mintedShares > 0, "ZERO_SHARES");

        // Effects: update state BEFORE external call
        totalShares += mintedShares;
        shares[receiver] += mintedShares;

        // Interactions: transfer assets in
        asset.transferFrom(msg.sender, address(this), assets);

        emit Deposit(msg.sender, receiver, assets, mintedShares);
    }

    // -----------------------------------------------------------------------
    // PATTERN: Withdraw
    //
    // Rounding direction matters: on deposit we round DOWN (fewer shares
    // for depositor = safe for vault), on withdraw we round DOWN
    // (fewer assets for withdrawer = safe for vault).
    //
    // If rounding goes the wrong way, a dust-level exploit loop can
    // drain the vault 1 wei at a time.
    // -----------------------------------------------------------------------

    function withdraw(uint256 shareAmount, address receiver) external returns (uint256 assets) {
        require(shareAmount > 0 && shareAmount <= shares[msg.sender], "INVALID_SHARES");

        // Compute assets (rounds DOWN — favoring the vault)
        assets = convertToAssets(shareAmount);

        // Effects first (CEI pattern)
        totalShares -= shareAmount;
        shares[msg.sender] -= shareAmount;

        // Transfer out
        asset.transfer(receiver, assets);

        emit Withdraw(msg.sender, receiver, assets, shareAmount);
    }
}
