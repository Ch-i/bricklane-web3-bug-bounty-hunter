---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-09-ignition-fogo-locker-1-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-02-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-09-Ignition-Fogo-Locker.md
tags:
- firm:codespect
- report:2026-02-09-ignition-fogo-locker
title: '[I-02] Lack of correct session validation'
vuln_class: []
---

# [I-02] Lack of correct session validation

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-09-Ignition-Fogo-Locker.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-09-Ignition-Fogo-Locker.md)_

---

**Original severity:** Best Practices

**Files:** [`create_vesting_escrow_with_session.rs`](https://github.com/Tempest-Finance/fogo-locker/blob/c405ebd242141dafbed8476ebe9dc987de9695ab/programs/locker/src/instructions/escrow_instructions/create_vesting_escrow_with_session.rs#L76), [`claim_with_session.rs`](https://github.com/Tempest-Finance/fogo-locker/blob/c405ebd242141dafbed8476ebe9dc987de9695ab/programs/locker/src/instructions/escrow_instructions/claim_with_session.rs#L52)

**Description:**

Both new instructions `create_vesting_escrow_with_session` and `claim_with_session` are designed to handle only session based calls. They both obtain the `user_pubkey` using special function:

```rust
let user_pubkey = Session::extract_user_from_signer_or_session(
    &ctx.accounts.signer_or_session,
    ctx.program_id,
)
.map_err(|_| LockerError::InvalidSession)?;
```

However if the `signer_or_session` is not a session account, but just a normal `Signer` it will not fail. As per the `fogo-sessions-sdk` code, this is the only condition for failure:

```rust
if !info.is_signer {
    return Err(SessionError::MissingRequiredSignature);
}
```

which will never be hit as Anchor requires the account to be a `Signer`.

**Impact:** The Session-only instructions allow non-session calls.

**Recommendation:** is to add `is_session` function to validate it correctly:

```rust
require!(
    is_session(&ctx.accounts.signer_or_session),
    LockerError::InvalidSession
);
```

**Status:** Fixed

**Client response:** Fixed. Added `is_session()` validation to both `create_vesting_escrow_with_session` and `claim_with_session` instructions. [484c05d6c82c85fc3977060150f0a4307d2ea1de](https://github.com/Tempest-Finance/fogo-locker/pull/1/changes/484c05d6c82c85fc3977060150f0a4307d2ea1de)

**CODESPECT fix review:** This is fixed correctly.
