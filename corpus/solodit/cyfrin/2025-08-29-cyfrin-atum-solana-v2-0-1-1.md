---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-29-cyfrin-atum-solana-v2-0-1-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-08-29T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-atum-solana-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-29-cyfrin-atum-solana-v2-0
title: 4-horizon wrap leaves stale replay bit and rejects valid deposit as `DuplicateTransaction`
vuln_class: []
---

# 4-horizon wrap leaves stale replay bit and rejects valid deposit as `DuplicateTransaction`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-29-cyfrin-atum-solana-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-atum-solana-v2.0.md)_

---

**Description:** `check_replay` stores a 2-bit epoch tag in the bitmap header and wipes the bitmap only when `epoch_now ^ stored_epoch == 2`. Epoch and parity are derived from `issued_at` as:
- `epoch_now = (issued_at / REPLAY_HORIZON_SECS) & 3`
- `parity = (issued_at / REPLAY_HORIZON_SECS) & 1`
with `REPLAY_HORIZON_SECS = 120`.

Because the epoch is only 2 bits, it wraps every 4 horizons. After an idle gap of exactly 4 horizons, both the parity and the 2-bit epoch equal their earlier values, so `diff == 0` and the bitmap is not wiped. The old slot bit remains set and a legitimate new deposit that reuses the same low-8-bit slot is rejected with `DuplicateTransaction`. This is scoped per authority and per replay bucket (derived from the upper 4 bytes of the nonce).

**Impact:** Legitimate deposits can be rejected until a different slot is used or subsequent activity triggers a wipe.


