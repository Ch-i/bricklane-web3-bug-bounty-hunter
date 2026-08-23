---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-1-7
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Precision loss can result in funds becoming stuck in incentive logic contracts
vuln_class: []
---

# Precision loss can result in funds becoming stuck in incentive logic contracts

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** In all three incentive logic contracts, the `ratePerSec` of deposited rewards is computed by performing a division of the `amount` to distribute by the `duration`:

```solidity
    function depositRewards(IncentivizedPoolId id, address token, uint256 amount, uint256 duration)
        external
        override
        nonReentrant
    {
        ...
        uint32 endTimestampCache = _state.endTimestamp;
        if (endTimestampCache < block.timestamp) {
            if (duration < MIN_DURATION) revert InvalidDuration();

            if (endTimestampCache == 0) poolRewards[id].push(token);

            // Calculate the rate
@>          uint256 rate = amount / duration;

            ...
        }
    }
```

If the token to distribute has a small amount of decimals, this can result in a "dust" amount accumulating that will never be distributed and ultimately remain locked in the contract. Considering WBTC on Ethereum, taking note of the fact that it has only 8 decimals and a large value per token, the value stuck in the contract can be significant.

This is additionally problematic for calculations performed to extend the duration of distribution, where the precision loss in `ratePerSec` is amplified when calculating the leftover rewards and updated rate:

```solidity
// Calculates the leftover rewards from the current distribution
uint96 ratePerSecCache = _state.ratePerSec;
uint256 leftoverRewards = ratePerSecCache * remainingDuration;

// Calculates the new rate
uint256 newRate = (amount + leftoverRewards) / newDuration;
if (newRate < ratePerSecCache) revert CannotReduceRate();
```

The amount lost due to down rounding will not be considered here, meaning the actual leftover rewards will exceed the calculated value. Calculation of the new rate is again affected by precision loss due to down rounding.

**Proof of Concept:** In the following example, a user attempts to distribute $10,000 worth of WBTC over a reasonable 10 week duration. In reality, $5,382 worth of WBTC is distributed while the remaining $4,618 gets stuck in the contract and will be never retrievable by anyone.

The following tests should be placed in `BasicIncentiveLogic.t.sol`:

