---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-0-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-08-05T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-05-cyfrin-securitize-evm-async-vault-v2-0
title: Nominal redemption accounting can make rebasing DS Token generations unfulfillable
vuln_class: []
---

# Nominal redemption accounting can make rebasing DS Token generations unfulfillable

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** `AsyncFundVault::requestRedeem` records requests in nominal DS Token units:

```solidity
$.pendingRedeemShares[genId][controller] += shares;
$.redeemGenerations[genId].totalPendingShares += shares;

IERC20(address($.dsToken)).safeTransferFrom(
    owner,
    address(this),
    shares
);
```

The DS Token internally converts each nominal transfer into rebasing shares. Later, `fulfillRedemptions` aggregates the stored nominal requests and performs a single nominal burn:

```solidity
uint256 burnAmount =
    (totalShares * fulfillmentRate) / WAD;

$.dsToken.burn(
    address(this),
    burnAmount,
    "AsyncFundVault: redemption"
);
```

Because the vault never records the internal shares actually received, the aggregate burn may require more internal shares than the vault escrowed. This can occur through two trigger paths:

1. **Multiplier change:** If the rebasing multiplier changes between request and fulfillment, converting the stored nominal amount during `burn` produces a different internal-share amount than the original transfers.

2. **Independent rounding:** Even with a constant multiplier, individually converting each request and later converting their nominal aggregate can produce different results. For example, with a multiplier of `10`, two requests of `19` tokens each escrow `floor(19 / 10) + floor(19 / 10) = 1 + 1 = 2 internal shares` but burning their aggregate requires: `floor((19 + 19) / 10) = floor(38 / 10) = 3 internal shares`. The vault therefore escrows 2 internal shares but attempts to burn 3.

In either case, the vault’s nominal generation accounting does not reconcile with its actual internal-share balance.

**Impact:** `fulfillRedemptions` can revert for the entire generation because the vault lacks enough internal shares for the aggregate burn. Once the generation is closed, users cannot cancel, and because fulfillment cannot succeed, they cannot claim through the normal flow. The generation remains blocked until an external action restores sufficient balance, such as a favorable rebase, administrative recovery, or contract upgrade.

**Proof of Concept:**
1. **Multiplier change case:**
Add the following Foundry test file and run:

```bash
forge test --match-test test_PoC_RebasingEscrowUnderflowBlocksFulfillment -vvv
```

