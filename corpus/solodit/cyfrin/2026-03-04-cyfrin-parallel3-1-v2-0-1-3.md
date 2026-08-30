---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-1-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: Oracle Inconsistency between surplus computation and post-check causes `Surplus::processSurplus(collateralAddress,0)`
  DoS
vuln_class: []
---

# Oracle Inconsistency between surplus computation and post-check causes `Surplus::processSurplus(collateralAddress,0)` DoS

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** `LibSurplus::_computeCollateralSurplus` uses `LibOracle::readMint` (L88) to value collateral and compute the extractable surplus. `readMint` snaps the spot price to the target price when spot falls within the `userDeviation` band — for example, spot=1.07 gets snapped to target=1.10 if `userDeviation` is 5%.

The computed `collateralSurplus` is then swapped into tokenP via `Swapper::swapExactInput` (Surplus L55), which internally calls `_quoteMintExactInput` — also using `readMint`. Both the surplus sizing and the swap agree on the inflated valuation, so the swap succeeds and mints tokenP proportional to the snapped price.

The problem is the post-check. After the swap, `Surplus::processSurplus` calls `LibGetters::getCollateralRatio` (L59) to verify the system is still healthy. `getCollateralRatio` uses `LibOracle::readRedemption` (LibGetters L81), which passes `deviation=0` — no snapping, always raw spot. It sees the collateral at 1.07 (not 1.10), but the stables issued now include the extra tokenP minted at the inflated 1.10 rate. The resulting CR drops below `surplusBufferRatio` and the transaction reverts with `Undercollateralized`.

```solidity
// Surplus.sol L59-60
(uint64 collatRatio,,,,) = LibGetters.getCollateralRatio();
if (collatRatio < ts.surplusBufferRatio) revert Undercollateralized();
```

The root cause is that surplus computation and the swap use `readMint` (optimistic, snapped), while the safety check uses `readRedemption` (conservative, raw). When spot < target within the deviation band, these two oracles diverge — the surplus is sized for the snapped price but validated against the real one.

**Impact:** DoS on `Surplus::processSurplus(collateralAddress,0)` whenever spot is below target but within `userDeviation`.
The governor can partially work around it by passing maxCollateralAmount lower than the value computed in `LibSurplus::_computeCollateralSurplus` , which caps the extraction to what the CR can absorb. But this requires off-chain knowledge of the oracle divergence.

**Proof of Concept:** Added to `tests/units/Parallelizer.t.sol`. Run with:
`forge test --match-test "test_ProcessSurplus_RevertWhen_OracleInconsistency_SpotBelowTargetWithinDeviation" -vvvv`

```solidity
function test_ProcessSurplus_RevertWhen_OracleInconsistency_SpotBelowTargetWithinDeviation()
    public
    setZeroMintFeesOnAllCollaterals
{
    // --- Step 1: Mint 100 tokenP at oracle = 1.0 (default STABLE target, userDeviation=0) ---
    _mintZeroFee(address(eurA), 100 * BASE_6);

    // --- Step 2: Reconfigure eurA oracle: MAX target = 1.10, userDeviation = 5% ---
    AggregatorV3Interface[] memory circuitChainlink = new AggregatorV3Interface[](1);
    uint32[] memory stalePeriods = new uint32[](1);
    uint8[] memory circuitChainIsMultiplied = new uint8[](1);
    uint8[] memory chainlinkDecimals = new uint8[](1);
    circuitChainlink[0] = AggregatorV3Interface(address(oracleA));
    stalePeriods[0] = 1 hours;
    circuitChainIsMultiplied[0] = 1;
    chainlinkDecimals[0] = 8;
    OracleQuoteType quoteType = OracleQuoteType.UNIT;
    bytes memory readData =
      abi.encode(circuitChainlink, stalePeriods, circuitChainIsMultiplied, chainlinkDecimals, quoteType);
    bytes memory targetData = abi.encode(uint256(1.10e18));

    vm.startPrank(governor);
    parallelizer.setOracle(
      address(eurA),
      abi.encode(
        OracleReadType.CHAINLINK_FEEDS,
        OracleReadType.MAX,
        readData,
        targetData,
        abi.encode(uint128(5e16), uint128(0)) // userDeviation=5%, burnRatioDeviation=0
      )
    );
    vm.stopPrank();

    // --- Step 3: Drop spot price to 1.07 — below target (1.10) but within 5% deviation ---
    MockChainlinkOracle(address(oracleA)).setLatestAnswer(int256(1.07e8));

    // --- Step 4: Verify surplus exists (overestimated by readMint) ---
    (uint256 collateralSurplus, uint256 stableSurplus) = parallelizer.getCollateralSurplus(address(eurA));
    assertGt(collateralSurplus, 0, "Surplus should exist (readMint snaps to 1.10)");
    assertGt(stableSurplus, 0, "Stable surplus should exist");

    // --- Step 5: processSurplus reverts — oracle inconsistency → Undercollateralized ---
    _setSlippageTolerance(address(eurA), 1e8);
    vm.startPrank(governor);
    parallelizer.updateSurplusBufferRatio(uint64(BASE_9));

    vm.expectRevert(Undercollateralized.selector);
    parallelizer.processSurplus(address(eurA), 0);
    vm.stopPrank();
}
```