```solidity
function test_DustAmountsLost() public {
    uint256 currentBTCValueInDollars = 89000;
    uint256 amountInDollarsToDeposit = 10000;       // 10k dollars to distribute
    uint256 btcAmount = amountInDollarsToDeposit * 10**8 / currentBTCValueInDollars;
    uint256 distributionDuration = 10 weeks;        // 10 weeks of distribution

    MockERC20 wbtc = new MockERC20("WBTC", "WBTC", 8);
    wbtc.mint(address(this), btcAmount);
    wbtc.approve(address(logic), type(uint256).max);

    PoolId poolKey;
    IncentivizedPoolId poolId;
    address lpToken = address(7);

    poolKey = createPoolKey(address(1), address(2), 3000).toId();
    poolId = IncentivizedPoolKey({ id: poolKey, lpToken: lpToken }).toId();

    manager.setListedPool(poolId, true);
    logic.updateDefaultFee(0);

    address[] memory systems = new address[](1);
    systems[0] = address(logic);

    manager.notifyAddLiquidty(systems, poolKey, lpToken, user1, int256(1 ether));

    logic.depositRewards(poolId, address(wbtc), btcAmount, distributionDuration);

    skip(10 weeks);

    // Since user1 is the only liquidity provider they own all rewards of the pool and given that all
    // distribution window has already elapsed, this is the full amount that will be distributed
    uint256 valueDistributedInDollars = logic.earned(poolId, address(wbtc), user1) * currentBTCValueInDollars / (10**8);
    uint256 valueLockedDueToRoundingInDollars = amountInDollarsToDeposit - valueDistributedInDollars;

    console.log("Value distributed:", valueDistributedInDollars);
    console.log("Value locked:", valueLockedDueToRoundingInDollars);
}

function test_ExtensionPrecisionLoss() public {
    uint256 currentBTCValueInDollars = 89000;
    uint256 amountInDollarsToDeposit = 10000;       // 10k dollars to distribute
    uint256 btcAmount = amountInDollarsToDeposit * 10**8 / currentBTCValueInDollars;
    uint256 distributionDuration = 10 weeks;        // 10 weeks of distribution

    MockERC20 wbtc = new MockERC20("WBTC", "WBTC", 8);
    wbtc.mint(address(this), btcAmount);
    wbtc.approve(address(logic), type(uint256).max);

    PoolId poolKey;
    IncentivizedPoolId poolId;
    address lpToken = address(7);

    poolKey = createPoolKey(address(1), address(2), 3000).toId();
    poolId = IncentivizedPoolKey({ id: poolKey, lpToken: lpToken }).toId();

    manager.setListedPool(poolId, true);
    logic.updateDefaultFee(0);

    address[] memory systems = new address[](1);
    systems[0] = address(logic);

    manager.notifyAddLiquidty(systems, poolKey, lpToken, user1, int256(1 ether));

    logic.depositRewards(poolId, address(wbtc), btcAmount, distributionDuration);

    uint256 initialDuration = 2 weeks;
    skip(initialDuration);

    wbtc.mint(address(this), btcAmount);
    // extend distribution by depositing the same amount again
    logic.depositRewards(poolId, address(wbtc), btcAmount, distributionDuration);

    skip(2 * distributionDuration - initialDuration);

    // Since user1 is the only liquidity provider they own all rewards of the pool and given that all
    // distribution window has already elapsed, this is the full amount that will be distributed
    uint256 valueDistributedInDollars = logic.earned(poolId, address(wbtc), user1) * currentBTCValueInDollars / (10**8);
    uint256 valueLockedDueToRoundingInDollars = 2 * amountInDollarsToDeposit - valueDistributedInDollars;

    console.log("Value distributed:", valueDistributedInDollars);
    console.log("Value locked:", valueLockedDueToRoundingInDollars);
}
```

Output:
```bash
Ran 2 tests for test/BasicIncentiveLogic.t.sol:TestBasicIncentiveLogic
[PASS] test_DustAmountsLost() (gas: 1195208)
Logs:
  Value distributed: 5382
  Value locked: 4618

[PASS] test_ExtensionPrecisionLoss() (gas: 1214484)
Logs:
  Value distributed: 10765
  Value locked: 9235
```

**Impact:** There is a high likelihood of significant loss of funds.

**Recommended Mitigation:** Consider preventing reward amounts that will result in the accumulation of dust from being deposited for initial distributions:

```diff
    function depositRewards(IncentivizedPoolId id, address token, uint256 amount, uint256 duration)
        external
        override
        nonReentrant
    {
        if (amount == 0) revert NullAmount();
++      if (amount % duration != 0) revert RemainingDust();
        if (!IncentiveManager(incentiveManager).isListedPool(id)) revert InvalidPool();

        ...
    }
```

When existing distributions are to be extended, similarly consider preventing dust amounts from accumulating by again checking the modulus:

```diff
    // Calculates the leftover rewards from the current distribution
    uint96 ratePerSecCache = _state.ratePerSec;
    uint256 leftoverRewards = ratePerSecCache * remainingDuration;

    // Calculates the new rate
++  if (amount + leftoverRewards % newDuration != 0) revert RemainingDust();
    uint256 newRate = (amount + leftoverRewards) / newDuration;
    if (newRate < ratePerSecCache) revert CannotReduceRate();
```

**Paladin:** Fixed by commit [`74060d7`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/74060d7a58161588c9f9a6791d70ef2745a155b3). Decided not to fully revert for any small amount of dust, as this could block some integrations, and be wronged by the fee taken or simply by another malicious actor frontrunning the deposit to deposit more rewards and make the call fail.
Instead we “accept” a certain percentage of dust lost due to imprecision.

**Cyfrin:** Verified. Additional validation is now performed to ensure that no more than 1% of the distributed rewards can accumulate as dust amounts. Note that this can still be significant equivalent dollar value for distributions of high value tokens with low decimals (e.g. WBTC).
