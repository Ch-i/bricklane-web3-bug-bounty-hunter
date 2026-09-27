---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0-1-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0
title: '`verify-governance` compares service slots without attesting the deployed
  implementation, so it reports no drift in a state where `ComplianceConfigurationService`
  rule setters remain transfer-agent gated and entirely undelayed'
vuln_class: []
---

# `verify-governance` compares service slots without attesting the deployed implementation, so it reports no drift in a state where `ComplianceConfigurationService` rule setters remain transfer-agent gated and entirely undelayed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md)_

---

**Description:** `verify-governance` establishes the compliance domain by reading the compliance service's own `COMPLIANCE_RULES_TIMELOCK` slot and comparing it to the token's mirrored entry:

```typescript
const ccsTimelock = await complianceConfigurationService.getDSService(DSConstants.services.COMPLIANCE_RULES_TIMELOCK);
check('compliance enforcement matches discovery', same(ccsTimelock, complianceEntry), ...);
```

That proves a storage slot holds an expected address. It does not prove the deployed `ComplianceConfigurationService` implementation contains `onlyComplianceAdmin`, which is the modifier that actually consults the slot. Enforcement lives in code; the check only inspects data.

The gap is reachable because `ServiceConsumer::getDSService, setDSService` are inherited rather than introduced by this change. `setup-governance` writes the enforcement slot with `ComplianceConfigurationService::setDSService`, and that call succeeds against any implementation, including one predating the modifier. The slot is written, nothing reads it, and verification reports the domain correctly wired.

The two governance domains fail differently, and neither behaviour is deliberate. Role management is protected by accident: `TrustService::setRolesGovernor` is a new function, so calling it against an implementation that lacks it reverts, and the wiring stops. Compliance is unprotected for the mirror-image reason: its wiring call is inherited, so it always succeeds. Nothing in either task distinguishes an installed implementation from an absent one.

A related property makes the state easy to reach. `setup-governance` performs five separate transactions, each awaited, with no rollback. When the roles wiring reverts, the token's three discovery entries and the compliance enforcement slot are already committed, and a later run or verification reads those committed values. The proof below shows exactly that: the compliance slot written before the revert survives into the successful re-run.

**Spec-Intent Gap:**

`timelocks.md` FR-2 states:

> While a compliance rules timelock is registered on the configuration service, only that address or master authority may call any of the 24 rule setters or `setAll`.

In the proof below a compliance rules timelock is registered on the configuration service, and a transfer agent calls a rule setter successfully.

**Impact:** A passing verification carries no information about the compliance domain. The checklist produces an identical result whether the enforcing implementation is installed or not, so it cannot be relied on for the judgement it exists to support.

Verification is the only gate before handover, which the runbook describes as irreversible for the signer. An operator who reads a clean checklist proceeds to hand over master authority while every compliance rule setter is still callable instantly by a transfer-agent holder.

The remediation cost also changes at that point. Before handover, upgrading the compliance service is a single transaction. After it, the upgrade is an operation queued on the master timelock, so correcting a gap that verification failed to report costs a full master delay.

**Proof of Concept:** Add the following test to `test/securitize-io-pocs/test/PartialUpgradeVerificationGap.t.sol` and run with `ETH_RPC_URL=<ethereum mainnet rpc> forge test --match-contract PartialUpgradeVerificationGapTest -vv`. It forks Ethereum mainnet against a live deployment, deploys the reviewed `TrustService` and upgrades the live proxy to it, so the audited code executes rather than a mock:

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.22;

import {Test, console} from "forge-std/Test.sol";
import {TrustService} from "contracts/trust/TrustService.sol";

interface IServiceRegistry {
    function getDSService(uint256 serviceId) external view returns (address);
    function setDSService(uint256 serviceId, address newAddress) external returns (bool);
}

interface ITrustServiceLive {
    function getRole(address who) external view returns (uint8);
    function setRole(address who, uint8 role) external returns (bool);
    function getRolesGovernor() external view returns (address);
    function setRolesGovernor(address newGovernor) external returns (bool);
}

interface ICCS {
    function setCountryCompliance(string calldata country, uint256 value) external;
    function getCountryCompliance(string calldata country) external view returns (uint256);
}

interface IUUPS {
    function upgradeToAndCall(address newImplementation, bytes calldata data) external payable;
}

