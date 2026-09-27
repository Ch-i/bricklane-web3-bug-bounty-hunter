---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-08-21-tokentable-sui-0-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-08-21T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-21-TokenTable-Sui.md
tags:
- firm:codespect
- report:2025-08-21-tokentable-sui
title: '[C-01] The send_tokens(...) and mark_claimed(...) functions lack access control'
vuln_class: []
---

# [C-01] The send_tokens(...) and mark_claimed(...) functions lack access control

_Section severity (from Solodit section header): Critical_  
_Audit firm: CODESPECT_  
_Source report: [2025-08-21-TokenTable-Sui.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-21-TokenTable-Sui.md)_

---

**Files:** [`base_distributor.move`](https://github.com/EthSign/ecdsa-token-distributor-sui/tree/5536d80395d269b7d3392b20a924cbcae7a86344/sources/base_distributor.move#L144)

**Description:**

During the token claim process, the `mark_claimed(...)` function is called to mark tokens as claimed to prevent replay, and then the `send_tokens(...)` function is called to transfer tokens from the `Distributor` treasury to the recipient.

```move
public fun mark_claimed<T>(
    distributor: &mut Distributor<T>,
    claim_id: vector<u8>
) {
    assert!(!is_claimed(distributor, claim_id), E_CLAIM_ALREADY_CLAIMED);
    table::add(&mut distributor.claimed_claims, claim_id, true);
}

public fun send_tokens<T>(
    distributor: &mut Distributor<T>,
    recipient: address,
    amount: u64,
    ctx: &mut TxContext
) {
    let token_balance = sui::balance::split(&mut distributor.token_balance, amount);
    let tokens = sui::coin::from_balance(token_balance, ctx);
    transfer::public_transfer(tokens, recipient);
}
```

However, both functions lack access control, allowing anyone to call them directly.

**Impact:** A malicious actor can call `mark_claimed(...)` before a user claims, marking the tokens as claimed and causing the user’s claim to fail. They can also call `send_tokens(...)` directly to steal all unclaimed tokens from the `Distributor` treasury.

**Recommendation:** Use `public(package)` to restrict these functions so they can only be called by this package.

**Status:** Fixed

**Client response:** [44f9228953fb383f3f356061ba9e245e22389d8d](https://github.com/EthSign/ecdsa-token-distributor-sui/commit/44f9228953fb383f3f356061ba9e245e22389d8d) Note: `public(friend)` is deprecated.
