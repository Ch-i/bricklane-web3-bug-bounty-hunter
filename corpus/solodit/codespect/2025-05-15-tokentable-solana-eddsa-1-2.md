---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-05-15-tokentable-solana-eddsa-1-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-05-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-05-15-TokenTable-Solana-EDDSA.md
tags:
- firm:codespect
- report:2025-05-15-tokentable-solana-eddsa
title: '[I-03] Unused code'
vuln_class: []
---

# [I-03] Unused code

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-05-15-TokenTable-Solana-EDDSA.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-05-15-TokenTable-Solana-EDDSA.md)_

---

**Files:** [utils.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/87b79fe77b74d734fc5274da93300aa39444146c/programs/eddsa-token-distributor-solana/src/instructions/utils.rs#L208)

**Description:**

The `utils.rs` file containing signature verification capabilities of the program contains unused code:

```rust
pub fn merkle_verify(proof: Vec<[u8; 32]>, root: [u8; 32], leaf: [u8; 32]) -> bool {
    let mut computed_hash = leaf;
    for proof_element in proof.into_iter() {
        if computed_hash <= proof_element {
            computed_hash = keccak::hashv(&[&computed_hash, &proof_element]).0;
        } else {
            computed_hash = keccak::hashv(&[&proof_element, &computed_hash]).0;
        }
    }
    computed_hash == root
}
```

Which was likely copied unnecessarily from the Merkle Distributor program.

Another unreachable code section is related to the `verify_secp256k1_ix` which is not used anywhere in the code, there could be two options. As per design the Secp256k1 signatures are not supported by the protocol

**Impact:** Higher SOL fees for program deployment and upgrades

**Recommendation(s):** Remove the unnecessary code.

**Status:** Fixed

**Update from TokenTable:** Unused code removed in [f925d1f5aaf75371cc9fd99c5c34269362abba97](https://github.com/EthSign/tokentable-unlocker-solana/commit/f925d1f5aaf75371cc9fd99c5c34269362abba97) and [54c916fe785c9249584836fed6bad594492c2a80](https://github.com/EthSign/tokentable-unlocker-solana/commit/54c916fe785c9249584836fed6bad594492c2a80).