```solidity
pragma solidity ^0.8.22;

import {Test} from "forge-std/Test.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";

import {AsyncFundVault} from "../contracts/AsyncFundVault.sol";
import {AsyncFundVaultStorage} from "../contracts/base/AsyncFundVaultStorage.sol";
import {IAsyncFundVaultErrors} from "../contracts/interfaces/IAsyncFundVaultErrors.sol";

contract ConfigurableERC20 {
    string public name;
    string public symbol;
    uint8 private immutable tokenDecimals;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    constructor(string memory name_, string memory symbol_, uint8 decimals_) {
        name = name_;
        symbol = symbol_;
        tokenDecimals = decimals_;
    }

    function decimals() external view returns (uint8) {
        return tokenDecimals;
    }

    function approve(address spender, uint256 value) external returns (bool) {
        allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    function transfer(address to, uint256 value) external returns (bool) {
        _transfer(msg.sender, to, value);
        return true;
    }

    function transferFrom(address from, address to, uint256 value) external returns (bool) {
        uint256 approved = allowance[from][msg.sender];
        if (approved != type(uint256).max) {
            allowance[from][msg.sender] = approved - value;
            emit Approval(from, msg.sender, allowance[from][msg.sender]);
        }

        _transfer(from, to, value);
        return true;
    }

    function mint(address to, uint256 value) public {
        totalSupply += value;
        balanceOf[to] += value;
        emit Transfer(address(0), to, value);
    }

    function _transfer(address from, address to, uint256 value) internal {
        require(to != address(0), "TRANSFER_TO_ZERO");
        balanceOf[from] -= value;
        balanceOf[to] += value;
        emit Transfer(from, to, value);
    }
}

contract RebaseLikeDSToken is ConfigurableERC20 {
    constructor(uint8 decimals_) ConfigurableERC20("Rebase DS", "rDS", decimals_) {}

    function issueTokens(address to, uint256 value) external returns (bool) {
        mint(to, value);
        return true;
    }

    function burn(address who, uint256 value, string calldata) external {
        require(balanceOf[who] >= value, "BURN_EXCEEDS_BALANCE");
        balanceOf[who] -= value;
        totalSupply -= value;
        emit Transfer(who, address(0), value);
    }

    function preTransferCheck(address, address, uint256) external pure returns (uint256, string memory) {
        return (0, "");
    }

    function setRebasedBalance(address account, uint256 newBalance) external {
        uint256 oldBalance = balanceOf[account];
        if (newBalance > oldBalance) {
            totalSupply += newBalance - oldBalance;
        } else {
            totalSupply -= oldBalance - newBalance;
        }
        balanceOf[account] = newBalance;
    }
}

contract AssetDecimalNavProvider {
    uint256 public rate;

    constructor(uint256 rate_) {
        rate = rate_;
    }

    function setRate(uint256 rate_) external {
        rate = rate_;
    }
}

contract AsyncFundVaultPoC_Test is Test {
    address private admin = makeAddr("admin");
    address private settler = makeAddr("settler");
    address private manager = makeAddr("manager");
    address private alice = makeAddr("alice");
    address private bob = makeAddr("bob");

    function test_PoC_RebasingEscrowUnderflowBlocksFulfillment() public {
        (AsyncFundVault vault, RebaseLikeDSToken dsToken, ConfigurableERC20 liquidityToken) =
            _deployVault(6, 6, 100e6);

        uint256 aliceRedemptionShares = 2e6;
        uint256 bobRedemptionShares = 1e6;
        uint256 totalRedemptionShares = aliceRedemptionShares + bobRedemptionShares;
        _injectLiquidity(vault, liquidityToken, 300e6);

        dsToken.mint(alice, aliceRedemptionShares);
        vm.startPrank(alice);
        dsToken.approve(address(vault), aliceRedemptionShares);
        vault.requestRedeem(aliceRedemptionShares, alice, alice);
        vm.stopPrank();

        dsToken.mint(bob, bobRedemptionShares);
        vm.startPrank(bob);
        dsToken.approve(address(vault), bobRedemptionShares);
        vault.requestRedeem(bobRedemptionShares, bob, bob);
        vm.stopPrank();

        assertEq(vault.pendingRedeemRequest(0, alice), aliceRedemptionShares);
        assertEq(vault.pendingRedeemRequest(0, bob), bobRedemptionShares);
        assertEq(dsToken.balanceOf(address(vault)), totalRedemptionShares);

        vm.prank(settler);
        vault.closeRedemptionGeneration(0);

        dsToken.setRebasedBalance(address(vault), totalRedemptionShares / 2);

        assertEq(vault.pendingRedeemRequest(0, alice), aliceRedemptionShares);
        assertEq(vault.pendingRedeemRequest(0, bob), bobRedemptionShares);
        assertEq(dsToken.balanceOf(address(vault)), totalRedemptionShares / 2);

        vm.prank(settler);
        vm.expectRevert(bytes("BURN_EXCEEDS_BALANCE"));
        vault.fulfillRedemptions(0, 100e18);

        AsyncFundVaultStorage.RedemptionGenerationData memory generation = vault.getRedemptionGeneration(0);
        assertEq(uint8(generation.status), uint8(AsyncFundVaultStorage.GenerationStatus.Closed));
        assertEq(vault.claimableRedeemRequest(0, alice), 0);
        assertEq(vault.claimableRedeemRequest(0, bob), 0);
        assertEq(vault.totalClaimableRedemption(alice), 0);
        assertEq(vault.totalClaimableRedemption(bob), 0);

        vm.prank(alice);
        vm.expectRevert(
            abi.encodeWithSelector(IAsyncFundVaultErrors.CancellationNotAllowed.selector, uint256(0))
        );
        vault.cancelRedeemRequest(0, alice);

        vm.prank(bob);
        vm.expectRevert(
            abi.encodeWithSelector(IAsyncFundVaultErrors.CancellationNotAllowed.selector, uint256(0))
        );
        vault.cancelRedeemRequest(0, bob);

        vm.prank(alice);
        vm.expectRevert(
            abi.encodeWithSelector(IAsyncFundVaultErrors.NoClaimableRedemption.selector, alice)
        );
        vault.redeem(aliceRedemptionShares, alice, alice);

        vm.prank(bob);
        vm.expectRevert(
            abi.encodeWithSelector(IAsyncFundVaultErrors.NoClaimableRedemption.selector, bob)
        );
        vault.redeem(bobRedemptionShares, bob, bob);
    }

    function _deployVault(uint8 dsDecimals, uint8 liquidityDecimals, uint256 navRate)
        private
        returns (AsyncFundVault vault, RebaseLikeDSToken dsToken, ConfigurableERC20 liquidityToken)
    {
        dsToken = new RebaseLikeDSToken(dsDecimals);
        liquidityToken = new ConfigurableERC20("Liquidity", "LIQ", liquidityDecimals);
        AssetDecimalNavProvider navProvider = new AssetDecimalNavProvider(navRate);

        vm.startPrank(admin);
        AsyncFundVault impl = new AsyncFundVault();
        bytes memory initData = abi.encodeCall(
            AsyncFundVault.initialize,
            (address(dsToken), address(liquidityToken), address(navProvider))
        );
        vault = AsyncFundVault(address(new ERC1967Proxy(address(impl), initData)));
        vault.grantRole(vault.SETTLER_ROLE(), settler);
        vault.grantRole(vault.MANAGER_ROLE(), manager);
        vm.stopPrank();

        vm.startPrank(settler);
        vault.openDepositGeneration();
        vault.openRedemptionGeneration();
        vm.stopPrank();
    }

    function _injectLiquidity(AsyncFundVault vault, ConfigurableERC20 liquidityToken, uint256 amount) private {
        liquidityToken.mint(manager, amount);
        vm.startPrank(manager);
        liquidityToken.approve(address(vault), amount);
        vault.injectLiquidity(amount);
        vm.stopPrank();
    }
}
```
2. **Independent rounding case:**
Add the following Foundry test file and run:

