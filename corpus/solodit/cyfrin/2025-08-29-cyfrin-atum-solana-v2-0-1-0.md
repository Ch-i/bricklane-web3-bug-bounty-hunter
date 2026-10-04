---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-29-cyfrin-atum-solana-v2-0-1-0
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
title: An `authority` cannot use the same `delegate_signer` across multiple mints
  due to `escrow_delegate` PDA seed design
vuln_class: []
---

# An `authority` cannot use the same `delegate_signer` across multiple mints due to `escrow_delegate` PDA seed design

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-29-cyfrin-atum-solana-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-atum-solana-v2.0.md)_

---

**Description:** The `CreateDelegate` instruction initializes an `EscrowDelegate` account with PDA seeds `[b"escrow_delegate", authority, delegate_signer]` while also creating an ATA for a specific `mint`. Because `mint` is not part of the `EscrowDelegate` PDA seeds, there can be only one `EscrowDelegate` instance per `(authority, delegate_signer)` pair regardless of the mint. The `EscrowDelegate` state stores `allowed_mint`, so that single instance becomes implicitly bound to one mint. Attempting to create a second `EscrowDelegate` for a different mint but with the same `delegate_signer` derives the same PDA and `init` fails with “account already in use”.

**Impact:** Prevents an authority from using a single trusted `delegate_signer` to manage deposits for multiple mints.

**Proof of Concept:**
- The following PoC can be run inside `02_delegate_lifecycle.ts`:
```typescript
  it.only("PoC: An `authority` cannot use the same `delegate_signer` across multiple mints due to `escrow_delegate` PDA seed design", async () => {
    // Prepare funded authority and delegate signer
    const [delegateAuthority, delegateSigner] = await Promise.all([
      generateFundedKeypair(),
      generateFundedKeypair(),
    ]);

    console.log("[PoC] Starting test");
    console.log("[PoC] delegateAuthority:", delegateAuthority.publicKey.toBase58());
    console.log("[PoC] delegateSigner:", delegateSigner.publicKey.toBase58());
    console.log("[PoC] first mint:", mint.toBase58());

    // Create first delegate lane for the first mint
    await createDelegate(
      delegateAuthority,
      delegateSigner,
      mint,
      DELEGATE_CAPACITY,
      MAX_TRANSFER_SIZE,
      1
    );
    console.log("[PoC] Created first delegate lane for mint:", mint.toBase58());

    // Spin up a second mint and try to reuse the same (authority, delegate_signer)
    const secondMintSetup = await setupMintAndFund();
    const secondMint = secondMintSetup.mint;
    console.log("[PoC] second mint:", secondMint.toBase58());
    console.log("[PoC] Attempting to create second delegate lane with SAME (authority, delegate_signer) but DIFFERENT mint...");

    try {
      // Expected to fail because PDA seeds do not include the mint,
      // so the same (authority, delegate_signer) maps to the same PDA.
      await createDelegate(
        delegateAuthority,
        delegateSigner,
        secondMint,
        DELEGATE_CAPACITY,
        MAX_TRANSFER_SIZE,
        1
      );

      // If we ever reach here, the test would still fail due to the expect below not running.
      // Log explicitly to make the unexpected path obvious in CI logs.
      console.log("[PoC][Unexpected] Second delegate lane creation succeeded, but it should have failed with PDA 'already in use'.");
    } catch (err) {
      // Anchor should throw an account init collision error that includes "already in use"
      console.log("[PoC] Caught expected init collision error:", err?.toString?.() ?? err);
      expect(err.toString()).to.include("already in use");
      console.log("[PoC] Assertion passed: error contains 'already in use'.");
    }
  });
```
- Output:
```bash
  2. Delegate Lifecycle
[PoC] Starting test
[PoC] delegateAuthority: DXjANuHbqrVPmEJ4G3pLBwFa1MPfmmL9SYtwaTsVqrhY
[PoC] delegateSigner: DXgRWHvxb3Z1FPSiTev5Xd6M6hFRxSmgf35phU3zkQLW
[PoC] first mint: Ediu4xZic4sKEntzFXjsGZSsLGArAYmqACfZc8v6Wazw
[PoC] Created first delegate lane for mint: Ediu4xZic4sKEntzFXjsGZSsLGArAYmqACfZc8v6Wazw
[PoC] second mint: FGHXRTctJhssRFooHyVhMJntiY1LKuF2ePtpQwPAe5qe
[PoC] Attempting to create second delegate lane with SAME (authority, delegate_signer) but DIFFERENT mint...
[PoC] Caught expected init collision error: Error: Simulation failed.
Message: Transaction simulation failed: Error processing Instruction 0: custom program error: 0x0.
Logs:
[
  "Program HuBE5XWDSKpxeQUTRp4BwVCV1c77FL5EQX5Q4xFogQbD invoke [1]",
  "Program log: Instruction: CreateDelegate",
  "Program 11111111111111111111111111111111 invoke [2]",
  "Allocate: account Address { address: m2YRvHLekxqgcJ5ty2sZuTEnVTb125yjv6TEdoAQZjX, base: None } already in use",
  "Program 11111111111111111111111111111111 failed: custom program error: 0x0",
  "Program HuBE5XWDSKpxeQUTRp4BwVCV1c77FL5EQX5Q4xFogQbD consumed 7025 of 200000 compute units",
  "Program HuBE5XWDSKpxeQUTRp4BwVCV1c77FL5EQX5Q4xFogQbD failed: custom program error: 0x0"
].
Catch the `SendTransactionError` and call `getLogs()` on it for full details.
[PoC] Assertion passed: error contains 'already in use'.
    ✔ PoC: An `authority` cannot use the same `delegate_signer` across multiple mints due to `escrow_delegate` PDA seed design (3264ms)
```

**Recommended Mitigation:** Include `mint` in the PDA seeds:
  - `EscrowDelegate` seeds: `[b"escrow_delegate", authority.key().as_ref(), delegate_signer.as_ref(), mint.key()]`

**Atum:**
Fixed in [f517a40](https://github.com/Atum-Labs/solana-escrow/commit/f517a40becedbd7684504b4ef3d6902ea3ac6668).

**Cyfrin:** Verified.
