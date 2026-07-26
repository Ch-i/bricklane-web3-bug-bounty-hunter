---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-3-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: '`LibHelpers.convertDecimalsTo` favours the user on a exact-out mint and burn
  for certain collateral decimals'
vuln_class: []
---

# `LibHelpers.convertDecimalsTo` favours the user on a exact-out mint and burn for certain collateral decimals

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** Function `convertToDecimals` favours user on the exact-out mint path of `Swapper::swap`. It always rounds down when converting from higher decimals to lower decimals

```solidity
function _quoteMintExactOutput(
...
@@> amountIn = LibHelpers.convertDecimalTo((amountIn * BASE_18) / oracleValue, 18, collatInfo.decimals);
```

For the exact-out burn path it is collaterals with decimals higher than 18 that get a small discount. Here

```solidity
function _quoteBurnExactOutput(
...
@@> amountIn = Math.mulDiv(LibHelpers.convertDecimalTo(amountOut, collatInfo.decimals, 18), oracleValue, ratio);
```
**Impact:** The rounding error of a mint with low decimals violates the maxim "rounding should always favour the protocol".

In this case it gives a negligible advantage to the user and no way to exploit this in a meaningful way has been found.

However, the addition of extra features to the codebase may allow exploitation in the future.

**Proof of Concept:** See tests `test_cyfrin_[mint/burn]ExactOutput_[low/high]Decimals_userFavorableRounding` in tests/units/parallel-protocolSwapperDecimalRounding.t.sol
```solidity

// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.28;

import { IERC20 } from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import { console2 } from "@forge-std/console2.sol";
import { AggregatorV3Interface } from "contracts/interfaces/external/chainlink/AggregatorV3Interface.sol";
import "contracts/utils/Constants.sol";
import "contracts/parallelizer/Storage.sol";

import "../Fixture.sol";
import { MockChainlinkOracle } from "../mock/MockChainlinkOracle.sol";
import { MockTokenPermit } from "../mock/MockTokenPermit.sol";
import { DecimalString } from "../utils/DecimalString.sol";

contract CyfrinSwapperDecimalRoundingTest is Fixture {
  using DecimalString for uint256;

  IERC20 internal eurZ;
  AggregatorV3Interface internal oracleZ;

  function setUp() public override {
    super.setUp();

    // Normalize oracles to 1.0 (8 decimals) to isolate rounding from price effects.
    MockChainlinkOracle(address(oracleA)).setLatestAnswer(100_000_000);
    MockChainlinkOracle(address(oracleY)).setLatestAnswer(100_000_000);

    // Zero mint/burn fees on both collaterals so the only nonlinearity is decimal rounding.
    uint64[] memory xFeeMint = new uint64[](1);
    int64[] memory yFeeMint = new int64[](1);
    xFeeMint[0] = 0;
    yFeeMint[0] = 0;
    uint64[] memory xFeeBurn = new uint64[](1);
    int64[] memory yFeeBurn = new int64[](1);
    xFeeBurn[0] = uint64(BASE_9);
    yFeeBurn[0] = 0;

    vm.startPrank(guardian);
    parallelizer.setFees(address(eurA), xFeeMint, yFeeMint, true);
    parallelizer.setFees(address(eurA), xFeeBurn, yFeeBurn, false);
    parallelizer.setFees(address(eurY), xFeeMint, yFeeMint, true);
    parallelizer.setFees(address(eurY), xFeeBurn, yFeeBurn, false);
    vm.stopPrank();

    // Add a 27-decimal collateral for the exact input test.
    eurZ = IERC20(address(new MockTokenPermit("EUR_Z", "EUR_Z", 27)));
    oracleZ = AggregatorV3Interface(address(new MockChainlinkOracle()));
    MockChainlinkOracle(address(oracleZ)).setLatestAnswer(100_000_000);

    vm.startPrank(governor);
    parallelizer.addCollateral(address(eurZ));
    _setOracleStable(address(eurZ), address(oracleZ));
    vm.stopPrank();

    vm.startPrank(guardian);
    parallelizer.setFees(address(eurZ), xFeeMint, yFeeMint, true);
    parallelizer.setFees(address(eurZ), xFeeBurn, yFeeBurn, false);
    parallelizer.setStablecoinCap(address(eurZ), type(uint256).max);
    parallelizer.togglePause(address(eurZ), ActionType.Mint);
    parallelizer.togglePause(address(eurZ), ActionType.Burn);
    vm.stopPrank();
  }

  function _setOracleStable(address collateral, address oracle) internal {
    AggregatorV3Interface[] memory circuitChainlink = new AggregatorV3Interface[](1);
    uint32[] memory stalePeriods = new uint32[](1);
    uint8[] memory circuitChainIsMultiplied = new uint8[](1);
    uint8[] memory chainlinkDecimals = new uint8[](1);
    circuitChainlink[0] = AggregatorV3Interface(oracle);
    stalePeriods[0] = 1 hours;
    circuitChainIsMultiplied[0] = 1;
    chainlinkDecimals[0] = 8;
    OracleQuoteType quoteType = OracleQuoteType.UNIT;
    bytes memory readData =
      abi.encode(circuitChainlink, stalePeriods, circuitChainIsMultiplied, chainlinkDecimals, quoteType);
    bytes memory targetData;
    parallelizer.setOracle(
      collateral,
      abi.encode(
        OracleReadType.CHAINLINK_FEEDS, OracleReadType.STABLE, readData, targetData, abi.encode(uint128(0), uint128(0))
      )
    );
  }

  function _mintExactOutputAndGetSpent(address tokenIn, address owner, uint256 amountOut)
    internal
    returns (uint256 spent)
  {
    deal(tokenIn, owner, type(uint128).max); // really large amount
    uint256 beforeBal = IERC20(tokenIn).balanceOf(owner);
    vm.startPrank(owner);
    IERC20(tokenIn).approve(address(parallelizer), type(uint256).max);
    parallelizer.swapExactOutput(amountOut, type(uint256).max, tokenIn, address(tokenP), owner, block.timestamp * 2);
    vm.stopPrank();
    spent = beforeBal - IERC20(tokenIn).balanceOf(owner);
  }

  function test_cyfrin_mintExactOutput_lowDecimals_userFavorableRounding() external {
    // Maximize rounding delta: choose amountOut with remainder (1e12 - 1) when divided by 1e12.
    // This makes the 6-decimal path floor by almost 1e12 units (in 18-decimal terms).
    uint256 amountOut = 1e24 + (1e12 - 1);

    uint256 quote6 = parallelizer.quoteOut(amountOut, address(eurA), address(tokenP));
    uint256 spent6 = _mintExactOutputAndGetSpent(address(eurA), alice, amountOut);

    uint256 quote18 = parallelizer.quoteOut(amountOut, address(eurY), address(tokenP));
    uint256 spent18 = _mintExactOutputAndGetSpent(address(eurY), alice, amountOut);

    // Normalize 6-decimals collateral into 18-decimals for apples-to-apples comparison.
    uint256 cost6In18 = spent6 * 1e12;
    uint256 cost18In18 = spent18;

    console2.log("Mint exact output comparison (same amountOut):");
    console2.log(string.concat("amountOut (TokenP, 18 dec) = ", amountOut.formatFixed(18)));
    console2.log(string.concat("collateral 6-dec (eurA) spent = ", spent6.formatFixed(6)));
    console2.log(string.concat("collateral 18-dec (eurY) spent = ", spent18.formatFixed(18)));
    console2.log(string.concat("eurA cost normalized to 18 dec = ", cost6In18.formatFixed(18)));
    console2.log(string.concat("eurY cost (18 dec) = ", cost18In18.formatFixed(18)));
    console2.log(string.concat("rounding delta (18 dec units) = ", (cost18In18 - cost6In18).formatFixed(18)));

    // Rounding in convertDecimalTo(18 -> 6) floors, making the 6-decimals mint slightly cheaper.
    assertLt(cost6In18, cost18In18);
  }


  function test_cyfrin_burnExactOutput_highDecimals_userFavorableRounding() external {
    // Choose amountOut for 27-dec collateral with remainder (1e9 - 1) to maximize rounding down
    // when converting 27 -> 18, reducing the TokenP required.
    uint256 amountOut18 = 1_000_000e18;
    uint256 amountOut27 = amountOut18 * 1e9 + (1e9 - 1);

    // Mint TokenP from each collateral to seed normalizedStables for burns.
    _mintExactInput(alice, address(eurZ), amountOut27, 0);
    _mintExactInput(alice, address(eurY), amountOut18, 0);

    // Fund the Parallelizer with collateral to pay out on burn.
    deal(address(eurY), address(parallelizer), amountOut18);
    deal(address(eurZ), address(parallelizer), amountOut27);

    uint256 expectedIn27 = amountOut18; // floor(amountOut27 / 1e9)

    vm.startPrank(alice);
    uint256 in27 =
      parallelizer.swapExactOutput(amountOut27, type(uint256).max, address(tokenP), address(eurZ), alice, block.timestamp * 2);
    uint256 in18 =
      parallelizer.swapExactOutput(amountOut18, type(uint256).max, address(tokenP), address(eurY), alice, block.timestamp * 2);
    vm.stopPrank();

    uint256 extraOut27 = amountOut27 - amountOut18 * 1e9;

    console2.log("Exact output burn comparison (27-dec vs 18-dec collateral):");
    console2.log(string.concat("amountOut27 (EUR_Z, 27 dec) = ", amountOut27.formatFixed(27)));
    console2.log(string.concat("amountOut18 (EUR_Y, 18 dec) = ", amountOut18.formatFixed(18)));
    console2.log(string.concat("tokenP in for 27-dec collateral = ", in27.formatFixed(18)));
    console2.log(string.concat("tokenP in for 18-dec collateral = ", in18.formatFixed(18)));
    console2.log(string.concat("extra collateral gained (27-dec units) = ", extraOut27.formatFixed(27)));

    // 27-dec path rounds down in 27 -> 18 conversion, so it needs the same TokenP
    // as the 18-dec path while delivering slightly more collateral.
    assertEq(in27, expectedIn27);
    assertEq(in18, amountOut18);
    assertEq(in27, in18);
    assertEq(extraOut27, 1e9 - 1);
  }

  function test_cyfrin_exactInput_27Decimals_roundingCanWasteInput() external {
    // Choose an amountIn with remainder (1e9 - 1) when divided by 1e9 to maximize rounding loss
    // in the 27-decimal -> 18-decimal conversion.
    uint256 amountIn27 = 1e27 + (1e9 - 1);
    uint256 amountIn18 = 1e18;

    deal(address(eurZ), alice, amountIn27);
    deal(address(eurY), alice, amountIn18);

    vm.startPrank(alice);
    eurZ.approve(address(parallelizer), type(uint256).max);
    eurY.approve(address(parallelizer), type(uint256).max);
    uint256 out27 = parallelizer.swapExactInput(amountIn27, 0, address(eurZ), address(tokenP), alice, block.timestamp * 2);
    uint256 out18 = parallelizer.swapExactInput(amountIn18, 0, address(eurY), address(tokenP), alice, block.timestamp * 2);
    vm.stopPrank();

    uint256 idealOut27 = (amountIn27 + (1e9 - 1)) / 1e9;
    uint256 roundingLoss = idealOut27 - out27;

    console2.log("Exact input comparison (27-dec vs 18-dec collateral):");
    console2.log(string.concat("amountIn27 (EUR_Z, 27 dec) = ", amountIn27.formatFixed(27)));
    console2.log(string.concat("amountIn18 (EUR_Y, 18 dec) = ", amountIn18.formatFixed(18)));
    console2.log(string.concat("out27 (TokenP, 18 dec) = ", out27.formatFixed(18)));
    console2.log(string.concat("out18 (TokenP, 18 dec) = ", out18.formatFixed(18)));
    console2.log(string.concat("idealOut27 (ceil, 18 dec) = ", idealOut27.formatFixed(18)));
    console2.log(string.concat("roundingLoss (TokenP wei) = ", roundingLoss.formatFixed(18)));

    // The 27-decimal path floors, so it loses up to 1 TokenP wei vs a ceiling conversion.
    assertEq(out27 + roundingLoss, idealOut27);
    assertEq(roundingLoss, 1);
  }

}
```

