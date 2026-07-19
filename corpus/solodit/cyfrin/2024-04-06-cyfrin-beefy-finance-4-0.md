---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-4-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Cache storage variables in memory when read multiple times without being changed
vuln_class: []
---

# Cache storage variables in memory when read multiple times without being changed

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** As reading from storage is considerably more expensive than reading from memory, cache storage variables in memory when read multiple times without being changed:

File: `StrategyPassiveManagerUniswap.sol`
```solidity
// @audit cache `vault` to save 2 storage reads;
// ideally `_onlyVault()` would return the vault
200:        if (_amount0 > 0) IERC20Metadata(lpToken0).safeTransfer(vault, _amount0);
201:        if (_amount1 > 0) IERC20Metadata(lpToken1).safeTransfer(vault, _amount1);

// @audit cache `positionMain.tickLower` to save 4 storage reads
// @audit cache `positionMain.tickUpper` to save 4 storage reads
// @audit cache `pool` to save ` storage read
220:            TickMath.getSqrtRatioAtTick(positionMain.tickLower),
221:            TickMath.getSqrtRatioAtTick(positionMain.tickUpper),
226:        bool amountsOk = _checkAmounts(liquidity, positionMain.tickLower, positionMain.tickUpper);
231:            IUniswapV3Pool(pool).mint(address(this), positionMain.tickLower, positionMain.tickUpper, liquidity, "Beefy Main");
239:            TickMath.getSqrtRatioAtTick(positionAlt.tickLower),
240:            TickMath.getSqrtRatioAtTick(positionAlt.tickUpper),
248:            IUniswapV3Pool(pool).mint(address(this), positionAlt.tickLower, positionAlt.tickUpper, liquidity, "Beefy Alt");

// @audit cache `pool' to save 5 storage reads
// @audit cache `positionMain.tickLower` to save 1 storage read
// @audit cache `positionAlt.tickUpper` to save 1 storage read
259:        (uint128 liquidity,,,,) = IUniswapV3Pool(pool).positions(keyMain);
260:        (uint128 liquidityAlt,,,,) = IUniswapV3Pool(pool).positions(keyAlt);
264:            IUniswapV3Pool(pool).burn(positionMain.tickLower, positionMain.tickUpper, liquidity);
265:            IUniswapV3Pool(pool).collect(address(this), positionMain.tickLower, positionMain.tickUpper, type(uint128).max, type(uint128).max);
269:            IUniswapV3Pool(pool).burn(positionAlt.tickLower, positionAlt.tickUpper, liquidityAlt);
270:            IUniswapV3Pool(pool).collect(address(this), positionAlt.tickLower, positionAlt.tickUpper, type(uint128).max, type(uint128).max);

// @audit cache `pool' to save 5 storage reads
// @audit cache `positionMain.tickLower` to save 1 storage read
// @audit cache `positionAlt.tickUpper` to save 1 storage read
338:        (uint128 liquidity,,,,) = IUniswapV3Pool(pool).positions(keyMain);
339:        (uint128 liquidityAlt,,,,) = IUniswapV3Pool(pool).positions(keyAlt);
342:        if (liquidity > 0) IUniswapV3Pool(pool).burn(positionMain.tickLower, positionMain.tickUpper, 0);
343:        if (liquidityAlt > 0) IUniswapV3Pool(pool).burn(positionAlt.tickLower, positionAlt.tickUpper, 0);
346:        (uint256 fee0, uint256 fee1) = IUniswapV3Pool(pool).collect(address(this), positionMain.tickLower, positionMain.tickUpper, type(uint128).max, type(uint128).max);
347:        (uint256 feeAlt0, uint256 feeAlt1) = IUniswapV3Pool(pool).collect(address(this), positionAlt.tickLower, positionAlt.tickUpper, type(uint128).max, type(uint128).max);

// @audit cache `pool` to save 1 storage read
453:        (uint128 liquidity,,,uint256 owed0, uint256 owed1) = IUniswapV3Pool(pool).positions(keyMain);
454:        (uint128 altLiquidity,,,uint256 altOwed0, uint256 altOwed1) =IUniswapV3Pool(pool).positions(keyAlt);

// @audit cache `pool` to save 2 storage reads
562:        if (msg.sender != pool) revert NotPool();
565:        if (amount0 > 0) IERC20Metadata(lpToken0).safeTransfer(pool, amount0);
566:        if (amount1 > 0) IERC20Metadata(lpToken1).safeTransfer(pool, amount1);

// @audit cache `twapInterval` to save 1 storage read
696:        secondsAgo[0] = uint32(twapInterval);
700:        twapTick = (tickCuml[1] - tickCuml[0]) / twapInterval;
```

File: `BeefyQIVault.sol`
```solidity
// @audit cache `rewardTokens[i]` to save 2 storage reads
211:                        uint256 bal = IERC20(rewardTokens[i]).balanceOf(address(this));
212:                        if (bal > 0 && rewardTokens[i] != native) {
213:                                BeefyBalancerStructs.Reward storage reward = rewards[rewardTokens[i]];

// @audit cache `rewardTokens[i]` to save 2 storage reads
371:                        IERC20(rewardTokens[i]).approve(rewards[rewardTokens[i]].router, 0);
372:                        delete rewards[rewardTokens[i]];

// @audit cache 'rewardPool` to save 1 storage read
390:                emit UpdatedRewardPool(rewardPool, _rewardPool);
392:                IERC20(qibpt).approve(rewardPool, 0);
```

**Beefy:**
Acknowledged.
