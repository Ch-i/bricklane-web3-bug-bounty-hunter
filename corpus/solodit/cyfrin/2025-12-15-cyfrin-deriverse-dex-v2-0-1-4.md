---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Anyone can sell anyone else's market seat
vuln_class: []
---

# Anyone can sell anyone else's market seat

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** In the `sell_market_seat` function the `check_signer` parameter is incorrectly set to false, allowing any user to force-sell another user's market seat without proper authorization.
```rust
let mut client_state = ClientPrimaryState::new_for_perp(
    program_id,
    client_primary_acc,
    &ctx,
    signer,
    system_program,
    0,
    false,  // alloc = false (correct)
    false,  // @audit why false? can I supply others's
)?;
```
`new_for_perp` calls `ClientPrimaryAccountHeader::from_account_info_unchecked` since we have set the `check_signer` flag to false, the `from_account_info_unchecked` only makes sure that the account `signer` is signer, however it does not make sure that the signer account is indeed the one `wallet_address` stored in  `ClientPrimaryAccountHeader`.. which means anyone could pass a anyone's valid `ClientPrimaryState` and sell their seat without consent.

Attack Scenario
- Attacker finds any `client_primary_acc` with a market seat
- Attacker call `sell_market_seat` with their own wallet as `signer` and Victim's `client_primary_acc`
- No validation occurs to check if the signer owns the client account
- Victim's market seat is sold and funds go to the victim's account, and the attacker closed victim's position without consent

**Impact:** Any user can close any other user's seats

**Recommended Mitigation:** Pass the `is_signer` flag set to true like we have done in `buy_market_seat`
```rust
// ...existing code...
let mut client_state = ClientPrimaryState::new_for_perp(
    program_id,
    client_primary_acc,
    &ctx,
    signer,
    system_program,
    0,
    false,
    true,   // check_signer = true
)?;
// ...existing code...
```
**Deriverse**
Fixed in commit: [9a5678](https://github.com/deriverse/protocol-v1/commit/9a56789cd5f5b479022da7c4da97f8ef1ee6aaf8)

**Cyfrin:** Verified.
