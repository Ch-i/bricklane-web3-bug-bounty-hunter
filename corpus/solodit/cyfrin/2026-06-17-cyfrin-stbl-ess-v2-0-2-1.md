---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`STBL_XLayer_Wrapper::ess_deposit` permanently reverts for non 18-decimal
  tokens'
vuln_class: []
---

# `STBL_XLayer_Wrapper::ess_deposit` permanently reverts for non 18-decimal tokens

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_ESS_Wrapper1::iCalculateRatios` splits a USD deposit amount across each basket asset by its configured ratio and calls `iSTBL_Issuer.deriveAssetValue(individualAmt)` to convert each USD share into the required token quantity. The resulting array is forwarded to `asset_issue`, which calls `IERC20(token).transferFrom(msg.sender, address(this), amounts[i])` and `iSTBL_Issuer.deposit(amounts[i])` treating each element as a native ERC20 token unit count.

```solidity
// STBL_ESS_Wrapper1.sol lines 308-312
uint256 individualAmts = (_amt * Ratios[assetIDs[i]].ratio) / FEES_CONSTANT;
amounts[i] = iSTBL_Issuer(Ratios[assetIDs[i]].issuer).deriveAssetValue(individualAmts);
```

```solidity
// STBL_ESS_Wrapper1.sol line 169-173
IERC20(Ratios[assetIDs[i]].token).transferFrom(
    msg.sender, address(this), _amount[i]  // _amount[i] treated as native units
);
```

The `_amt` parameter is unambiguously 18-decimal. The concrete wrapper documents it as "the amount of ESS tokens to mint" (`STBL_XLayer_Wrapper.sol:99`) and the abstract base documents it as "the total USD-denominated amount the user wishes to deposit" (`_Wrapper_ess_deposit:236`) — ESS is an 18-decimal token and the protocol's USD unit (USST) is also 18-decimal.
The wrapper is designed to handle a basket of assets with heterogeneous decimals (e.g., USDC at 6, USDT at 8, SUSD at 18 simultaneously). A single `_amt` parameter cannot be expressed in any one token's native decimals when the basket spans multiple decimal counts; the only coherent shared denomination is the protocol's 18-decimal USD unit. There is no alternative interpretation.

The concrete issuer for XLayer deployments, `STBL_XLayer_Asset_Issuer::deriveAssetValue`, converts the USD input to a token quantity via oracle division:

```solidity
return (adjustedAmt * (10 ** priceDecimals)) / oraclePrice;
```

With the oracle returning `priceDecimals = 18`, this formula always produces a result in 18-decimal representation regardless of the underlying token's decimal count.
- For an 18-decimal token the output coincidentally equals the correct native unit count.
- But, for a 6-decimal token such as USDC or USDT priced at $1 — `oraclePrice = 1e18`, `priceDecimals = 18` — a $1 input (`1e18`) yields `(1e18 × 1e18) / 1e18 = 1e18`. The correct native USDC quantity for $1 is `1e6`. The result is `10^12` times larger than any realistic user balance or allowance. T


**Impact:** Every `ess_deposit` call for a basket containing a non-18-decimal token fails permanently — no funds are lost, but the ESS minting path is entirely unavailable for non-18-decimal tokens

**Proof of Concept:** `test_poc_sixDecimalToken_DoS` — deploys a 6-decimal mock token (USDC stand-in) with a $1.00 oracle, configures a single-asset wrapper basket for it, funds a user with 10,000 USDC (10,000e6 native units), and calls `ess_deposit(1000e18)`. Logs the inflated transfer amount (1000e18 + 1, the 18-decimal oracle result) against the correct native amount (1000e6) — an inflation factor of exactly 10^12. Asserts the deposit reverts and the user's balance is unchanged.
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./XLayer_Setup.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/**
 * @title  SixDecimalToken_DoS_PoC
 * @notice Title:    ess_deposit permanent DoS for 6-decimal tokens
 * @notice Affected: STBL_ESS_Wrapper1.iCalculateRatios / STBL_XLayer_Asset_Issuer.deriveAssetValue
 * @notice Impact:   Permanent revert in ess_deposit for any basket containing a 6-decimal token
 * @notice Author:   0xStalin
 */

// == [ 6-Decimal Mock Token ] ==

/**
 * @dev In-file mock ERC20 with 6 decimals — simulates USDC/USDT.
 *      Mirrors STBL_TestToken but overrides decimals() to return 6.
 */
contract STBL_6Dec_TestToken is ERC20 {
    constructor() ERC20("Mock USDC", "mUSDC") {}

    function mint(address account) external {
        _mint(account, 10_000 * 10 ** 6);
    }

    function mintVal(address account, uint256 _value) external {
        _mint(account, _value);
    }

    function decimals() public view virtual override returns (uint8) {
        return 6;
    }
}

// == [ PoC Contract ] ==

contract SixDecimalToken_DoS_PoC is XLayer_Setup {
    // Asset 3 — 6-decimal token, $1.00 price, 100% ratio
    STBL_6Dec_TestToken public testToken3;
    STBL_TestOracle     public testOracle3;
    STBL_XLayer_Asset_Issuer public issuer3;
    STBL_XLayer_Asset_Vault  public vault3;
    STBL_XLayer_Asset_YieldDistributor public yieldDistributor3;
    ERC1967Proxy public issuerProxy3;
    ERC1967Proxy public vaultProxy3;
    ERC1967Proxy public yieldDistributorProxy3;
    uint256 public assetId3;

    // Dedicated 6-dec wrapper
    STBL_XLayer_Wrapper public sixDecWrapper;
    ERC1967Proxy        public sixDecWrapperProxy;

    // Oracle price for Asset3: $1.00 expressed with 18 decimals
    uint256 constant ASSET3_PRICE = 1e18;

    // 100% ratio — expressed relative to FEES_CONSTANT (10^9)
    uint256 constant ASSET3_RATIO = FEES_CONSTANT;

    // Deposit expressed in 18-decimal USD units ($1,000)
    uint256 constant DEPOSIT_USD = 1_000e18;

    // Correct 6-dec native quantity for $1,000 at $1/token
    uint256 constant CORRECT_NATIVE_AMT = 1_000e6;

    function setUp() public override {
        // Deploy all base infrastructure (assets 1 & 2, main wrapper, NFT vault)
        super.setUp();

        vm.startPrank(admin);

        // == [ Setup: Deploy Asset3 (6-dec) + Dedicated 6-Dec Wrapper ] ==

        // Step 1 — deploy the 6-dec token and its $1.00 oracle
        testToken3  = new STBL_6Dec_TestToken();  // nonce N+0
        testOracle3 = new STBL_TestOracle(ASSET3_PRICE); // nonce N+1

        // Step 2 — register Asset3
        assetId3 = registry.addAsset("Asset3", "Mock USDC 6-dec", 1, false);

        // Step 3 — pre-compute the 6-dec wrapper proxy address so the issuer
        //          can be initialised with the correct wrapper address.
        //
        //  Remaining deployments in this setUp() after this line:
        //    N+0  issuerImpl3
        //    N+1  issuerProxy3
        //    N+2  vaultImpl3
        //    N+3  vaultProxy3
        //    N+4  ydImpl3
        //    N+5  ydProxy3
        //    N+6  wrapperImpl6dec
        //    N+7  sixDecWrapperProxy  <-- this is what we precompute
        uint64 nonceNow = vm.getNonce(admin);
        address predictedSixDecWrapperProxy = vm.computeCreateAddress(admin, nonceNow + 7);

        // Step 4 — deploy issuer proxy for Asset3, pointing at the predicted wrapper
        STBL_XLayer_Asset_Issuer issuerImpl3 = new STBL_XLayer_Asset_Issuer(); // N+0
        issuerProxy3 = new ERC1967Proxy(                                        // N+1
            address(issuerImpl3),
            abi.encodeWithSelector(
                STBL_XLayer_Asset_Issuer.initialize.selector,
                assetId3,
                address(registry),
                iSTBL_T1e_Issuer.AssetType.PT,
                predictedSixDecWrapperProxy
            )
        );
        issuer3 = STBL_XLayer_Asset_Issuer(address(issuerProxy3));

        // Step 5 — deploy vault and yield distributor for Asset3.
        //          The registry's setupAsset validates that these addresses are non-zero,
        //          so we must deploy minimal real instances even though they are never
        //          reached (the DoS revert fires in asset_issue before the vault step).
        STBL_XLayer_Asset_Vault vaultImpl3 = new STBL_XLayer_Asset_Vault();     // N+2
        vaultProxy3 = new ERC1967Proxy(                                          // N+3
            address(vaultImpl3),
            abi.encodeWithSelector(
                STBL_XLayer_Asset_Vault.initialize.selector,
                assetId3,
                address(registry),
                predictedSixDecWrapperProxy
            )
        );
        vault3 = STBL_XLayer_Asset_Vault(address(vaultProxy3));

        STBL_XLayer_Asset_YieldDistributor ydImpl3 =
            new STBL_XLayer_Asset_YieldDistributor();                            // N+4
        yieldDistributorProxy3 = new ERC1967Proxy(                              // N+5
            address(ydImpl3),
            abi.encodeWithSelector(
                STBL_XLayer_Asset_YieldDistributor.initialize.selector,
                assetId3,
                address(registry)
            )
        );
        yieldDistributor3 = STBL_XLayer_Asset_YieldDistributor(address(yieldDistributorProxy3));

        // Step 6 — register Asset3 in the registry
        registry.setupAsset(
            assetId3,
            address(testToken3),
            address(issuer3),
            address(yieldDistributor3),
            address(vault3),
            address(testOracle3),
            0,                    // cut
            type(uint256).max,    // limit
            0,                    // depositFee
            0,                    // withdrawFee
            0,                    // yieldFee
            0,                    // insuranceFee
            7 days,               // duration
            1 days,               // yieldDuration
            ""                    // additionalBytes
        );

        // Step 7 — deploy the dedicated 6-dec wrapper (single-asset basket: Asset3 @ 100%)
        //
        //  The existing xLayerNFTVaultProxy is passed as the NFT vault.
        //  It will never be reached — the revert occurs in asset_issue (transferFrom)
        //  before the NFT vault deposit step.
        iSTBL_ESS_Wrapper1.RatioStuct[] memory ratios =
            new iSTBL_ESS_Wrapper1.RatioStuct[](1);
        ratios[0] = iSTBL_ESS_Wrapper1.RatioStuct({
            assetID: assetId3,
            issuer:  address(issuer3),
            vault:   address(vault3),
            token:   address(testToken3),
            ratio:   ASSET3_RATIO          // 100%
        });

        STBL_XLayer_Wrapper wrapperImpl6dec = new STBL_XLayer_Wrapper(); // N+6
        sixDecWrapperProxy = new ERC1967Proxy(                            // N+7
            address(wrapperImpl6dec),
            abi.encodeWithSelector(
                STBL_XLayer_Wrapper.initialize.selector,
                address(registry),
                iSTBL_ESS_Token(address(xLayerToken)),
                iSTBL_ESS_NFT_Vault1(address(xLayerNFTVaultProxy)),
                ratios
            )
        );
        sixDecWrapper = STBL_XLayer_Wrapper(address(sixDecWrapperProxy));

        // Verify the prediction was correct
        require(
            address(sixDecWrapperProxy) == predictedSixDecWrapperProxy,
            "6-dec wrapper address prediction failed"
        );

        // Grant MINTER_ROLE to the 6-dec wrapper on the ESS token
        xLayerToken.grantRole(MINTER_ROLE, address(sixDecWrapper));

        vm.stopPrank();
    }

    // == [ PoC Test ] ==

    /**
     * @notice PoC: iCalculateRatios returns an 18-decimal amount for a 6-decimal token,
     *         causing asset_issue to request a transferFrom of 10^12x the user's entire
     *         balance — ess_deposit reverts unconditionally.
     */
    function test_poc_sixDecimalToken_DoS() public {
        // == [ Setup: Fund user with a realistic 6-dec USDC balance ] ==

        // Mint 10,000 USDC (6 decimals) to user1
        vm.prank(admin);
        testToken3.mintVal(user1, 10_000e6);

        uint256 userBalance = testToken3.balanceOf(user1);
        console.log("=== PoC: ess_deposit DoS for 6-decimal token ===");
        console.log("[*] User USDC balance (native units, 6 dec):", userBalance);

        // User approves the 6-dec wrapper for the maximum possible amount
        vm.prank(user1);
        IERC20(address(testToken3)).approve(address(sixDecWrapper), type(uint256).max);

        // == [ Demonstrate Discrepancy: Log the inflated transfer amount ] ==

        // CalculateRatios returns the amount that asset_issue will try to transferFrom
        uint256[] memory calculated = sixDecWrapper.CalculateRatios(DEPOSIT_USD);
        uint256 requestedAmt = calculated[0];

        console.log("[*] Deposit USD amount (18 dec):", DEPOSIT_USD);
        console.log("[*] deriveAssetValue returned (inflated, ~1000e18):", requestedAmt);
        console.log("[*] Correct 6-dec native amount (~1000e6):", CORRECT_NATIVE_AMT);
        console.log("[*] User USDC balance (native units):", userBalance);
        console.log("[*] Inflation factor (requestedAmt / correctAmt):", requestedAmt / CORRECT_NATIVE_AMT);

        // Assert: the calculated amount is exactly 10^12 times what it should be
        // (no fees, no rounding offset beyond +1 from the fee adjustment)
        // Expected: (1000e18 * 1e9 / 1e9 + 1) * 1e18 / 1e18 = 1000e18 + 1
        assertGt(
            requestedAmt,
            userBalance,
            "Requested amount must exceed user's entire balance"
        );
        assertGe(
            requestedAmt / CORRECT_NATIVE_AMT,
            1e12 - 1,
            "Inflation must be at least 10^12x"
        );

        console.log("[*] Requested amount >> User balance: confirmed");
        console.log("[*] Attempting ess_deposit(1000e18) - expected to revert ...");

        // == [ Execute Exploit: ess_deposit must revert ] ==

        vm.prank(user1);
        vm.expectRevert();
        sixDecWrapper.ess_deposit(DEPOSIT_USD);

        // == [ Verify Impact: Revert confirmed, user funds untouched ] ==

        uint256 userBalanceAfter = testToken3.balanceOf(user1);
        assertEq(
            userBalanceAfter,
            userBalance,
            "User balance must be unchanged after revert"
        );

        console.log("[+] CONFIRMED: ess_deposit reverts for 6-decimal token basket");
        console.log("[+] User USDC balance unchanged:", userBalanceAfter);
        console.log("[+] ESS minting path permanently unavailable for USDC/USDT baskets");
    }
}

```

**Recommended Mitigation:** In `STBL_XLayer_Asset_Issuer::deriveAssetValue`, normalize the 18-decimal oracle result down to native token decimals before returning, dividing by `10 ** (18 - tokenDecimals)` where `tokenDecimals` is fetched from the token registered in the asset definition

**STBL:** Fixed in commits [d0d3319](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/d0d33194bf09df99562b5cdd9b6ce88fb9ea5612) & [02a08ea](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/02a08ea096ce9a5a77622f7d95d48fade7f3b75c).

**Cyfrin:** Verified. `deriveAssetValue` now fetches the token's native decimal and passes the raw 18-decimal oracle result through `DecimalConverter.convertFrom18Decimals` before returning, normalizing the output to the token's actual precision
