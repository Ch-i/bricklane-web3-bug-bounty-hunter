---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-05-15-tokentable-solana-eddsa-1-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-05-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-05-15-TokenTable-Solana-EDDSA.md
tags:
- firm:codespect
- report:2025-05-15-tokentable-solana-eddsa
title: '[I-02] The fee_collector_storage account constraint makes switching the fee_collector
  failed.'
vuln_class: []
---

# [I-02] The fee_collector_storage account constraint makes switching the fee_collector failed.

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-05-15-TokenTable-Solana-EDDSA.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-05-15-TokenTable-Solana-EDDSA.md)_

---

**Files:** [claim.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/87b79fe77b74d734fc5274da93300aa39444146c/programs/eddsa-token-distributor-solana/src/instructions/claim.rs#L110), [initialize.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/87b79fe77b74d734fc5274da93300aa39444146c/programs/eddsa-token-distributor-solana/src/instructions/initialize.rs#L70), [set_fee_collector.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/87b79fe77b74d734fc5274da93300aa39444146c/programs/eddsa-token-distributor-solana/src/instructions/set_fee_collector.rs#L52)

**Description:**

The EDDSA program allows different `fee_collector` programs to be configured for airdrop accounts. However, since the CPI to `fee_collector` program in the ctx uses an `Account<'info, fee_collector::models::FeeCollectorStorage>` type, it checks whether the `fee_collector_storage` account’s owner matches `fee_collector::models::FeeCollectorStorage::owner`. This causes the instructions to fail if a different `fee_collector` program is configured, due to an owner mismatch on the `fee_collector_storage` account.

```rust
pub fee_collector_storage: Option<
    Box<Account<'info, fee_collector::models::FeeCollectorStorage>>
>,
```

**Impact:** The airdrop account cannot be updated or used with a different `fee_collector` program, which is not the expected behavior.

**Recommendation(s):** In the ctx, specify the type of `fee_collector_storage` as `UncheckedAccount<'info>` instead of `Account<'info, T>`. During the CPI call, the `fee_collector` program will verify whether the account is as expected.

**Status:** Fixed

**Update from TokenTable:** Switched to `UncheckedAccount<'info>` for all usages of `fee_collector_storage` in all programs in [c0d34b3e6128278a11bf9df06812ffb87df3d779](https://github.com/EthSign/tokentable-unlocker-solana/commit/c0d34b3e6128278a11bf9df06812ffb87df3d779).