**Proof of Concept:**
- The following PoC can be run inside `08_replay_protection.ts`:
```typescript
it.only("PoC: 4-horizon wrap leaves stale replay bit and rejects valid deposit as `DuplicateTransaction`", async function () {
  this.timeout(11 * 60 * 1000);

  const H = 120; // REPLAY_HORIZON_SECS
  const nonce = new anchor.BN("0000000E00000025", 16); // bucket 14, slot 37

  // Helpers only for inspection/logging (no behavior change)
  const e2 = (t: number) => (Math.floor(t / H) & 3);
  const p  = (t: number) => (Math.floor(t / H) & 1);
  const ts = (t: number) => new Date(t * 1000).toISOString();

  // Log the nonce layout for reviewers (no behavior change)
  const nonceLe = nonce.toBuffer("le", 8);
  const slot = nonceLe[0];
  const bucketHi = Buffer.from(nonceLe.slice(4));
  console.log("ℹ️  Nonce layout",
    "| bucket_hi(le):", bucketHi.toString("hex"),
    "| slot:", slot,
    "| raw_le:", Buffer.from(nonceLe).toString("hex")
  );

  // -------- A) First deposit: set the bit in current parity --------
  const paymentIdA = createPaymentId();
  const nowA = Math.floor(Date.now() / 1000);
  const issuedAtA = new anchor.BN(nowA - 5);           // inside window
  const deadlineA = new anchor.BN(issuedAtA.toNumber() + 60);

  console.log(
    "[A] issuedAt:", issuedAtA.toNumber(), `(${ts(issuedAtA.toNumber())})`,
    "| epoch2:", e2(issuedAtA.toNumber()),
    "| parity:", p(issuedAtA.toNumber())
  );

  const msgA = await createMessage("deposit", [
    paymentIdA,
    depositor.publicKey.toBuffer(),
    mint.toBuffer(),
    DEPOSIT_AMOUNT.toBuffer("le", 8),
    reserver.publicKey.toBuffer(),
    releaser.publicKey.toBuffer(),
    nonce.toBuffer("le", 8),
    issuedAtA.toBuffer("le", 8),
    deadlineA.toBuffer("le", 8),
  ]);
  const sigA = createEd25519Instruction(delegateSigner, msgA);

  const [replayBucket] = PublicKey.findProgramAddressSync(
    [REPLAY_SEED, depositor.publicKey.toBuffer(), nonce.toBuffer("le", 8).slice(4)],
    escrowProgram.programId
  );
  const [depositA] = PublicKey.findProgramAddressSync(
    [DEPOSIT_SEED, depositor.publicKey.toBuffer(), paymentIdA],
    escrowProgram.programId
  );
  const escrowAtaA = await getAssociatedTokenAddress(mint, depositA, true);

  console.log("PDAs",
    "| replayBucket:", replayBucket.toBase58(),
    "| depositA:", depositA.toBase58(),
    "| escrowAtaA:", escrowAtaA.toBase58()
  );

  await escrowProgram.methods
    .deposit(
      Array.from(paymentIdA),
      DEPOSIT_AMOUNT,
      reserver.publicKey,
      releaser.publicKey,
      nonce,
      issuedAtA,
      deadlineA
    )
    .accountsPartial({
      escrowDelegate: delegate,
      authority: depositor.publicKey,
      replayBucket,
      authorityAta,
      deposit: depositA,
      escrowAta: escrowAtaA,
      mint,
      payer: payer.publicKey,
      tokenProgram: TOKEN_PROGRAM_ID,
      associatedTokenProgram: ASSOCIATED_TOKEN_PROGRAM_ID,
      systemProgram: SystemProgram.programId,
      instructions: anchor.web3.SYSVAR_INSTRUCTIONS_PUBKEY,
    })
    .preInstructions([sigA])
    .signers([payer])
    .rpc();

  console.log(`✅ [A] Deposit set bit slot=${slot} in parity=${p(issuedAtA.toNumber())} (epoch2=${e2(issuedAtA.toNumber())})`);

  // -------- B) Align to the SAME parity+epoch2 after 4 horizons --------
  // Compute based on A's epoch, not "now". This matches your original logic.
  const baseK = Math.floor(issuedAtA.toNumber() / H);
  let targetStart = (baseK + 4) * H; // start of the slice 4 horizons after A

  // Original behavior: no extra guards or loops, just one sleep
  const now1 = Math.floor(Date.now() / 1000);
  const secsUntil = targetStart - now1 + 2;
  console.log(`[sleep] waiting ${secsUntil}s to hit 4-horizon wrap aligned to A`,
              "| targetStart:", targetStart, `(${ts(targetStart)})`,
              "| baseK:", baseK, "→ targetK:", baseK + 4);
  await sleep(secsUntil * 1000);

  // Keep the original issuedAtB logic exactly as-is
  const issuedAtBNum = targetStart + 1;
  const issuedAtB = new anchor.BN(issuedAtBNum);
  const deadlineB = new anchor.BN(issuedAtBNum + 60);

  console.log(
    "[B] issuedAt:", issuedAtBNum, `(${ts(issuedAtBNum)})`,
    "| epoch2:", e2(issuedAtBNum),
    "| parity:", p(issuedAtBNum),
    "(should match [A])"
  );

  const paymentIdB = createPaymentId();
  const msgB = await createMessage("deposit", [
    paymentIdB,
    depositor.publicKey.toBuffer(),
    mint.toBuffer(),
    DEPOSIT_AMOUNT.toBuffer("le", 8),
    reserver.publicKey.toBuffer(),
    releaser.publicKey.toBuffer(),
    nonce.toBuffer("le", 8),
    issuedAtB.toBuffer("le", 8),
    deadlineB.toBuffer("le", 8),
  ]);
  const sigB = createEd25519Instruction(delegateSigner, msgB);
  const [depositB] = PublicKey.findProgramAddressSync(
    [DEPOSIT_SEED, depositor.publicKey.toBuffer(), paymentIdB],
    escrowProgram.programId
  );
  const escrowAtaB = await getAssociatedTokenAddress(mint, depositB, true);

  console.log("PDAs",
    "| depositB:", depositB.toBase58(),
    "| escrowAtaB:", escrowAtaB.toBase58()
  );

  try {
    await escrowProgram.methods
      .deposit(
        Array.from(paymentIdB),
        DEPOSIT_AMOUNT,
        reserver.publicKey,
        releaser.publicKey,
        nonce,
        issuedAtB,
        deadlineB
      )
      .accountsPartial({
        escrowDelegate: delegate,
        authority: depositor.publicKey,
        replayBucket,
        authorityAta,
        deposit: depositB,
        escrowAta: escrowAtaB,
        mint,
        payer: payer.publicKey,
        tokenProgram: TOKEN_PROGRAM_ID,
        associatedTokenProgram: ASSOCIATED_TOKEN_PROGRAM_ID,
        systemProgram: SystemProgram.programId,
        instructions: anchor.web3.SYSVAR_INSTRUCTIONS_PUBKEY,
      })
      .preInstructions([sigB])
      .signers([payer])
      .rpc();

    console.log("❌ [B] deposit unexpectedly succeeded");
    expect.fail("Expected DuplicateTransaction after 4-horizon wrap, but deposit succeeded");
  } catch (err: any) {
    const s = String(err);
    console.log("[B] expected failure caught →", s);
    console.log("📍 Expecting AnchorError DuplicateTransaction from utils/replay.rs @ check_replay()");
    expect(s).to.include("DuplicateTransaction");
  }
});
```
- Output:
```bash
  8. Replay Protection
ℹ️  Nonce layout | bucket_hi(le): 0e000000 | slot: 37 | raw_le: 250000000e000000
[A] issuedAt: 1756379201 (2025-08-28T11:06:41.000Z) | epoch2: 1 | parity: 1
PDAs | replayBucket: 4aAFdtScExWrKzbPkyUZhdWyzB5ZhkTCGJWYVStYPE3H | depositA: A4yt8RAg8PFfBrX3AQiQxZ2medH7RyzL9tTQQN1vCiCy | escrowAtaA: 8nSLVJvYTixrzxvz8Rg1gMDFKxvKE3KhAxx3SvEFBtXr
✅ [A] Deposit set bit slot=37 in parity=1 (epoch2=1)
[sleep] waiting 435s to hit 4-horizon wrap aligned to A | targetStart: 1756379640 (2025-08-28T11:14:00.000Z) | baseK: 14636493 → targetK: 14636497
[B] issuedAt: 1756379641 (2025-08-28T11:14:01.000Z) | epoch2: 1 | parity: 1 (should match [A])
PDAs | depositB: Bvike8cJnmYsreDHqVSBqfiZ8iqmZz8nt2uoKS1ygrvt | escrowAtaB: EaWERuFbQAQ2nqkTVEUethgA9N8HczAyz6mjiBWEVXgz
[B] expected failure caught → AnchorError thrown in programs/escrow/src/utils/replay.rs:76. Error Code: DuplicateTransaction. Error Number: 6025. Error Message: DuplicateTransaction.
📍 Expecting AnchorError DuplicateTransaction from utils/replay.rs @ check_replay()
    ✔ PoC: 4-horizon wrap leaves stale replay bit and rejects valid deposit as `DuplicateTransaction` (435482ms)


  1 passing (7m)
```

**Recommended Mitigation:** There is no trivial fix. Either expand the epoch to 3 bits so wipes trigger after gaps of 2 to 7 horizons, which pushes the corner case to exact 8-horizon wraps, or document the behavior and accept the residual availability risk.

**Atum:**
Fixed in [4c1f8d7](https://github.com/Atum-Labs/solana-escrow/commit/4c1f8d7329817e9d933d52ce23a26e22f658e779) and [e7dc659](https://github.com/Atum-Labs/solana-escrow/commit/e7dc659a42f1543776ac303aa9f2ac086b6b2fa1).

**Cyfrin:** Verified.


\clearpage
