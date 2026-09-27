---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-09-ignition-fogo-locker-1-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-09-Ignition-Fogo-Locker.md
tags:
- firm:codespect
- report:2026-02-09-ignition-fogo-locker
title: '[I-01] Session version adds missing validations from original instructions'
vuln_class: []
---

# [I-01] Session version adds missing validations from original instructions

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-09-Ignition-Fogo-Locker.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-09-Ignition-Fogo-Locker.md)_

---

**Files:** [`create_vesting_escrow_with_session.rs`](https://github.com/Tempest-Finance/fogo-locker/blob/c405ebd242141dafbed8476ebe9dc987de9695ab/programs/locker/src/instructions/escrow_instructions/create_vesting_escrow_with_session.rs)

**Description:**

The session version of `create_vesting_escrow` adds a validation that is missing in the original `create_vesting_escrow2.rs`:

```rust
constraint = sender_token.mint == token_mint.key() @ LockerError::InvalidEscrowTokenAddress
```

The original `CreateVestingEscrow2Ctx` does not validate that `sender_token.mint` matches `token_mint`.

**Impact:** This is an improvement in the session version. The original instruction should be updated to include this validation for consistency and security. If the token mint does not match, the transaction would fail.

**Recommendation:** Backport this validation to `create_vesting_escrow2.rs` for consistency across all escrow creation instructions.

**Status:** Fixed

**Client response:** Fixed. Added `sender_token.mint == token_mint.key()` constraint to `create_vesting_escrow2`, matching the validation already present in the session variant. [484c05d6c82c85fc3977060150f0a4307d2ea1de](https://github.com/Tempest-Finance/fogo-locker/pull/1/changes/484c05d6c82c85fc3977060150f0a4307d2ea1de)

**CODESPECT fix review:** This is fixed correctly.