contract PartialUpgradeVerificationGapTest is Test {
    uint256 constant FORK_BLOCK = 25_845_400;

    // ACRED deployment, Ethereum mainnet
    address constant TOKEN = 0x17418038ecF73BA4026c4f428547BF099706F27B;
    address constant TRUST = 0xc397436742eAF7C325DDBFc4dc63D95822b27101;
    address constant CCS = 0x49465989B80ea0aE4f4129A0f803a4f38B09EA6c;
    address constant MASTER_EOA = 0x59c1eAcEc450c57Dcb9b8725d0F96635C2b676Ee;

    // holds ROLE_TRANSFER_AGENT on this token
    address constant TRANSFER_AGENT = 0x7b021A22fe5a6CaEFD81623fF8fbE7e97B0e61eE;

    uint256 constant MASTER_TIMELOCK = 8198;
    uint256 constant COMPLIANCE_RULES_TIMELOCK = 8199;
    uint256 constant ROLES_TIMELOCK = 8200;

    uint8 constant ROLE_EXCHANGE = 4;

    address masterTl = makeAddr("masterTimelock");
    address complianceTl = makeAddr("complianceTimelock");
    address rolesTl = makeAddr("rolesTimelock");

    function setUp() public {
        vm.createSelectFork(vm.envString("ETH_RPC_URL"), FORK_BLOCK);
    }

    function test_VerificationPassesWhileComplianceEnforcementIsAbsent() public {
        // ---------------------------------------------------------------
        // Step 1: an operator follows the runbook against live proxies and
        //         runs the wiring in the task's own order: the three token
        //         discovery mirrors, then compliance enforcement, then roles
        //         enforcement. The deployment sequence has no upgrade step,
        //         so nothing has been upgraded yet. Everything ahead of the
        //         roles domain lands, then the run dies and the failure names
        //         only TrustService
        // ---------------------------------------------------------------
        vm.startPrank(MASTER_EOA);
        IServiceRegistry(TOKEN).setDSService(MASTER_TIMELOCK, masterTl);
        IServiceRegistry(TOKEN).setDSService(COMPLIANCE_RULES_TIMELOCK, complianceTl);
        IServiceRegistry(TOKEN).setDSService(ROLES_TIMELOCK, rolesTl);

        // the compliance domain gives no signal: its slot is writable on the
        // legacy implementation because getDSService and setDSService are
        // inherited rather than introduced by this change
        IServiceRegistry(CCS).setDSService(COMPLIANCE_RULES_TIMELOCK, complianceTl);
        vm.stopPrank();

        vm.prank(MASTER_EOA);
        (bool ok,) = TRUST.call(abi.encodeCall(ITrustServiceLive.setRolesGovernor, (rolesTl)));
        assertFalse(ok, "step 1: expected setRolesGovernor to fail on the legacy implementation");

        // ---------------------------------------------------------------
        // Step 2: the operator upgrades the contract the error named, and
        //         only that contract, then re-runs
        // ---------------------------------------------------------------
        TrustService newTrustImpl = new TrustService();
        vm.prank(MASTER_EOA);
        IUUPS(TRUST).upgradeToAndCall(address(newTrustImpl), "");

        // ---------------------------------------------------------------
        // Step 3: the wiring now completes end to end
        // ---------------------------------------------------------------
        vm.startPrank(MASTER_EOA);
        IServiceRegistry(TOKEN).setDSService(MASTER_TIMELOCK, masterTl);
        IServiceRegistry(TOKEN).setDSService(COMPLIANCE_RULES_TIMELOCK, complianceTl);
        IServiceRegistry(TOKEN).setDSService(ROLES_TIMELOCK, rolesTl);
        IServiceRegistry(CCS).setDSService(COMPLIANCE_RULES_TIMELOCK, complianceTl);
        ITrustServiceLive(TRUST).setRolesGovernor(rolesTl);
        vm.stopPrank();

        // ---------------------------------------------------------------
        // Step 4: every assertion the verification checklist makes about
        //         the two domains now passes, so it reports no drift
        // ---------------------------------------------------------------
        address ccsTimelock = IServiceRegistry(CCS).getDSService(COMPLIANCE_RULES_TIMELOCK);
        address rolesGovernor = ITrustServiceLive(TRUST).getRolesGovernor();
        address complianceEntry = IServiceRegistry(TOKEN).getDSService(COMPLIANCE_RULES_TIMELOCK);
        address rolesEntry = IServiceRegistry(TOKEN).getDSService(ROLES_TIMELOCK);

        assertEq(ccsTimelock, complianceEntry, "compliance enforcement matches discovery");
        assertEq(rolesGovernor, rolesEntry, "roles enforcement matches discovery");
        assertEq(ccsTimelock, complianceTl, "compliance timelock is the expected address");
        assertEq(rolesGovernor, rolesTl, "roles timelock is the expected address");

        // ---------------------------------------------------------------
        // Step 5: the roles domain really is enforced. A transfer agent
        //         that could previously manage roles is now rejected
        // ---------------------------------------------------------------
        vm.prank(TRANSFER_AGENT);
        vm.expectRevert("Not enough permissions");
        ITrustServiceLive(TRUST).setRole(makeAddr("victim"), ROLE_EXCHANGE);

        // ---------------------------------------------------------------
        // Step 6: the compliance domain is not enforced at all. The same
        //         transfer agent still rewrites a compliance rule directly,
        //         with no queued operation and no delay
        // ---------------------------------------------------------------
        uint256 before = ICCS(CCS).getCountryCompliance("KP");

        vm.prank(TRANSFER_AGENT);
        ICCS(CCS).setCountryCompliance("KP", before + 7);

        assertEq(ICCS(CCS).getCountryCompliance("KP"), before + 7, "step 6: rule did not change");

        console.log("verification reports no drift for both domains");
        console.log("  compliance slot on CCS   :", ccsTimelock);
        console.log("  compliance slot on token :", complianceEntry);
        console.log("  roles governor           :", rolesGovernor);
        console.log("roles domain enforced      : yes, transfer agent reverted");
        console.log("compliance domain enforced : no, transfer agent wrote the rule");
        console.log("  KP compliance before     :", before);
        console.log("  KP compliance after      :", ICCS(CCS).getCountryCompliance("KP"));
    }
}
```

Output:

```
Ran 1 test for test/PartialUpgradeVerificationGap.t.sol:PartialUpgradeVerificationGapTest
[PASS] test_VerificationPassesWhileComplianceEnforcementIsAbsent() (gas: 1370201)
Logs:
  verification reports no drift for both domains
    compliance slot on CCS   : 0xb9191278B80bFC3dd52840a467A06ABD589754eE
    compliance slot on token : 0xb9191278B80bFC3dd52840a467A06ABD589754eE
    roles governor           : 0xF2Bb3e5107d47315209Ae05df69c656f6C53Fc04
  roles domain enforced      : yes, transfer agent reverted
  compliance domain enforced : no, transfer agent wrote the rule
    KP compliance before     : 4
    KP compliance after      : 11
