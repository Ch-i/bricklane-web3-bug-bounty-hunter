---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-03-swell-eth-staking-deposit-bot-0-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-07-03T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md
tags:
- firm:codespect
- report:2026-07-03-swell-eth-staking-deposit-bot
title: '[H-01] Deposit front-run of an aged key captures 32 ETH to an operator credential'
vuln_class: []
---

# [H-01] Deposit front-run of an aged key captures 32 ETH to an operator credential

_Section severity (from Solodit section header): High_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-03-Swell-ETH-Staking-Deposit-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md)_

---

**Files:** [`gates.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/gates.py#L97-L137), [`web3_chain.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/web3_chain.py#L150-L162), [`plan.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/plan.py#L177-L246)

**Description:**

This off-chain bot decides which validator public keys receive a 32 ETH deposit funded from the pooled `DepositManager` balance. The contracts deliberately deny node operators any control over a validator’s withdrawal credential and always substitute the protocol’s own (the `DepositManager` address for swETH, a protocol-controlled `EigenPod` for rswETH), so on exit the staked ETH returns to the protocol. The `setupValidators` NatSpec in `IDepositManager` gives the off-chain service two front-running defenses: validate that each public key has not already been used for a validator setup, and snapshot the deposit contract’s `depositDataRoot` for re-check at broadcast. The bot performs only the snapshot (backed on-chain by `InvalidDepositDataRoot`) and never the used-key check, so the credential-fixing pre-deposit it is meant to catch goes unchecked. A malicious or compromised operator who holds a validator BLS key:

a. Registers key K with the `NodeOperatorRegistry` well in advance. The registry stores the pubkey and signature without verifying the signature (its own comment delegates this to an off-chain service, i.e. this bot). The registered signature is valid for the protocol credential, so K later passes the `bls_valid` gate;

b. Shortly before a run, submits a separate 1 ETH deposit to the beacon deposit contract for K, under a withdrawal credential the operator controls. Consensus fixes a validator’s credential on its first valid deposit, so K’s credential is now permanently the operator’s;

c. The bot later selects K (aged, registered, BLS-valid) and broadcasts the 32 ETH deposit. Consensus treats it as a top-up to an already-initialized validator and credits the 32 ETH to the operator’s credential, ignoring the protocol’s. Per `apply_deposit` in the consensus spec, the signature and withdrawal credential are used only for the first deposit to a pubkey; every later deposit only increases the balance;

The gates miss it. `key_age_mature` measures the time since K was added to the registry (`key_added_ts`, built from `OperatorAddedValidatorDetails` logs), not the time since the hostile pre-deposit, so registering K early clears the window with a full margin: [`gates.py:117-123`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/gates.py#L117-L123)

```python
now = ctx["finalized_ts"]
added = ctx["key_added_ts"]
min_age = ctx["min_key_age_secs"]
# @audit age anchored to registry-add time, not first on-chain deposit; aged key passes despite hostile pre-deposit
too_young = [pk for pk in ctx["pubkeys"] if now - added.get(pk, now) < min_age]
```

`not_on_beacon` reads the validator set at beacon HEAD, which a freshly pre-deposited key does not enter until the deposit is processed, so the pre-deposit is invisible during that lag; it never reads the deposit contract where the pre-deposit lands immediately. The `InvalidDepositDataRoot` guard only covers the short read-to-broadcast window, so a pre-deposit that settled earlier does not trigger it. No check asks whether a selected key already received a deposit, and to which credential.

**Impact:** Each front-run key permanently sends 32 ETH of pooled user funds to a validator whose withdrawal credential the operator controls, recoverable only by the operator on exit. A 1 ETH pre-deposit captures 32 ETH; the loss is direct, irrecoverable, repeatable across keys and runs, and applies to both swETH and rswETH. High if a malicious or compromised node operator is in scope; if operators are fully trusted, the front-run is an accepted risk under that assumption rather than a defect.

**Recommendation:** Before depositing, query the deposit-contract history (or a beacon source exposing prior/pending deposits) for each selected key and refuse the run if one exists under a credential other than the expected protocol or pod credential. Alternatives: anchor `key_age_mature` to the first on-chain deposit observed for the key rather than the registry-add time, or require operators to self-fund the full 32 ETH so there is no pooled top-up to capture. Separately, make `not_on_beacon` fail closed by distinguishing an empty beacon response from a complete one and cross-checking beacon finality against the execution finalized block.

**Status:** Fixed

**Client response:** Addressed in [ede12615](https://github.com/SwellNetwork/eth-staking-deposit-bot/commit/ede12615c831e707413e020ec4dfb340f8637aab). New `no_foreign_predeposit` gate: before depositing, the bot reads each selected key’s existing deposit credentials from the beacon node (Pectra `pending_deposits`) and halts the whole run if any key already carries a deposit under a credential other than its expected protocol/pod one. The finding’s "separately" recommendation — the fail-closed on-beacon read with an EL cross-check — is delivered under CODESPECT-03, and the same checks protect this read. The remaining dependency is the beacon node itself: the bot verifies it is synced, Pectra-aware, and ahead of the EL finalized block, and refuses on any doubt — but a node that lies within those checks is believed. Operator registration is governance-gated, which bounds who could attempt this.

**CODESPECT fix review:** Fixed (narrow residual). New `no_foreign_predeposit` gate halts on any key already deposited under a non-protocol credential; still reads at plan time, not re-checked at broadcast.
