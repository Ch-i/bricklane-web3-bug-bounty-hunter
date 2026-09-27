---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-16-tokentable-solana-merkle-airdrop-2-3
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
title: '[I-04] Miscalculated MerkleAirdrop size'
vuln_class: []
---

# [I-04] Miscalculated MerkleAirdrop size

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-16-TokenTable-Solana-Merkle-Airdrop.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Merkle-Airdrop.md)_

---

**Files:** [merkle_airdrop](https://github.com/EthSign/tokentable-unlocker-solana/tree/67a39faff7b848ae05c5e3ab45e36b60efcc622e/programs/merkle-token-distributor-solana/src/state/merkle_airdrop.rs#L20)

**Description:**

When creating the `MerkleAirdrop` account, use `calculate_size` to determine the allocated space.

```rust
pub fn calculate_size(uri_length: usize) -> usize {
    let mut size: usize = 0;
    size += 248; // Takes care of all non-vector items
    size += 4 + uri_length; // Add required data size of data vector

    size
}
```

The calculation seems to be implemented incorrectly as the total size of non-vector items should be `32 + 32 * 1 + 32 + 32 + 8 + 8 + 32 + 32 + 1 = 209` instead of `248`.

**Impact:** This would result in unnecessary rent wastage.

**Recommendation(s):** Calculate account space using the correct size.

**Status:** Fixed

**Update from TokenTable:** Updated account size calculation from a base of `248` to `209` in [08d6356a40601e5e5b0cf8cb6dfac9102da23583](https://github.com/EthSign/tokentable-unlocker-solana/pull/8/commits/08d6356a40601e5e5b0cf8cb6dfac9102da23583).