```

One wiring run, one clean verification, and two domains: the transfer agent is rejected by role management and accepted by compliance, rewriting a live country rule from 4 to 11.

**Recommended Mitigation:** Make verification attest to installed behaviour rather than to mutable storage.

1. Introduce a capability or version getter on `ComplianceConfigurationService` alongside `onlyComplianceAdmin`, and have `verify-governance` require it. A missing function reverts, which gives the compliance domain the same accidental protection the roles domain already has, by design rather than by luck
2. Resolve the ERC1967 implementation of each governed proxy and compare it against an approved deployment manifest, so verification reports which code is installed and not only which addresses are stored
3. Have `setup-governance` perform that capability check before writing any enforcement slot, so wiring refuses to proceed against an implementation that cannot honour it
4. Add a fork test over live proxy state asserting the property the checklist claims: a direct transfer-agent call to a rule setter reverts, and the equivalent call executed through the compliance timelock succeeds
5. Write the enforcement slots before the discovery mirrors, and reverse that order when tearing down. The two drift directions are not symmetric: mirrors set with enforcement unset restores instant transfer-agent authority over every rule setter while advertising the domain as timelocked, whereas enforcement set with mirrors unset fails closed. The order the task uses today passes through the damaging state on any interrupted run

**Securitize:** Acknowledged; these Hardhat tasks aren't our production deployment path, and for existing tokens we're treating a per-token review (including confirming which implementation is installed) as a prerequisite before any governance wiring, rather than something the verification task is expected to catch.
