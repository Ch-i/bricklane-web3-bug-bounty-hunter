---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-03-cyfrin-linea-burn-v2-2-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-11-03T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md
tags:
- firm:cyfrin
- report:2025-11-03-cyfrin-linea-burn-v2-2
title: Unnecessary implementation of the `RollupRevenueVault::initialize` given that
  the deployed proxy is already initialized
vuln_class: []
---

# Unnecessary implementation of the `RollupRevenueVault::initialize` given that the deployed proxy is already initialized

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-03-cyfrin-linea-burn-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md)_

---

**Description:** The `RollupRevenueVault` contract will be used to upgrade the implementation of the [proxy](https://lineascan.build/address/0xfd5fb23e06e46347d8724486cdb681507592e237)
The proxy is already initialized; therefore, the `_initialized` flag is already set to 1. This means that no function calling the `initializer` modifier can be executed again, not even after the upgrade.
This means that the only alternative to initializing the values of the new implementation is to call the `reinitializer` modifier, which is invoked by the `RollupRevenueVault::initializeRolesAndStorageVariables` function.
```solidity
    function initialize(
        ...
@>  ) external initializer {
        ...
    }

    function initializeRolesAndStorageVariables(
        ...
@>  ) external reinitializer(2) {
        ...
        );
    }
```

**Proof of Concept:** Run the following PoC to verify the upgrade only works when calling the `initializeRolesAndStorageVariables` function and reverts when calling the `initialize` function.
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.30;

import "forge-std/Test.sol";
import {
    TransparentUpgradeableProxy,
    ITransparentUpgradeableProxy
} from "@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";

import {RollupRevenueVault} from "src/operational/RollupRevenueVault.sol";

import {Vm} from "forge-std/Vm.sol";

contract RollupRevenueVaultUpgradeSimulationTest is Test {
    ITransparentUpgradeableProxy public proxy;
    RollupRevenueVault public newImpl;
    RollupRevenueVault public vaultUpgraded; // Proxy cast to upgraded interface

    bytes32 ADMIN_SLOT = 0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103;
    bytes32 IMPLEMENTATION_SLOT = 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;

    // Existing proxy address on Linea
    address public proxyAddr = 0xFD5FB23e06e46347d8724486cDb681507592e237;

    // Fork URL for Linea mainnet
    string public lineaRpc = "https://linea-mainnet.g.alchemy.com/v2/<ALCHEMY_API_KEY>";

    // Variables for initialization
    address public admin;
    address public invoiceSubmitter;
    address public burner;
    address public invoicePaymentReceiver;
    address public tokenBridge = address(100);
    address public messageService = address(101);
    address public l1LineaTokenBurner = 0x000000000000000000000000000000000000dEaD;
    address public lineaToken = address(102);
    address public dex = address(103);
    uint256 public lastInvoiceDate;

    function setUp() public {
        // Create and select fork of Linea mainnet
        uint256 forkId = vm.createFork(lineaRpc);
        vm.selectFork(forkId);

        // Set the proxy
        proxy = ITransparentUpgradeableProxy(payable(proxyAddr));

        assertGt(address(proxy).balance, 0);

                //@audit-info => Doesn't work because the caller is not the admin :) !
                // admin = proxy.admin();

        // Get the current admin
        admin = getAdminAddress(address(proxy));

        // Set mock/test values for roles and receiver (in production, these would be specific addresses)
        invoiceSubmitter = vm.addr(1); // Placeholder, replace with actual if known
        burner = vm.addr(2); // Placeholder, replace with actual if known
        invoicePaymentReceiver = vm.addr(3); // Placeholder, replace with actual if known
        lastInvoiceDate = block.timestamp; // Use current timestamp for simulation

        // Deploy the new implementation
        newImpl = new RollupRevenueVault();

        // Encode the initialize calldata for upgrade (initialize())
        bytes memory initDataUpgrade_initialize = abi.encodeWithSelector(
            RollupRevenueVault.initialize.selector,
            lastInvoiceDate,
            admin, // Keep the same admin
            invoiceSubmitter,
            burner,
            invoicePaymentReceiver,
            tokenBridge,
            messageService,
            l1LineaTokenBurner,
            lineaToken,
            dex
        );

//@audit => upgrade fails when calling initialize because of the initializer modifier
        vm.prank(admin);
        vm.expectRevert();
        proxy.upgradeToAndCall(address(newImpl), initDataUpgrade_initialize);

        // Encode the reinitialization calldata for upgrade (reinitializer(2))
        bytes memory initDataUpgrade_reinitialize = abi.encodeWithSelector(
            RollupRevenueVault.initializeRolesAndStorageVariables.selector,
            lastInvoiceDate,
            admin, // Keep the same admin
            invoiceSubmitter,
            burner,
            invoicePaymentReceiver,
            tokenBridge,
            messageService,
            l1LineaTokenBurner,
            lineaToken,
            dex
        );

//@audit => upgrade succeeds when calling initializeRolesAndStorageVariables because of the reinitializer modifier
        vm.prank(admin);
        proxy.upgradeToAndCall(address(newImpl), initDataUpgrade_reinitialize);


        // Cast the proxy to the new interface
        vaultUpgraded = RollupRevenueVault(payable(address(proxy)));
    }

    function testUpgradeSimulation() public {
        // Verify the implementation has been updated
        assertEq(getImplementationAddress(address(proxy)), address(newImpl));

        // // Verify initialization values after upgrade
        assertEq(vaultUpgraded.lastInvoiceDate(), lastInvoiceDate);
        assertEq(vaultUpgraded.invoicePaymentReceiver(), invoicePaymentReceiver);
        assertEq(vaultUpgraded.dex(), dex);
        assertEq(address(vaultUpgraded.tokenBridge()), tokenBridge);
        assertEq(address(vaultUpgraded.messageService()), messageService);
        assertEq(vaultUpgraded.l1LineaTokenBurner(), l1LineaTokenBurner);
        assertEq(vaultUpgraded.lineaToken(), lineaToken);

        // Verify invoice arrears starts at 0
        assertEq(vaultUpgraded.invoiceArrears(), 0);

        // Verify constants
        assertEq(vaultUpgraded.ETH_BURNT_PERCENTAGE(), 20);

        // Verify the proxy still holds its balance (should be unchanged)
        assertGt(address(proxy).balance, 0); // From explorer, ~198 ETH
    }

    function getAdminAddress(address proxy) internal view returns (address) {
        address CHEATCODE_ADDRESS = 0x7109709ECfa91a80626fF3989D68f67F5b1DD12D;
        Vm vm = Vm(CHEATCODE_ADDRESS);

        bytes32 adminSlot = vm.load(proxy, ADMIN_SLOT);
        return address(uint160(uint256(adminSlot)));
    }

    function getImplementationAddress(address proxy) internal view returns (address) {
        address CHEATCODE_ADDRESS = 0x7109709ECfa91a80626fF3989D68f67F5b1DD12D;
        Vm vm = Vm(CHEATCODE_ADDRESS);

        bytes32 implementationSlot = vm.load(proxy, IMPLEMENTATION_SLOT);
        return address(uint160(uint256(implementationSlot)));
    }
}
```

**Recommended Mitigation:** Remove the `RollupRevenueVault::initialize`. Only `RollupRevenueVault::initializeRolesAndStorageVariables` is required to reinitialize the values for the upgrade.

**Linea:** Fixed at [PR 1604](https://github.com/Consensys/linea-monorepo/pull/1604)

**Cyfrin:** Verified. The initialize function has been removed.
