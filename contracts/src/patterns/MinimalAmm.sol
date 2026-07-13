// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Minimal AMM — Constant Product Market Maker (x*y=k)
/// @notice Reference implementation of the foundational DeFi primitive.
///         This is the mathematical core of Uniswap V2 and all its forks.
///
/// @dev KEY LOGIC PATTERN: The invariant x * y = k means that any trade
///      that increases one reserve must decrease the other such that
///      the product remains constant (minus fees). This creates a
///      deterministic price curve without order books.
///
///      The price of tokenA in terms of tokenB is simply:
///          price = reserveB / reserveA
///
///      This shifts after every trade — which is both the mechanism's
///      power (continuous price discovery) and its weakness (impermanent
///      loss, sandwich attacks, slippage).
///
///      SECURITY NOTES:
///      - First depositor can inflate share price (see ERC-4626 inflation attack)
///      - All swaps must enforce caller-supplied minOut (never 0)
///      - deadline must be a real timestamp, not block.timestamp
///      - sqrt calculation must use safe integer math

import {IERC20} from "./interfaces/IERC20.sol";

contract MinimalAMM {
    IERC20 public immutable tokenA;
    IERC20 public immutable tokenB;

    uint256 public reserveA;
    uint256 public reserveB;

    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    uint256 private constant FEE_BPS = 30; // 0.3% fee

    event Mint(address indexed provider, uint256 amountA, uint256 amountB, uint256 shares);
    event Burn(address indexed provider, uint256 amountA, uint256 amountB, uint256 shares);
    event Swap(address indexed sender, address indexed tokenIn, uint256 amountIn, uint256 amountOut);

    constructor(address _tokenA, address _tokenB) {
        tokenA = IERC20(_tokenA);
        tokenB = IERC20(_tokenB);
    }

    // -----------------------------------------------------------------------
    // PATTERN: Liquidity Provision
    // Depositors add both tokens proportionally and receive LP shares.
    // The ratio must match current reserves to prevent value extraction.
    // -----------------------------------------------------------------------

    function addLiquidity(uint256 amountA, uint256 amountB)
        external
        returns (uint256 shares)
    {
        tokenA.transferFrom(msg.sender, address(this), amountA);
        tokenB.transferFrom(msg.sender, address(this), amountB);

        if (totalSupply == 0) {
            // First deposit: shares = sqrt(amountA * amountB)
            // This sets the initial price ratio.
            shares = _sqrt(amountA * amountB);
            require(shares > 0, "INSUFFICIENT_LIQUIDITY");
        } else {
            // Subsequent deposits: shares proportional to smaller ratio
            // This prevents depositing unbalanced amounts to extract value.
            shares = _min(
                (amountA * totalSupply) / reserveA,
                (amountB * totalSupply) / reserveB
            );
        }

        require(shares > 0, "ZERO_SHARES");
        totalSupply += shares;
        balanceOf[msg.sender] += shares;
        reserveA += amountA;
        reserveB += amountB;

        emit Mint(msg.sender, amountA, amountB, shares);
    }

    // -----------------------------------------------------------------------
    // PATTERN: Swap with constant product invariant
    //
    // The core logic: given input amount, compute output such that
    // (reserveIn + amountIn) * (reserveOut - amountOut) >= k
    //
    // The fee is taken from the input before computing the output.
    // -----------------------------------------------------------------------

    function swap(
        address tokenIn,
        uint256 amountIn,
        uint256 minAmountOut,    // CRITICAL: caller must set this > 0
        uint256 deadline         // CRITICAL: must be a real timestamp
    )
        external
        returns (uint256 amountOut)
    {
        // SECURITY: Real deadline check — block.timestamp alone is NOT a deadline
        require(block.timestamp <= deadline, "EXPIRED");
        require(amountIn > 0, "ZERO_INPUT");

        bool isAtoB = tokenIn == address(tokenA);
        require(isAtoB || tokenIn == address(tokenB), "INVALID_TOKEN");

        (uint256 resIn, uint256 resOut) = isAtoB
            ? (reserveA, reserveB)
            : (reserveB, reserveA);

        // Transfer in
        IERC20(tokenIn).transferFrom(msg.sender, address(this), amountIn);

        // Apply fee: only (10000 - FEE_BPS) / 10000 of input counts
        uint256 amountInWithFee = amountIn * (10000 - FEE_BPS);

        // x * y = k formula:
        // amountOut = (resOut * amountInWithFee) / (resIn * 10000 + amountInWithFee)
        amountOut = (resOut * amountInWithFee) / (resIn * 10000 + amountInWithFee);

        // SECURITY: Enforce caller-supplied minimum output
        // This is the PRIMARY defense against sandwich attacks.
        // Setting minAmountOut = 0 means accepting any price = free sandwich.
        require(amountOut >= minAmountOut, "INSUFFICIENT_OUTPUT");
        require(amountOut > 0, "ZERO_OUTPUT");

        // Transfer out
        IERC20(isAtoB ? address(tokenB) : address(tokenA)).transfer(msg.sender, amountOut);

        // Update reserves
        if (isAtoB) {
            reserveA += amountIn;
            reserveB -= amountOut;
        } else {
            reserveB += amountIn;
            reserveA -= amountOut;
        }

        emit Swap(msg.sender, tokenIn, amountIn, amountOut);
    }

    // -----------------------------------------------------------------------
    // PATTERN: Liquidity Removal
    // Burns LP shares and returns proportional amounts of both tokens.
    // -----------------------------------------------------------------------

    function removeLiquidity(uint256 shares)
        external
        returns (uint256 amountA, uint256 amountB)
    {
        require(shares > 0 && shares <= balanceOf[msg.sender], "INVALID_SHARES");

        amountA = (shares * reserveA) / totalSupply;
        amountB = (shares * reserveB) / totalSupply;

        balanceOf[msg.sender] -= shares;
        totalSupply -= shares;
        reserveA -= amountA;
        reserveB -= amountB;

        tokenA.transfer(msg.sender, amountA);
        tokenB.transfer(msg.sender, amountB);

        emit Burn(msg.sender, amountA, amountB, shares);
    }

    // -----------------------------------------------------------------------
    // PATTERN: Integer square root (Babylonian method)
    // Used for initial LP share calculation. Must be safe — no overflow.
    // -----------------------------------------------------------------------

    function _sqrt(uint256 x) internal pure returns (uint256 z) {
        if (x == 0) return 0;
        z = x;
        uint256 y = (z + 1) / 2;
        while (y < z) {
            z = y;
            y = (x / y + y) / 2;
        }
    }

    function _min(uint256 a, uint256 b) internal pure returns (uint256) {
        return a < b ? a : b;
    }
}
