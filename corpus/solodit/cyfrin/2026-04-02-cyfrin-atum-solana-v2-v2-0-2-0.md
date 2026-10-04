---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-02-cyfrin-atum-solana-v2-v2-0-2-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-04-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-02-cyfrin-atum-solana-v2-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-02-cyfrin-atum-solana-v2-v2-0
title: Unused Error Variants in Escrow Program
vuln_class: []
---

# Unused Error Variants in Escrow Program

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-02-cyfrin-atum-solana-v2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-02-cyfrin-atum-solana-v2-v2.0.md)_

---

**Description:** Several error variants are defined in the escrow program’s `ErrorCode` enum but are never used in the codebase. For example:
```rust
    #[msg("Deposit with this ID already exists")]
    DepositAlreadyExists,
    #[msg("Deposit not found")]
    DepositNotFound,
    #[msg("Deposit has already been released")]
    DepositAlreadyReleased,
    #[msg("Deposit has already been refunded")]
    DepositAlreadyRefunded,
```

The program never reaches a point where it could return these custom errors.


**Impact:** Unused enum variants add noise and can suggest to future readers that explicit checks exist when they do not. Removing them (or wiring them to explicit checks for clearer client errors) would simplify the codebase.

**Recommended Mitigation:** Remove the four unused error variants. If the team wants more descriptive client-facing errors, add explicit `require!` checks that return these errors.

**Atum:** Fixed in [b4c128e](https://github.com/Atum-Labs/solana-escrow/commit/b4c128e78d8b91112a242b652cfb8b8f4ee0e736).

**Cyfrin:** Verified.

\clearpage
