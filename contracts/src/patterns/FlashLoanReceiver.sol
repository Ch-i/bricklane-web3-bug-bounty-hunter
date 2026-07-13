// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Flash Loan Receiver — Anatomy of Atomic Composability
/// @notice Reference implementation showing how flash loans work.
///         This is the purest expression of web3's unique logic:
///         uncollateralized loans that exist within a single transaction.
///
/// @dev KEY LOGIC PATTERN: A flash loan lets you borrow any amount
///      with zero collateral, as long as you repay it (plus fee)
///      within the SAME TRANSACTION. If repayment fails, the entire
///      transaction reverts — the loan never existed.
///
///      This is impossible in traditional finance. It exists because
///      blockchain transactions are atomic: they either fully succeed
///      or fully revert, with no intermediate state visible to others.
///
///      WHY THIS MATTERS:
///      - Enables capital-free arbitrage (align prices across DEXes)
///      - Enables capital-free liquidations (repay debt, seize collateral)
///      - Enables atomic governance attacks (borrow votes, pass proposal, return)
///      - Creates a level playing field: you don't need capital, just logic
///
///      SECURITY IMPLICATIONS:
///      - Any function that reads token balances is now attackable
///        (balances can be temporarily inflated by flash loans)
///      - Price oracles reading spot reserves are manipulable
///      - Governance voting power can be temporarily inflated
///      - The "have tokens = are economically aligned" assumption breaks

import {IERC20} from "./interfaces/IERC20.sol";

/// @notice Minimal flash loan pool — lends its entire balance in one call
contract FlashLoanPool {
    IERC20 public immutable token;
    uint256 public constant FEE_BPS = 9; // 0.09% fee (Aave V3 rate)

    event FlashLoan(address indexed borrower, uint256 amount, uint256 fee);

    constructor(address _token) {
        token = IERC20(_token);
    }

    // -----------------------------------------------------------------------
    // PATTERN: Flash Loan Execution
    //
    // The magic is in the structure:
    //   1. Record balance BEFORE
    //   2. Transfer tokens to borrower
    //   3. Call borrower's callback (they do whatever they want)
    //   4. Check balance AFTER >= balance BEFORE + fee
    //   5. If check fails, entire tx reverts — loan never happened
    //
    // This is why flash loans are trustless: the lender takes zero risk.
    // The EVM's atomicity guarantee IS the collateral.
    // -----------------------------------------------------------------------

    function flashLoan(uint256 amount, bytes calldata data) external {
        uint256 balanceBefore = token.balanceOf(address(this));
        require(amount <= balanceBefore, "INSUFFICIENT_LIQUIDITY");

        uint256 fee = (amount * FEE_BPS) / 10000;

        // Transfer tokens to borrower
        token.transfer(msg.sender, amount);

        // Callback: borrower executes their strategy
        // SECURITY: This is where the borrower does arbitrage, liquidation, etc.
        // They can do ANYTHING with the borrowed tokens as long as they repay.
        IFlashBorrower(msg.sender).onFlashLoan(amount, fee, data);

        // CRITICAL CHECK: verify repayment
        // If this fails, the entire transaction reverts.
        // The tokens were never actually "lent" — the state change is undone.
        uint256 balanceAfter = token.balanceOf(address(this));
        require(balanceAfter >= balanceBefore + fee, "REPAYMENT_FAILED");

        emit FlashLoan(msg.sender, amount, fee);
    }
}

/// @notice Example flash loan receiver — demonstrates the callback pattern
/// @dev In production, the onFlashLoan callback would contain the actual
///      strategy (arbitrage, liquidation, collateral swap, etc.)
contract ExampleFlashBorrower {
    IERC20 public immutable token;
    FlashLoanPool public immutable pool;

    constructor(address _token, address _pool) {
        token = IERC20(_token);
        pool = FlashLoanPool(_pool);
    }

    /// @notice Execute a flash loan
    function executeFlashLoan(uint256 amount) external {
        pool.flashLoan(amount, "");
    }

    // -----------------------------------------------------------------------
    // PATTERN: Flash Loan Callback
    //
    // SECURITY: This function MUST verify that msg.sender is the
    // expected pool. Otherwise, anyone can call it to steal funds.
    //
    // The rekt-ripmevbot exploit ($1.5M, 2022) happened because a
    // MEV bot left its dYdX flashloan callback (`callFunction`)
    // permissionless — anyone could call it to drain the bot.
    // -----------------------------------------------------------------------

    function onFlashLoan(uint256 amount, uint256 fee, bytes calldata /* data */) external {
        // SECURITY: Verify caller is the legitimate pool
        require(msg.sender == address(pool), "UNAUTHORIZED_CALLER");

        // ═══════════════════════════════════════════════════════════════
        // YOUR STRATEGY GOES HERE
        //
        // At this point you have `amount` tokens with zero collateral.
        // You can:
        //   - Swap on DEX A, swap back on DEX B (arbitrage)
        //   - Repay someone's debt, seize their collateral (liquidation)
        //   - Swap collateral type in a lending position (collateral swap)
        //   - Temporarily inflate your voting power (governance attack)
        //
        // The only rule: you must have amount + fee tokens in this
        // contract by the time this function returns.
        // ═══════════════════════════════════════════════════════════════

        // Repay: transfer amount + fee back to the pool
        token.transfer(address(pool), amount + fee);
    }
}

interface IFlashBorrower {
    function onFlashLoan(uint256 amount, uint256 fee, bytes calldata data) external;
}
