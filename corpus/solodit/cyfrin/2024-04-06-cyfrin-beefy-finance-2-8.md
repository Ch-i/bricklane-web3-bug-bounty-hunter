---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-8
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Deposit can return zero shares when user deposits a positive amount of tokens
vuln_class: []
---

# Deposit can return zero shares when user deposits a positive amount of tokens

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** Stateless fuzzing found an edge-case where a user could deposit an amount of tokens > 0 but receive zero output shares. The cause appears to be either a rounding down to zero precision loss in the share calculation [L179](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol#L179) due to small amounts or the subtraction of the minimum share amount [L182](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol#L182) from the first depositor, combined with no zero share check after this occurs.

Interestingly `BeefyVaultConcLiq::deposit` does have a check to prevent zero shares [L173](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol#L173) being minted but the share amount is subsequently modified after this check occurs.

**Impact:** Protocol can enter a state where a user deposits a positive amount of tokens but receives zero output shares in return.

**Proof of Concept:** Add this test file `test/forge/ConcLiqTests/ConcLiqWBTCUSDC.t.sol`:
```solidity
pragma solidity 0.8.23;

import {Test, console} from "forge-std/Test.sol";
import {IERC20} from "@openzeppelin-4/contracts/token/ERC20/ERC20.sol";
import {BeefyVaultConcLiq} from "contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol";
import {BeefyVaultConcLiqFactory} from "contracts/protocol/concliq/vault/BeefyVaultConcLiqFactory.sol";
import {StrategyPassiveManagerUniswap} from "contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol";
import {StrategyFactory} from "contracts/protocol/concliq/uniswap/StrategyFactory.sol";
import {StratFeeManagerInitializable} from "contracts/protocol/beefy/StratFeeManagerInitializable.sol";
import {IStrategyConcLiq} from "contracts/interfaces/beefy/IStrategyConcLiq.sol";
import {UniV3Utils} from "contracts/interfaces/exchanges/UniV3Utils.sol";

// Test WBTC/USDC Uniswap Strategy
contract ConLiqWBTCUSDCTest is Test {
    BeefyVaultConcLiq vault;
    BeefyVaultConcLiqFactory vaultFactory;
    StrategyPassiveManagerUniswap strategy;
    StrategyPassiveManagerUniswap implementation;
    StrategyFactory factory;
    address constant pool = 0x9a772018FbD77fcD2d25657e5C547BAfF3Fd7D16;
    address constant token0 = 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599;
    address constant token1 = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address constant native = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address constant strategist = 0xb2e4A61D99cA58fB8aaC58Bb2F8A59d63f552fC0;
    address constant beefyFeeRecipient = 0x65f2145693bE3E75B8cfB2E318A3a74D057e6c7B;
    address constant beefyFeeConfig = 0x3d38BA27974410679afF73abD096D7Ba58870EAd;
    address constant unirouter = 0xE592427A0AEce92De3Edee1F18E0157C05861564;
    address constant keeper = 0x4fED5491693007f0CD49f4614FFC38Ab6A04B619;
    int24 constant width = 500;
    address constant user     = 0x161D61e30284A33Ab1ed227beDcac6014877B3DE;
    address constant attacker = address(0x1337);
    bytes tradePath1;
    bytes tradePath2;
    bytes path0;
    bytes path1;

    function setUp() public {
        BeefyVaultConcLiq vaultImplementation = new BeefyVaultConcLiq();
        vaultFactory = new BeefyVaultConcLiqFactory(address(vaultImplementation));
        vault = vaultFactory.cloneVault();
        implementation = new StrategyPassiveManagerUniswap();
        factory = new StrategyFactory(keeper);

        address[] memory lpToken0ToNative = new address[](2);
        lpToken0ToNative[0] = token0;
        lpToken0ToNative[1] = native;

        address[] memory lpToken1ToNative = new address[](2);
        lpToken1ToNative[0] = token1;
        lpToken1ToNative[1] = native;

        uint24[] memory fees = new uint24[](1);
        fees[0] = 500;

        path0 = routeToPath(lpToken0ToNative, fees);
        path1 = routeToPath(lpToken1ToNative, fees);

        address[] memory tradeRoute1 = new address[](2);
        tradeRoute1[0] = token0;
        tradeRoute1[1] = token1;

        address[] memory tradeRoute2 = new address[](2);
        tradeRoute2[0] = token1;
        tradeRoute2[1] = token0;

        tradePath1 = routeToPath(tradeRoute1, fees);
        tradePath2 = routeToPath(tradeRoute2, fees);

        StratFeeManagerInitializable.CommonAddresses memory commonAddresses = StratFeeManagerInitializable.CommonAddresses(
            address(vault),
            unirouter,
            keeper,
            strategist,
            beefyFeeRecipient,
            beefyFeeConfig
        );

        factory.addStrategy("StrategyPassiveManagerUniswap_v1", address(implementation));

        address _strategy = factory.createStrategy("StrategyPassiveManagerUniswap_v1");
        strategy = StrategyPassiveManagerUniswap(_strategy);
        strategy.initialize(
            pool,
            native,
            width,
            path0,
            path1,
            commonAddresses
        );

        // render calm check ineffective to allow deposit to work; not related to the
        // identified bug, for some reason the first deposit was failing due to the calm
        // check
        strategy.setTwapInterval(1);

        vault.initialize(address(strategy), "Moo Vault", "mooVault");
    }

    // run with:
    // forge test --match-path test/forge/ConcLiqTests/ConcLiqWBTCUSDC.t.sol --fork-url https://rpc.ankr.com/eth --fork-block-number 19410822 -vvv
    function test_DepositResultsInZeroShares(uint32 token0Amount, uint32 token1Amount) public {
        // satisfy minimum share to prevent reverting due to underflow
        vm.assume( (token1Amount + (token0Amount * strategy.price() / 1e36)) == 10**3 );

        uint256 userInitShares = vault.balanceOf(user);

                            // 0           // 1000
        deposit(user, true, token0Amount, token1Amount);

        uint256 userAfterShares = vault.balanceOf(user);

        console.log(userInitShares);  // 0
        console.log(userAfterShares); // 0

        // shares should have increased
        assert(userInitShares < userAfterShares);
    }

    // handlers
    function deposit(address depositor, bool dealTokens, uint256 token0Amount, uint256 token1Amount) public {
        vm.startPrank(depositor);

        if(dealTokens) {
            deal(address(token0), depositor, token0Amount);
            deal(address(token1), depositor, token1Amount);
        }

        IERC20(token0).approve(address(vault), token0Amount);
        IERC20(token1).approve(address(vault), token1Amount);

        uint256 _shares = vault.previewDeposit(token0Amount, token1Amount);

        vault.depositAll(_shares);

        vm.stopPrank();
    }

    // Convert token route to encoded path
    // uint24 type for fees so path is packed tightly
    function routeToPath(
        address[] memory _route,
        uint24[] memory _fee
    ) internal pure returns (bytes memory path) {
        path = abi.encodePacked(_route[0]);
        uint256 feeLength = _fee.length;
        for (uint256 i = 0; i < feeLength; i++) {
            path = abi.encodePacked(path, _fee[i], _route[i+1]);
        }
    }
}
```

Run with: `forge test --match-path test/forge/ConcLiqTests/ConcLiqWBTCUSDC.t.sol --fork-url https://rpc.ankr.com/eth --fork-block-number 19410822 -vvv`

**Recommended Mitigation:** Check for zero shares again before minting shares to the user.

**Beefy:**
Fixed in commit [bee75ac](https://github.com/beefyfinance/experiments/commit/bee75ac2e2ec0d94093ee8f5c3361f98119604bc).

**Cyfrin:** Verified.
