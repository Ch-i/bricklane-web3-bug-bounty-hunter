---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-03-swell-eth-staking-deposit-bot-2-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-07-03T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md
tags:
- firm:codespect
- report:2026-07-03-swell-eth-staking-deposit-bot
title: '[L-01] Duplicate operator name silently shadows an operator'
vuln_class: []
---

# [L-01] Duplicate operator name silently shadows an operator

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-03-Swell-ETH-Staking-Deposit-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md)_

---

**Files:** [`config.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/config.py#L83-L86), [`plan.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/plan.py#L116-L122)

**Description:**

The bot allocates deposits by a greedy-deficit ratio scheme, and every allocation and selection dict is keyed by `operator.name`. `load_dataset` (`config.py:83-86`) applies no name-uniqueness check. Three planning dicts are built by name: [`plan.py:116-122`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/plan.py#L116-L122)

```python
# @audit dicts keyed by o.name; duplicate name silently overwrites, shadowing one operator to zero
active = {o.name: chain.active_count(o.address, block) for o in live}
pending = {o.name: chain.pending_keys(o.address, block) for o in live}
capacity = {name: len(keys) for name, keys in pending.items()}
```

When two operators share a name (with distinct addresses), the second overwrites the first in each dict, so the shadowed operator’s pending keys, active count, and capacity are replaced by the twin’s. The allocator computes slots over the collided maps, and the selection loop iterates all operators but writes `selected[o.name]` (`plan.py:177-184`), so the shadowed operator deposits zero keys while the surviving twin fills both slots. The batch stays internally consistent (the selection sums to `n`, all keys BLS-valid), so no gate detects the drift and no contract backstop fires. The shortfall witness is itself computed from the same collided dicts, so the off-ratio state is never surfaced. The duplicate-*address* case differs: two distinct names sharing one address select the same keys twice and are caught loudly by the `no_duplicate_pubkeys` gate.

**Impact:** Config integrity only. One legitimate operator gets zero deposits while its same-name twin is over-funded, so the validator fleet drifts off the protocol’s target allocation ratios silently, with no diagnostic surfaced. There is no fund loss and no wrong credential: the 32 ETH still reaches a legitimate operator’s valid keys under the correct withdrawal credential. The trigger requires a fully-trusted config author to duplicate a name in the dataset; there is no attacker-reachable path.

**Recommendation:** Assert name uniqueness in `load_dataset` (raise if `len(names) != len(set(names))`), or, more robustly, key all allocation and selection dicts by operator address, which is unique by construction and maps to on-chain operator identity, eliminating the shadowing class of bug at its root.

**Status:** Fixed

**Client response:** Addressed in [ede12615](https://github.com/SwellNetwork/eth-staking-deposit-bot/commit/ede12615c831e707413e020ec4dfb340f8637aab). `load_dataset` now rejects duplicate operator names or addresses (case-normalized) at load. We chose this over re-keying the maps by address: operators are identified by name everywhere the tool reports to a human, so names must be unique anyway — and once that’s enforced at load, the by-name maps are safe.

**CODESPECT fix review:** Fixed. `load_dataset` now rejects duplicate operator names and addresses, so the silent shadowing cannot enter.
