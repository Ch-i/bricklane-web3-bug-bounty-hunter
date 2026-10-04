---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-03-swell-eth-staking-deposit-bot-3-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-07-03T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md
tags:
- firm:codespect
- report:2026-07-03-swell-eth-staking-deposit-bot
title: '[I-02] funding_covers_queue gate never fires on dead code'
vuln_class: []
---

# [I-02] funding_covers_queue gate never fires on dead code

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-03-Swell-ETH-Staking-Deposit-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md)_

---

**Files:** [`gates.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/gates.py#L81)

**Description:**

`funding_covers_queue(...)` is one of the seven safety gates. Its stated job is to be an early, legible mirror of the `DepositManager`’s on-chain invariant, the contract reverts with `InsufficientETHBalance` unless the manager holds enough ETH to cover the new validators plus the ETH already owed to exiting validators. The gate is meant to catch that underfunding before any gas is spent. In the `funding_covers_queue`:

```python
need = ctx["n"] * (32 * 10**18) + ctx["exiting_eth_wei"]
have = ctx["deposit_manager_balance_wei"]
if have < need:
    return (
        f"underfunded: balance {have} < {ctx['n']}*32e18 + exitingETH "
        f"{ctx['exiting_eth_wei']} = {need}"
    )
```

The `if` condition will never be hit, because `n` is taken from the `have` and the `existingETH`, using the same 32-ETH constant, they are taken from the same source. Looks like nothing in the test suite tries to fire that gate, the only one aimed at underfunding is when `balance == exiting`.

**Impact:** Dead code. Gate does not capture the condition, yet it is already enforced by the correct calculation.

**Recommendation:** Remove the gate or reconsider when the gate would still make sense (e.g. if the values are re-read).

**Status:** Fixed

**Client response:** Addressed in [ede12615](https://github.com/SwellNetwork/eth-staking-deposit-bot/commit/ede12615c831e707413e020ec4dfb340f8637aab). Removed the gate and relocated the invariant it was reaching for ("sizing never overspends the balance") into a unit test over a pure sizing function. We did not take the re-read alternative: a fresh-read funding check already exists in `simulate()` (`InsufficientETHBalance`) just before broadcast, so a re-armed gate would duplicate it.

**CODESPECT fix review:** Fixed. The tautological funding gate is gone; the invariant is now a tested pure function and `simulate()` still re-checks the balance at broadcast.
