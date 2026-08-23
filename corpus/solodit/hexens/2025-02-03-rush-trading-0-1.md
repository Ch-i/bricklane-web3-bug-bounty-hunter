---
affected_contracts: []
derives_from: []
id: solodit-hexens-2025-02-03-rush-trading-0-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-02-03T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-02-03-Rush-Trading.md
tags:
- firm:hexens
- report:2025-02-03-rush-trading
title: '[RUSH1-8] Utilisation ratio can exceed 100% to inflate fees and exploit the
  sponsor'
vuln_class: []
---

# [RUSH1-8] Utilisation ratio can exceed 100% to inflate fees and exploit the sponsor

_Section severity (from Solodit section header): High_  
_Audit firm: Hexens_  
_Source report: [2025-02-03-Rush-Trading.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-02-03-Rush-Trading.md)_

---

**Severity:** High

**Path:** FeeCalculator.sol:calculateFee#L55-L84

**Description:** The `calculateFee` function calculates the required fee for RushERC20 deployment by taking the liquidity amount, duration and utilisation ratio into account.

However, it receives the snapshotted total assets of the LiquidityPool as input for `params.totalLiquidity`. This means that it becomes possible to have a case where `params.outstandingLiquidity + params.newLiquidity > params.totalLiquidity`.

For example, consider the case when:

1. The snapshot of the assets in the liquidity is `1 wei`;

2. Someone deposits `1 ether` into the liquidity pool;

3. In the same block someone launches an ERC20 with `1 ether` as liquidity amount.

The utilisation ratio becomes `1e36` and the resulting fee also becomes much higher than the actual liquidity amount. Launching won’t revert, as the liquidity amount is available in the LiquidityPool.

This can be exploited against the sponsored launch of a RushERC20 in the RushRouterAlpha. The sponsor only pays the fees for a deployment of minimal liquidity amount and minimal liquidity duration. The resulting fee is assumed to be low in that case.

But by inflating the utilisation ratio, the sponsor will be paying far too much and lose funds. These funds will be distributed to the liquidity pool, where the attacker could be controlling the pool and gain those assets.

For the default parameters, with a minimum liquidity amount of `0.00001 ether` and minimum liquidity duration of `1 second`, the inflated fee becomes almost `6 ether` for every sponsored launch.

The reverse is also true for the fees of a normal launch. The snapshot of the total liquidity can be made very high for a single block to lower the fees in the next block.
```
    function calculateFee(FC.CalculateFeeParams calldata params)
        external
        view
        override
        returns (uint256 totalFee, uint256 reserveFee)
    {
        FC.CalculateFeeLocalVars memory vars;

        vars.feeRate = BASE_FEE_RATE;
        vars.utilizationRatio =
            Math.mulDiv(params.outstandingLiquidity + params.newLiquidity, 1e18, params.totalLiquidity); 
        if (vars.utilizationRatio > OPTIMAL_UTILIZATION_RATIO) {
            // If U > U_optimal, formula is:
            //                                                        U - U_optimal
            // R_fee = BASE_FEE_RATE + RATE_SLOPE_1 + RATE_SLOPE_2 * ----------------
            //                                                        1 - U_optimal
            vars.feeRate += RATE_SLOPE_1
                + Math.mulDiv(RATE_SLOPE_2, vars.utilizationRatio - OPTIMAL_UTILIZATION_RATIO, MAX_EXCESS_UTILIZATION_RATIO);
        } else {
            // Else, formula is:
            //                                             U
            // R_fee = BASE_FEE_RATE + RATE_SLOPE_1 *  -----------
            //                                          U_optimal
            vars.feeRate += Math.mulDiv(RATE_SLOPE_1, vars.utilizationRatio, OPTIMAL_UTILIZATION_RATIO);
        }

        totalFee = Math.mulDiv(vars.feeRate * params.duration, params.newLiquidity, 1e18);
        reserveFee = Math.mulDiv(totalFee, params.reserveFactor, 1e18);
    }
```
**Remediation:**  The utilisation ratio should be calculated using the:

- `max(actualTotalLiquidity, snapshotTotalLiquidity)` for the sponsored fee calculation in `RushRouterAlpha.sol` on lines 463-471.

- `min(actualTotalLiquidity, snapshotTotalLiquidity)` for the fee calculation in `LiquidityDeployer.sol` on lines 165-173.

**Status:**  Fixed

- - -