```
[PASS] test_cyfrin_mintExactOutput_lowDecimals_userFavorableRounding() (gas: 735829)
Logs:
  Mint exact output comparison (same amountOut):
  amountOut (TokenP, 18 dec) = 1,000,000.000000999999999999
  collateral 6-dec (eurA) spent = 1,000,000.000000
  collateral 18-dec (eurY) spent = 1,000,000.000000999999999999
  eurA cost normalized to 18 dec = 1,000,000.000000000000000000
  eurY cost (18 dec) = 1,000,000.000000999999999999
  rounding delta (18 dec units) = 0.000000999999999999```
```

```
[PASS] test_cyfrin_burnExactOutput_highDecimals_userFavorableRounding() (gas: 1288290)
Logs:
  Exact output burn comparison (27-dec vs 18-dec collateral):
  amountOut27 (EUR_Z, 27 dec) = 1,000,000.000000000000000000999999999
  amountOut18 (EUR_Y, 18 dec) = 1,000,000.000000000000000000
  tokenP in for 27-dec collateral = 1,000,000.000000000000000000
  tokenP in for 18-dec collateral = 1,000,000.000000000000000000
  extra collateral gained (27-dec units) = 0.000000000000000000999999999
```

**Recommended Mitigation:** Modify `convertDecimalsTo` to include a parameter for the rounding direction and use appropriately.

**Parallel:** Fixed in commit [f60101a](https://github.com/parallel-protocol/parallel-parallelizer/commit/f60101a455c9215c49a7ea70551da7d31ca5ca76).

**Cyfrin:** Verified. `LibHelpers.convertDecimalsTo` now rounds towards the specified direction when converting from higher decimals to lower decimals.
