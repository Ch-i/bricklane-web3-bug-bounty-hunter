---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-16-tokentable-solana-merkle-airdrop-2-4
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-04-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Merkle-Airdrop.md
tags:
- firm:codespect
- report:2025-04-16-tokentable-solana-merkle-airdrop
title: '[I-05] Redundant code'
vuln_class: []
---

# [I-05] Redundant code

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-16-TokenTable-Solana-Merkle-Airdrop.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Merkle-Airdrop.md)_

---

**Files:** [utils.rs](https://github.com/EthSign/tokentable-unlocker-solana/blob/67a39faff7b848ae05c5e3ab45e36b60efcc622e/programs/merkle-token-distributor-solana/src/instructions/utils.rs#L156)

**Description:**

The protocol contains multiple pieces of redundant code.

1. Both `if` and `require` statements are used when checking the result of the `merkle_verify` call; however, a single `require` statement would suffice;

```rust
pub fn _verify_and_claim<'info>(...) -> Result<u64> {
    //...
    if !merkle_verify(proof, root, leaf) {
        require!(false, TokenTableError::InvalidProof);
    }
}
```

**Impact:** Redundant code hinders readability and increases deployment costs.

**Recommendation(s):** It is recommended to optimize the redundant code.

**Status:** Fixed

**Update from TokenTable:** `merkle_verify()` require statement simplified in [2025f68a4d699cc4997c133775f26f2768aba7e6](https://github.com/EthSign/tokentable-unlocker-solana/pull/8/commits/2025f68a4d699cc4997c133775f26f2768aba7e6).