The `-vvvv` trace confirms the flow:

```
Surplus::processSurplus
  → readMint(oracleA) → snaps 1.07 → 1.10   // surplus = ~10 eurA
  → eurA::approve(Parallelizer, 9.09e6)
  → Swapper::swapExactInput                   // self-swap, readMint=1.10
    → eurA::transferFrom(self, self, 9.09e6)  // collateral stays in diamond
    → tokenP::mint(Parallelizer, 9.999e18)    // ~10 tokenP minted
  → getCollateralRatio()                       // post-check
    → readRedemption(oracleA) → raw 1.07      // no snapping
    → CR = 107e18 / 110e18 ≈ 0.972            // < surplusBufferRatio (1.0)
    └─ REVERT: Undercollateralized()
```

**Recommended Mitigation:** A complete fix requires resolving the oracle valuation in `LibSurplus::_computeCollateralSurplus` to conservatively compute the stable surplus, and readMint to back-convert to collateral (matching the swap execution price).

```diff
   function _computeCollateralSurplus(address collateral)
     internal
     view
     returns (uint256 collateralSurplus, uint256 stableSurplus)
   {
     ParallelizerStorage storage ts = s.transmuterStorage();
     Collateral storage collatInfo = ts.collaterals[collateral];
     uint256 currentCollateralBalance;
     if (collatInfo.isManaged > 0) {
       (, currentCollateralBalance) = LibManager.totalAssets(collatInfo.managerData.config);
     } else {
       currentCollateralBalance = IERC20(collateral).balanceOf(address(this));
     }
-    uint256 oracleValue = LibOracle.readMint(collatInfo.oracleConfig);
+    uint256 redemptionValue = LibOracle.readRedemption(collatInfo.oracleConfig);
+    uint256 mintValue = LibOracle.readMint(collatInfo.oracleConfig);
+    uint256 conservativeValue = redemptionValue < mintValue ? redemptionValue : mintValue;
     uint256 totalCollateralValue =
-      LibHelpers.convertDecimalTo(oracleValue * currentCollateralBalance, 18 + collatInfo.decimals, 18);
+      LibHelpers.convertDecimalTo(conservativeValue * currentCollateralBalance, 18 + collatInfo.decimals, 18);
     uint256 stablesBacked = (uint256(collatInfo.normalizedStables) * ts.normalizer) / BASE_27;
     if (totalCollateralValue <= stablesBacked) revert ZeroSurplusAmount();
     stableSurplus = totalCollateralValue - stablesBacked;
-    collateralSurplus = LibHelpers.convertDecimalTo((stableSurplus * BASE_18) / oracleValue, 18, collatInfo.decimals);
+    collateralSurplus = LibHelpers.convertDecimalTo((stableSurplus * BASE_18) / mintValue, 18, collatInfo.decimals);
   }
```
This adds non-trivial complexity.
As a practical alternative, the team can use the existing maxCollateralAmount parameter: compute the correct collateralSurplus off-chain using both oracle values and pass it to processSurplus, bypassing the on-chain overestimate.


**Parallel:** Fixed in commit [7d9d712](https://github.com/parallel-protocol/parallel-parallelizer/commit/7d9d712c7fcd3db8325424d932089b7f79ab8656).

**Cyfrin:** Verified. Fixed by implementing the recommended mitigation.
