---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-29-cyfrin-atum-solana-v2-0-2-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-08-29T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-atum-solana-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-29-cyfrin-atum-solana-v2-0
title: reserve/release/refund methods are not implementing deadline check for signatures
  allows signature reusing
vuln_class: []
---

# reserve/release/refund methods are not implementing deadline check for signatures allows signature reusing

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-29-cyfrin-atum-solana-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-atum-solana-v2.0.md)_

---

**Description:** We are not implementing nonce replay protection mechanism for functions `reserve/release/refund`. we are not using `check_replay` method which checks for the signature `deadline` and nonce unique usage.

There are currently two problems in the current implementations that can will introduce issues as well as reply attack possibilities

1. No deadline parameter is implemented
When signing a message, it is better to have a deadline parameter, so that the signature do not stay for too long as valid. there is no deadline parameter implemented in the hash construction for any of the three mentioned functions.

[signatures.rs#L39-L59](https://github.com/Atum-Labs/solana-escrow/blob/main/programs/escrow/src/utils/signatures.rs#L39-L59)
```rust
pub fn compute_reserve_hash(
    payment_id: [u8; 32],
    recipient: Pubkey,
    depositor: Pubkey,
) -> [u8; 32] {
    keccak::hashv(&[
        b"reserve",
        &payment_id,
        recipient.as_ref(),
        depositor.as_ref(),
    ])
    .0
}

pub fn compute_release_hash(payment_id: [u8; 32], depositor: Pubkey) -> [u8; 32] {
    keccak::hashv(&[b"release", &payment_id, depositor.as_ref()]).0
}

pub fn compute_refund_hash(payment_id: [u8; 32], depositor: Pubkey) -> [u8; 32] {
    keccak::hashv(&[b"refund", &payment_id, depositor.as_ref()]).0
}

```

2. The signature can be reused again, if same paymentId is reused again
When calling deposit, we are creating `DepositInfo` account. This account is derived from the depositor and the paymentId.

The `DepositInfo` account is closed when releasing or refunding. so if the same depositor called deposit with the same paymentId, it can recreate this account. The problem is that when reusing the paymentId for the same depositor, all previous signed messages can be reused again.

NOTE: this is not the same as that in EVM, as in EVM deadline is used for these three functions, and another point, is that the possibility of having same `depositId` twice is too little to occur as it depend on signature, which includes nonce, so it is changeable.

So the current behaviour will not satisfy the reply protection for reserve/release/refund functions

**Impact:**
- Signatures for reserve/release/refund will be kept alive forever without a deadline
- Possibility of reusing the signatures again, since there `paymentId` can be reused, as well as no deadline check is implemented

**Recommended Mitigation:** The issue can be mitigated by implementing deadline check, this will not guarantee the issue to not occur as it can occur if the `deposit` account is closed either by refunding or releasing. and new one is created with the same paymentId for the same depositor before the deadline ends. But since it should be hard for paymentId to get used twice, and should be handled by the off-chain system, we see deadline check is enough

**Atum:**
Fixed in [eb24d80](https://github.com/Atum-Labs/solana-escrow/commit/eb24d801a7beef9815f3828a216381a6f74136a4).

**Cyfrin:** Verified.
