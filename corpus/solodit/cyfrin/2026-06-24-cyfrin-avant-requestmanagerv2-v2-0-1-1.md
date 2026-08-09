---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-24-cyfrin-avant-requestmanagerv2-v2-0-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-06-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-24-cyfrin-avant-requestmanagerv2-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-24-cyfrin-avant-requestmanagerv2-v2-0
title: '`SimpleToken::idempotentMint, idempotentBurn` write the idempotency flag after
  the body executes instead of before'
vuln_class: []
---

# `SimpleToken::idempotentMint, idempotentBurn` write the idempotency flag after the body executes instead of before

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-24-cyfrin-avant-requestmanagerv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-24-cyfrin-avant-requestmanagerv2-v2.0.md)_

---

**Description:** The keyed `SimpleToken::mint` and `SimpleToken::burn` overloads guard against idempotency-key reuse with the `idempotentMint` and `idempotentBurn` modifiers (src/SimpleToken.sol:20-34). Both modifiers run the function body at `_;` and only afterwards record the key as used:

```solidity
modifier idempotentMint(bytes32 _idempotencyKey) {
    if (mintIds[_idempotencyKey]) {
        revert IdempotencyKeyAlreadyExist(_idempotencyKey);
    }
    _;                                  // body runs first
    mintIds[_idempotencyKey] = true;    // effect applied afterwards
}
```

This inverts the checks-effects-interactions ordering: the effect (recording the key in `mintIds` / `burnIds`) is applied after the interaction in the body (the `_mint` / `_burn` call) rather than before it. The canonical idempotency guard records the key as consumed before executing the body, so that any re-entrant call observes the key as already used and reverts.

With the current code the ordering is harmless. Each keyed overload's body is a single `_mint` / `_burn` call, and in OpenZeppelin Contracts Upgradeable v5.3.0 those route through `ERC20Upgradeable._update` (out of scope, traced for context), which only mutates balances and emits `Transfer`. It makes no external call and invokes no token-transfer or receiver hook - the `_beforeTokenTransfer` / `_afterTokenTransfer` hooks present in OZ v4 were removed in v5. `SimpleToken` does not override `_update`. Control therefore never leaves the contract between the key check and the key write, so a single key cannot be consumed twice within one transaction and no double-mint or double-burn is reachable today.

Here there is no current impact however this is also not good practice; writing the effect before the body removes the hazard unconditionally and costs nothing.

**Recommended Mitigation:** Apply the effect before running the body so the guard holds regardless of what the body later does:

```solidity
modifier idempotentMint(bytes32 _idempotencyKey) {
    if (mintIds[_idempotencyKey]) {
        revert IdempotencyKeyAlreadyExist(_idempotencyKey);
    }
    mintIds[_idempotencyKey] = true;
    _;
}
```

Apply the same reordering to `idempotentBurn`.

**Avant:** Fixed in commit [ff7803c](https://github.com/Avant-Protocol/Avant-Contracts-Max/commit/ff7803c1c3ee4c41936a56f4afcd104780563fb5).

**Cyfrin:** Verified.
