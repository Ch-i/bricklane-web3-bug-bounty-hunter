---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-03-26-tokentable-solana-unlocker-v2-2-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-03-26T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md
tags:
- firm:codespect
- report:2025-03-26-tokentable-solana-unlocker-v2
title: '[I-02] Unnecessary account ownership validation'
vuln_class: []
---

# [I-02] Unnecessary account ownership validation

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-03-26-TokenTable-Solana-Unlocker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md)_

---

**Files:** [`initialize.rs`](https://github.com/EthSign/tokentable-unlocker-solana/blob/7516b8c86cb305f9d9eb3ac77e7fcd7c6b60cc2f/programs/unlocker-v2-solana/src/instructions/initialize.rs), [`deploy.rs`](https://github.com/EthSign/tokentable-unlocker-solana/blob/7516b8c86cb305f9d9eb3ac77e7fcd7c6b60cc2f/programs/unlocker-v2-solana/src/instructions/deploy.rs)

**Description:**

Initialize and Deploy instructions are used the create new accounts: unlocker and config respectively. Those instruction’s context definitions contain the `init` attribute for the above accounts. Indicating that the accounts must not exist prior to calling those instructions. In the instruction handler, however exists an additional check that validates if those are new accounts; however, this check will always be true because the Anchor context definition ensures that they did not exist, hence the below require statement is unnecessary:

```rust
require!(ctx.accounts.config.admin == Pubkey::default(), TokenTableError::AlreadyDeployed);
```

**Impact:** No impact on code functionality.

**Recommendation:** Remove those require statements.

**Status:** Fixed

**Update from TokenTable:** Removed `require!()` statements in [ade803ab2628944df96a406546d5573692a13469](https://github.com/EthSign/tokentable-unlocker-solana/tree/ade803ab2628944df96a406546d5573692a13469).
