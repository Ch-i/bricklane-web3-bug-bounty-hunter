---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-02-cyfrin-atum-solana-v2-v2-0-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-04-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-02-cyfrin-atum-solana-v2-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-02-cyfrin-atum-solana-v2-v2-0
title: Signatures Lack Cluster and Program Binding, Enabling Cross-Cluster and Cross-Program
  Replay
vuln_class: []
---

# Signatures Lack Cluster and Program Binding, Enabling Cross-Cluster and Cross-Program Replay

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-02-cyfrin-atum-solana-v2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-02-cyfrin-atum-solana-v2-v2.0.md)_

---

**Description:** `compute_deposit_hash` builds the signed message without cluster or program context:

```rust
    // 4. Signature Verification
    let message = compute_deposit_hash(
        payment_id,
        delegate.authority,
        delegate.allowed_mint,
        amount,
        reserver,
        releaser,
        nonce,
        issued_at,
        deadline,
    );
```

The deposit (and derived reserve/release/refund) signatures do not include cluster-specific data or the program ID. This allows:
- Cross-cluster replay: A signature created for Devnet/Testnet to be replayed on Mainnet.

1. User signs a deposit on Devnet for testing.
2. Attacker captures the Ed25519 instruction and signature.
3. Attacker submits the same instruction on Mainnet.
4. Mainnet replay bucket has not seen this nonce, so the replay check passes.
5. If delegate, ATA, and other accounts exist on Mainnet, the deposit succeeds and real funds are moved.

- Cross-program replay: A signature to be replayed on a forked program instance with a different program ID. If the user happens to interact with both programs, the signature could be replyed.


**Impact:** Cross-cluster: Users testing on Devnet/Testnet can have their signatures replayed on Mainnet, leading to unintended deposits and fund movement.
Cross-program: Signatures can be replayed on fork instances

**Recommended Mitigation:**
1. Include `program_id` in the signed message
2. Add a `cluster_id` (or similar) to the signed message.

**Atum:** Fixed in [b4c128e](https://github.com/Atum-Labs/solana-escrow/commit/b4c128e78d8b91112a242b652cfb8b8f4ee0e736).

**Cyfrin:** Verified.
