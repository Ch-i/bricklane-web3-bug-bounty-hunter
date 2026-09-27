---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-03-swell-eth-staking-deposit-bot-1-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-07-03T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md
tags:
- firm:codespect
- report:2026-07-03-swell-eth-staking-deposit-bot
title: '[M-01] A single BLS-invalid front-of-queue key can halt allocated node-operator
  deposits'
vuln_class: []
---

# [M-01] A single BLS-invalid front-of-queue key can halt allocated node-operator deposits

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-03-Swell-ETH-Staking-Deposit-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md)_

---

**Files:** [`gates.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/gates.py#L126-L137), [`plan.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/plan.py#L177-L184), [`web3_chain.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/web3_chain.py#L144-L148)

**Description:**

Each run’s selected keys pass a fixed sequence of gates before broadcast. `bls_valid` refuses to broadcast if any selected key’s registry signature does not verify against its withdrawal credentials, which guarantees the bot never deposits to an unverifiable key. The problem is the scope: the refusal is global over the whole batch, so one invalid key blocks every operator selected in the same run. Three properties combine. First, the registry accepts a bad-signature key with no verification: `NodeOperatorRegistry.addNewValidatorDetails` stores (`pubKey`, `signature`) without checking the signature (delegated to this bot by design), so any live, enabled operator can register a key whose signature does not commit to the protocol or pod credential, with no special on-chain state required. Second, the bot folds the number of failed keys across all operators into a single count (`bls_unverified = len(resolved.unverified)`, `plan.py:199`) and the gate refuses the whole plan if it is non-zero, with no notion of which operator owns the offending key: [`gates.py:126-137`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/gates.py#L126-L137)

```python
def bls_valid(ctx):
    n_bad = ctx["bls_unverified_count"]
    # @audit batch-global refusal, no per-operator isolation; one bad key halts whole fleet
    if n_bad:
        return f"{n_bad} key(s) failed BLS verification / pod recovery"
    return True
```

Third, selection is FIFO front-of-queue (`selected[o.name] = pending[o.name][:want]`), and the contract consumes each operator’s keys strictly front-to-back: `usePubKeysForValidatorSetup` reverts `NextOperatorPubKeyMismatch` unless the next key consumed is the operator’s current head, so the bot cannot skip a bad head key. A blocked run deposits nothing and changes no on-chain state, so re-runs against the same snapshot re-select the same head key and fail again. The halt is self-perpetuating until the key is removed on-chain or the selected allocation changes, and under normal target-ratio allocation a live operator is allocated regularly, so this is a realistic operating condition rather than a theoretical edge case.

**Impact:** A single live node operator, malicious or merely careless with one key, can halt all allocated node-operator deposits protocol-wide (both swETH and rswETH) until a maintainer removes the offending key on-chain. Honest operators selected alongside it are blocked even though their own keys are valid. No funds are lost and no wrong-credential deposit occurs: the gate fires before broadcast, so the 32 ETH per validator stays in the `DepositManager` and nothing is signed. The block is recoverable through a routine on-chain key removal and is legible in the witness log as a clean `deposit.blocked` record at the `bls_valid` gate.

**Recommendation:** Fault-isolate by operator instead of refusing the whole batch. When an operator’s front-of-queue key fails `bls_valid`, allocate zero to that operator and proceed with the operators whose front prefixes verify, surfacing the offending operator and key as an incident in the witness log. Isolation must be per-operator (the registry consumes keys front-to-back, so a single bad key inside a prefix cannot be skipped), which stops one operator’s bad key from halting the whole fleet while still refusing to deposit any unverifiable key.

**Status:** Acknowledged

**Client response:** Addressed in [ede12615](https://github.com/SwellNetwork/eth-staking-deposit-bot/commit/ede12615c831e707413e020ec4dfb340f8637aab). We considered the per-operator fault isolation and deliberately kept the batch-global halt: an unverifiable key from a vetted operator is an incident, and the right response is to stop and review out-of-band, not to isolate the operator and continue — the same whole-run-stop posture as CODESPECT-02. What we fixed is legibility: the refusal now names the offending operator, key, and cause — in the refusal itself and in the preview — so the review is immediately actionable.

**CODESPECT fix review:** Acknowledged. One bad key still halts the whole fleet; only the refusal message improved (names the operator, key, and cause).
