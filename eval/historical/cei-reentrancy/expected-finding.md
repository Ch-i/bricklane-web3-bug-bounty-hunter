---
id: cei-reentrancy-classic
title: "Reentrancy in withdraw() — funds sent before balance decrement"
post_mortem_url: https://swcregistry.io/docs/SWC-107/
incident_date: "various"
funds_at_risk_usd: null
target_protocol: "synthetic"
expected_vuln_class:
  - reentrancy
  - cei-violation
  - external-call
expected_severity: High
expected_locations:
  - file: LiquidityPool.sol
    function: withdraw
required_keywords:
  - reentrancy
  - withdraw
memorization_signals:
  - "the DAO"
  - "2016"
exclude_corpus_ids: []
grading_mode: keyword
---

# Canonical bug

`LiquidityPool.withdraw(amount)` follows a classic checks-effects-interactions
violation:

```solidity
function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount, "insufficient balance");
    uint256 pending = _pending(msg.sender);
    uint256 payout = amount + pending;
    (bool ok, ) = msg.sender.call{value: payout}("");   // <-- external call
    require(ok, "withdraw send failed");
    balances[msg.sender] -= amount;                     // <-- state update AFTER
    totalDeposits -= amount;
    rewardDebt[msg.sender] = ...;
}
```

A malicious depositor whose `receive()` fallback re-enters `withdraw` (or
`harvest`) during the `call{value:...}` will drain the pool: each
re-entrant call sees the original (un-decremented) `balances[attacker]`
and passes the require check, sending another `payout` of ETH before
the state update.

`deposit()` and `harvest()` exhibit a similar pattern (external call
before settling state in `deposit`'s reward-payout branch is also
re-enterable), so a comprehensive auditor would flag the whole family,
not just `withdraw`.

## Acceptance criteria

A passing finding must:

1. Identify reentrancy in `withdraw()` (and optionally `deposit()` /
   `harvest()` for full credit).
2. Note that the ETH send via `call{value: ...}("")` happens BEFORE
   the state update that decrements `balances` / `totalDeposits` /
   `rewardDebt`.
3. Be rated High or Critical.

This is a sanity-check entry: any working audit harness should catch a
classic CEI-violation reentrancy. If this fails, something is broken
in the harness pipeline, not the corpus or the LLM.