```bash
forge test --match-test test_PoC_AggregateBurnExceedsRoundedEscrowShares -vvv
```

```solidity
pragma solidity ^0.8.22;

import {Test} from "forge-std/Test.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";

import {AsyncFundVault} from "../contracts/AsyncFundVault.sol";
import {AsyncFundVaultStorage} from "../contracts/base/AsyncFundVaultStorage.sol";
import {IAsyncFundVaultErrors} from "../contracts/interfaces/IAsyncFundVaultErrors.sol";

contract ConfigurableERC20 {
    string public name;
    string public symbol;
    uint8 private immutable tokenDecimals;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    constructor(string memory name_, string memory symbol_, uint8 decimals_) {
        name = name_;
        symbol = symbol_;
        tokenDecimals = decimals_;
    }

    function decimals() external view returns (uint8) {
        return tokenDecimals;
    }

    function approve(address spender, uint256 value) external returns (bool) {
        allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    function transfer(address to, uint256 value) external returns (bool) {
        _transfer(msg.sender, to, value);
        return true;
    }

    function transferFrom(address from, address to, uint256 value) external returns (bool) {
        uint256 approved = allowance[from][msg.sender];
        if (approved != type(uint256).max) {
            allowance[from][msg.sender] = approved - value;
            emit Approval(from, msg.sender, allowance[from][msg.sender]);
        }

        _transfer(from, to, value);
        return true;
    }

    function mint(address to, uint256 value) public {
        totalSupply += value;
        balanceOf[to] += value;
        emit Transfer(address(0), to, value);
    }

    function _transfer(address from, address to, uint256 value) internal {
        require(to != address(0), "TRANSFER_TO_ZERO");
        balanceOf[from] -= value;
        balanceOf[to] += value;
        emit Transfer(from, to, value);
    }
}

contract RoundingRebaseDSToken {
    uint256 private constant WAD = 1e18;

    string public name = "Rounding DS";
    string public symbol = "rDS";
    uint8 private immutable tokenDecimals;
    uint256 public immutable multiplier;
    uint256 private totalShareSupply;

    mapping(address => uint256) private shareBalance;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    constructor(uint8 decimals_, uint256 multiplier_) {
        tokenDecimals = decimals_;
        multiplier = multiplier_;
    }

    function decimals() external view returns (uint8) {
        return tokenDecimals;
    }

    function totalSupply() external view returns (uint256) {
        return _sharesToTokens(totalShareSupply);
    }

    function balanceOf(address account) external view returns (uint256) {
        return _sharesToTokens(shareBalance[account]);
    }

    function rawSharesOf(address account) external view returns (uint256) {
        return shareBalance[account];
    }

    function approve(address spender, uint256 value) external returns (bool) {
        allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    function transfer(address to, uint256 value) external returns (bool) {
        _transferTokens(msg.sender, to, value);
        return true;
    }

    function transferFrom(address from, address to, uint256 value) external returns (bool) {
        uint256 approved = allowance[from][msg.sender];
        if (approved != type(uint256).max) {
            allowance[from][msg.sender] = approved - value;
            emit Approval(from, msg.sender, allowance[from][msg.sender]);
        }

        _transferTokens(from, to, value);
        return true;
    }

    function mint(address to, uint256 value) public {
        uint256 shares = _tokensToShares(value);
        shareBalance[to] += shares;
        totalShareSupply += shares;
        emit Transfer(address(0), to, value);
    }

    function issueTokens(address to, uint256 value) external returns (bool) {
        mint(to, value);
        return true;
    }

    function burn(address who, uint256 value, string calldata) external {
        uint256 shares = _tokensToShares(value);
        require(shares <= shareBalance[who], "Not enough balance");
        shareBalance[who] -= shares;
        totalShareSupply -= shares;
        emit Transfer(who, address(0), value);
    }

    function preTransferCheck(address, address, uint256) external pure returns (uint256, string memory) {
        return (0, "");
    }

    function _transferTokens(address from, address to, uint256 value) internal {
        require(to != address(0), "TRANSFER_TO_ZERO");
        uint256 shares = _tokensToShares(value);
        require(shares <= shareBalance[from], "Not enough balance");
        shareBalance[from] -= shares;
        shareBalance[to] += shares;
        emit Transfer(from, to, value);
    }

    function _tokensToShares(uint256 tokens) internal view returns (uint256) {
        uint256 shares = (tokens * WAD + multiplier / 2) / multiplier;
        if (tokens > 0) {
            require(shares > 0, "Shares amount too small");
        }
        return shares;
    }

    function _sharesToTokens(uint256 shares) internal view returns (uint256) {
        return (shares * multiplier + WAD / 2) / WAD;
    }
}

contract AssetDecimalNavProvider {
    uint256 public rate;

    constructor(uint256 rate_) {
        rate = rate_;
    }

    function setRate(uint256 rate_) external {
        rate = rate_;
    }
}

contract AsyncFundVaultPoC_Test is Test {
    address private admin = makeAddr("admin");
    address private settler = makeAddr("settler");
    address private manager = makeAddr("manager");
    address private alice = makeAddr("alice");
    address private bob = makeAddr("bob");

    function test_PoC_AggregateBurnExceedsRoundedEscrowShares() public {
        (AsyncFundVault vault, RoundingRebaseDSToken dsToken, ConfigurableERC20 liquidityToken) =
            _deployVaultWithRoundingToken(18, 18, 1e18, 10e18);

        uint256 aliceRedemptionShares = 14;
        uint256 bobRedemptionShares = 14;
        uint256 totalRedemptionShares = aliceRedemptionShares + bobRedemptionShares;
        _injectLiquidity(vault, liquidityToken, totalRedemptionShares);

        dsToken.mint(alice, aliceRedemptionShares);
        vm.startPrank(alice);
        dsToken.approve(address(vault), aliceRedemptionShares);
        vault.requestRedeem(aliceRedemptionShares, alice, alice);
        vm.stopPrank();

        dsToken.mint(bob, bobRedemptionShares);
        vm.startPrank(bob);
        dsToken.approve(address(vault), bobRedemptionShares);
        vault.requestRedeem(bobRedemptionShares, bob, bob);
        vm.stopPrank();

        AsyncFundVaultStorage.RedemptionGenerationData memory generation = vault.getRedemptionGeneration(0);
        assertEq(generation.totalPendingShares, totalRedemptionShares);
        assertEq(dsToken.rawSharesOf(address(vault)), 2);

        vm.prank(settler);
        vault.closeRedemptionGeneration(0);

        vm.prank(settler);
        vm.expectRevert(bytes("Not enough balance"));
        vault.fulfillRedemptions(0, 1e18);

        generation = vault.getRedemptionGeneration(0);
        assertEq(uint8(generation.status), uint8(AsyncFundVaultStorage.GenerationStatus.Closed));
        assertEq(generation.totalPendingShares, totalRedemptionShares);
        assertEq(vault.claimableRedeemRequest(0, alice), 0);
        assertEq(vault.claimableRedeemRequest(0, bob), 0);
        assertEq(dsToken.rawSharesOf(address(vault)), 2);

        vm.prank(alice);
        vm.expectRevert(
            abi.encodeWithSelector(IAsyncFundVaultErrors.CancellationNotAllowed.selector, uint256(0))
        );
        vault.cancelRedeemRequest(0, alice);

        vm.prank(bob);
        vm.expectRevert(
            abi.encodeWithSelector(IAsyncFundVaultErrors.CancellationNotAllowed.selector, uint256(0))
        );
        vault.cancelRedeemRequest(0, bob);

        vm.prank(alice);
        vm.expectRevert(
            abi.encodeWithSelector(IAsyncFundVaultErrors.NoClaimableRedemption.selector, alice)
        );
        vault.redeem(aliceRedemptionShares, alice, alice);

        vm.prank(bob);
        vm.expectRevert(
            abi.encodeWithSelector(IAsyncFundVaultErrors.NoClaimableRedemption.selector, bob)
        );
        vault.redeem(bobRedemptionShares, bob, bob);
    }

    function _deployVaultWithRoundingToken(
        uint8 dsDecimals,
        uint8 liquidityDecimals,
        uint256 navRate,
        uint256 multiplier
    )
        private
        returns (AsyncFundVault vault, RoundingRebaseDSToken dsToken, ConfigurableERC20 liquidityToken)
    {
        dsToken = new RoundingRebaseDSToken(dsDecimals, multiplier);
        liquidityToken = new ConfigurableERC20("Liquidity", "LIQ", liquidityDecimals);
        AssetDecimalNavProvider navProvider = new AssetDecimalNavProvider(navRate);

        vm.startPrank(admin);
        AsyncFundVault impl = new AsyncFundVault();
        bytes memory initData = abi.encodeCall(
            AsyncFundVault.initialize,
            (address(dsToken), address(liquidityToken), address(navProvider))
        );
        vault = AsyncFundVault(address(new ERC1967Proxy(address(impl), initData)));
        vault.grantRole(vault.SETTLER_ROLE(), settler);
        vault.grantRole(vault.MANAGER_ROLE(), manager);
        vm.stopPrank();

        vm.startPrank(settler);
        vault.openDepositGeneration();
        vault.openRedemptionGeneration();
        vm.stopPrank();
    }

    function _injectLiquidity(AsyncFundVault vault, ConfigurableERC20 liquidityToken, uint256 amount) private {
        liquidityToken.mint(manager, amount);
        vm.startPrank(manager);
        liquidityToken.approve(address(vault), amount);
        vault.injectLiquidity(amount);
        vm.stopPrank();
    }
}
```

