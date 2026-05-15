// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

import {MockToken} from "./MockToken.sol";

/// @notice Single-asset isolated lending market. Users post collateral,
///         borrow up to LTV, optionally donate eToken-like collateral
///         shares to protocol reserves, and can be liquidated when their
///         health factor drops below the threshold.
///
/// @dev Collateral and debt are tracked 1:1 with the underlying asset (no
///      eToken/dToken share recursion) so the accounting is straight
///      forward. The liquidation discount scales with how distressed the
///      violator is so liquidators are incentivised to mop up bad debt
///      promptly.
contract CreditMarket {
    MockToken public immutable asset;

    /// @notice User collateral in underlying-asset units.
    mapping(address => uint256) public collateral;

    /// @notice User debt in underlying-asset units (no interest accrual).
    mapping(address => uint256) public debt;

    /// @notice Protocol-owned reserves accumulated from donations + bad-debt sweep.
    uint256 public reserves;

    /// @dev Loan-to-value cap on new borrows, in percent.
    uint256 public constant LTV_PCT = 75;

    /// @dev Health-factor threshold below which a position becomes liquidatable.
    /// HF is reported as (collateral * 100) / debt, so HF = 100 means
    /// collateral exactly equals debt. HF = 80 means the position is 80%
    /// covered.
    uint256 public constant LIQUIDATION_THRESHOLD_HF = 100;

    event Deposit(address indexed user, uint256 amount);
    event Withdraw(address indexed user, uint256 amount);
    event Borrow(address indexed user, uint256 amount);
    event Repay(address indexed user, uint256 amount);
    event Donate(address indexed donor, uint256 amount);
    event Liquidate(
        address indexed violator,
        address indexed liquidator,
        uint256 repaid,
        uint256 seized
    );

    constructor(MockToken _asset) {
        asset = _asset;
    }

    function deposit(uint256 amount) external {
        require(amount > 0, "zero deposit");
        require(asset.transferFrom(msg.sender, address(this), amount), "transfer in");
        collateral[msg.sender] += amount;
        emit Deposit(msg.sender, amount);
    }

    function withdraw(uint256 amount) external {
        require(collateral[msg.sender] >= amount, "insufficient collateral");
        collateral[msg.sender] -= amount;
        _requireHealth(msg.sender);
        require(asset.transfer(msg.sender, amount), "transfer out");
        emit Withdraw(msg.sender, amount);
    }

    function borrow(uint256 amount) external {
        require(amount > 0, "zero borrow");
        uint256 maxBorrow = (collateral[msg.sender] * LTV_PCT) / 100;
        require(debt[msg.sender] + amount <= maxBorrow, "exceeds LTV");
        debt[msg.sender] += amount;
        require(asset.transfer(msg.sender, amount), "transfer out");
        emit Borrow(msg.sender, amount);
    }

    function repay(uint256 amount) external {
        uint256 owed = debt[msg.sender];
        uint256 toRepay = amount > owed ? owed : amount;
        require(asset.transferFrom(msg.sender, address(this), toRepay), "transfer in");
        debt[msg.sender] -= toRepay;
        emit Repay(msg.sender, toRepay);
    }

    /// @notice Burn `amount` of caller's collateral into protocol reserves.
    /// @dev Used to reward stakers, top up the bad-debt buffer, or pay
    ///      protocol-level subsidies. Caller must hold enough collateral
    ///      to cover the donation.
    function donateToReserves(uint256 amount) external {
        require(collateral[msg.sender] >= amount, "insufficient collateral");
        collateral[msg.sender] -= amount;
        reserves += amount;
        emit Donate(msg.sender, amount);
    }

    /// @notice Liquidate an unhealthy position by repaying some of its debt
    ///         in exchange for a discounted slice of its collateral.
    /// @param violator the borrower being liquidated
    /// @param repayAmount amount of `asset` the liquidator pays to repay
    ///                    `violator`'s debt
    function liquidate(address violator, uint256 repayAmount) external {
        require(_healthFactor(violator) < LIQUIDATION_THRESHOLD_HF, "not liquidatable");
        require(repayAmount > 0 && repayAmount <= debt[violator], "bad repay amount");

        // Liquidators get a discount that grows as the violator's position
        // sinks further underwater. Encourages prompt clean-up of bad debt.
        uint256 discountBps = _liquidationDiscountBps(violator);
        uint256 seized = (repayAmount * (10_000 + discountBps)) / 10_000;

        // Clamp to what the violator actually has, to avoid underflow.
        if (seized > collateral[violator]) {
            seized = collateral[violator];
        }

        require(asset.transferFrom(msg.sender, address(this), repayAmount), "transfer in");
        debt[violator] -= repayAmount;
        collateral[violator] -= seized;
        collateral[msg.sender] += seized;

        emit Liquidate(violator, msg.sender, repayAmount, seized);
    }

    /// @notice Sweep a fully-bankrupt position's residual debt into reserves.
    /// @dev If a position is so far underwater that `collateral == 0` but
    ///      `debt > 0`, no liquidator will touch it. Reserves absorb the
    ///      bad debt and the position is reset.
    function clearBadDebt(address user) external {
        require(collateral[user] == 0 && debt[user] > 0, "not bankrupt");
        uint256 toAbsorb = debt[user];
        require(reserves >= toAbsorb, "reserves too low");
        reserves -= toAbsorb;
        debt[user] = 0;
    }

    function healthFactor(address user) external view returns (uint256) {
        return _healthFactor(user);
    }

    function _healthFactor(address user) internal view returns (uint256) {
        if (debt[user] == 0) return type(uint256).max;
        return (collateral[user] * 100) / debt[user];
    }

    function _requireHealth(address user) internal view {
        if (debt[user] == 0) return;
        uint256 maxDebt = (collateral[user] * LTV_PCT) / 100;
        require(debt[user] <= maxDebt, "would exceed LTV");
    }

    /// @notice Return the liquidation discount in basis points (10000 = 100%).
    /// @dev Discount scales linearly with how far below the threshold the
    ///      violator's health factor is. At HF = threshold the discount is
    ///      0; at HF = 0 the discount is 100% (i.e. liquidator receives
    ///      2× the repaid amount in collateral).
    function _liquidationDiscountBps(address user) internal view returns (uint256) {
        uint256 hf = _healthFactor(user);
        if (hf >= LIQUIDATION_THRESHOLD_HF) return 0;
        // Scale (0..threshold) → (10000..0) bps of bonus.
        return ((LIQUIDATION_THRESHOLD_HF - hf) * 10_000) / LIQUIDATION_THRESHOLD_HF;
    }
}
