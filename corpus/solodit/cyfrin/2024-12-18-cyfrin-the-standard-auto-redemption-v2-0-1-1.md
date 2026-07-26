---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: Automation and redemption could be artificially manipulated due to use of instantaneous
  `sqrtPriceX96`
vuln_class: []
---

# Automation and redemption could be artificially manipulated due to use of instantaneous `sqrtPriceX96`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** `AutoRedemption::checkUpkeep` is queried every block by the Chainlink Automation DON:

```solidity
function checkUpkeep(bytes calldata checkData) external returns (bool upkeepNeeded, bytes memory performData) {
    (uint160 sqrtPriceX96,,,,,,) = pool.slot0();
    upkeepNeeded = sqrtPriceX96 <= triggerPrice;
}
```

However, use of `sqrtPriceX96` is problematic since it is based on the instantaneous pool reserves which can be manipulated to force upkeep into triggering even if it is not required. Additionally, this instantaneous price is used in calculation of the `USDs` that needs to be bought to reach the target price:

```solidity
function calculateUSDsToTargetPrice() private view returns (uint256 _usdc) {
    int24 _spacing = pool.tickSpacing();
    (uint160 _sqrtPriceX96, int24 _tick,,,,,) = pool.slot0();
    int24 _upperTick = _tick / _spacing * _spacing;
    int24 _lowerTick = _upperTick - _spacing;
    uint128 _liquidity = pool.liquidity();
    ...
}
```

So despite the latency between checking and fulfilling upkeep, and additional latency in fulfilling the Functions request, the `USDs` price can be manipulated without relying on multi-block manipulation. Combined with an attacker providing just-in-time (JIT) liquidity, the calculation can be manipulated to redeem the entire debt of a vault as capped within `AutoRedemption::fulfillRequest`:

```solidity
if (_USDsTargetAmount > _vaultData.status.minted) _USDsTargetAmount = _vaultData.status.minted;
```

**Impact:** A vault owner could manipulate the `USDs`/`USDC` pool reserves to force auto redemption even if it is not required. If their vault is the one returned by the off-chain service, they will have caused their debt to be repaid while circumventing fees. Note that other MEV attacks that have not been explored in this analysis may also be possible.

**Recommended Mitigation:** Re-check the upkeep condition within `AutoRedemption::performUpkeep` and `AutoRedemption::fulfilRequest` to minimize the impact of isolated price oracle manipulation; however, note that repeated manipulation does not necessarily require multi-block manipulation. Therefore, additionally consider consuming a time-weighted average price or work with Chainlink Labs to create a decentralized `USDs` price oracle.

**The Standard DAO:** Fixed by commit [5ec532e](https://github.com/the-standard/smart-vault/commit/5ec532e5f3813a865102501dbb91cf13a0813930).

**Cyfrin:** The trigger condition is re-checked and a TWAP has been implemented; however, it is recommended to use a substantially large interval (at least 900 seconds, if not 1800 seconds) to protect against manipulation. Note: Uniswap V3 pool oracles are not multi-block MEV resistant.

**The Standard DAO:** Fixed by commit [a8cdc77](https://github.com/the-standard/smart-vault/commit/a8cdc77d1fac9817128e1f3c1c8a1ab57f715513).

**Cyfrin:** Verified. The TWAP interval has been increased.