**Recommended Mitigation:** Make redemption accounting consistently use internal rebasing shares. Record the internal shares actually received for each request and use that basis across fulfillment, cancellation, reassignment, claims, and views.

**Securitize:** Confirmed - we reproduced this against our own repo and the mechanism checks out: `AsyncFundVault` tracks deposits and redemptions purely in nominal DS Token units and never reconciles against the token's own internal share/rebasing accounting. Against a DS Token with an active or changing rebasing multiplier, `fulfillRedemptions` can indeed attempt to burn more internal shares than the vault actually holds, permanently stranding the generation.

For this version, we're addressing it as a documented constraint in commit [5cbf38b](https://github.com/securitize-io/bc-async-ramp-sc/commit/5cbf38b2afcc28ef1b7dec774f3fc2d61f931c5e) rather than a code change: this vault is only supported against a DS Token whose rebasing multiplier is fixed at 1e18 (i.e. no active rebasing). We've added explicit warnings at the contract level, on initialize()'s dsToken param, and on the storage field itself, so this constraint is visible to anyone deploying or reviewing the contract, not just something known informally.

We're not treating this as "won't fix" - if a future fund needs this vault to work with an actively-rebasing DS Token, that will need a new version that tracks internal shares received/burned directly (per the recommended mitigation) rather than nominal amounts, since that's a real architectural change to the redemption accounting, not a patch. For now, every 7540 vault we deploy will be paired with a non-rebasing DS Token, so this is out of reach in practice.

\clearpage
