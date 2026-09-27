---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-03-swell-eth-staking-deposit-bot-3-3
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-07-03T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md
tags:
- firm:codespect
- report:2026-07-03-swell-eth-staking-deposit-bot
title: '[I-04] Operator can steer redistributed surplus by deepening its own queue'
vuln_class: []
---

# [I-04] Operator can steer redistributed surplus by deepening its own queue

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-03-Swell-ETH-Staking-Deposit-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md)_

---

**Files:** [`allocate.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/allocate.py#L57), [`cli.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/cli.py#L69)

**Description:**

`allocate(...)` places each new validator with the operator furthest below its target ratio, converging the active fleet toward the configured ratios. When capacity (an operator’s pending-key count) is passed, an operator that cannot fill its share has its slots flow to operators that still have keys:

```python
def has_room(o: Operator) -> bool:
    return capacity is None or alloc[o.name] < capacity.get(o.name, 0)
# ...
candidates = [o for o in live if has_room(o)]
```

So an operator that keeps a deep, mature pending queue while peers stay shallow repeatedly absorbs the redistributed surplus, gaining active-validator share (and the rewards that follow it) above its target ratio. The drift is recorded and printed, but only as a non-blocking warning in `_print_preview(...)`; there is no concentration gate among the seven, so the deposit proceeds. It is self-correcting (an over-share operator carries a negative deficit until peers catch up), and `min_key_age` (12h) only rate-limits how fast a fresh queue can be built. No funds are at risk; absorbed validators still use the verified protocol/pod withdrawal credential.

**Impact:** Off-ratio concentration toward whichever operator keeps the deepest queue; economic and ratio drift only, no fund loss or wrong credentials.

**Recommendation:** Confirm with the protocol owner whether the concentration warning should become a blocking gate above some threshold rather than advisory auto-proceed.

**Status:** Acknowledged

**Client response:** Confirming per the recommendation: the concentration warning stays advisory. We do not read a deep queue as steering — supplying mature keys is exactly what operators are asked to do, and surplus redistributes only when peers have no keys to take their own share. A blocking gate would leave user capital idle to penalize the one operator that came prepared, enforcing a ratio that self-corrects anyway (an over-share operator is skipped until peers catch up). Key maturity rate-limits how fast a queue can be deepened, and the post-run share is shown in the preview before confirm.

**CODESPECT fix review:** Acknowledged (accepted). The concentration signal stays an advisory warning, no code change.
