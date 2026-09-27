---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-03-swell-eth-staking-deposit-bot-2-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-07-03T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md
tags:
- firm:codespect
- report:2026-07-03-swell-eth-staking-deposit-bot
title: '[L-02] No gate checks the operator enabled flag'
vuln_class: []
---

# [L-02] No gate checks the operator enabled flag

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-03-Swell-ETH-Staking-Deposit-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md)_

---

**Files:** [`web3_chain.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/web3_chain.py#L135-L142), [`plan.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/plan.py#L237-L245)

**Description:**

The on-chain `NodeOperatorRegistry` tracks an `enabled` boolean per operator and enforces it when consuming keys:

```solidity
// NodeOperatorRegistry.usePubKeysForValidatorSetup (L203-205)
if (!getOperatorForOperatorId[operatorId].enabled) revert CannotUseDisabledOperator();
```

The bot fetches the full operator tuple in `active_count` but reads only field index 4 (`activeValidators`) and discards field index 0 (`enabled`): [`web3_chain.py:135-142`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/web3_chain.py#L135-L142)

```python
op = self._nor.functions.getOperatorForOperatorId(op_id).call(...)
# @audit op[0] enabled flag discarded; disabled operator passes all gates, reverts on-chain
return int(op[4]) # activeValidators -- op[0] (enabled) is discarded
```

None of the seven gates reads it. So a key belonging to an operator disabled on-chain between dataset curation and a run (for example, disabled by Swell governance) passes all seven gates: `plan.ok == True`, the preview prints `gates: PASS`, and the operator launches execute. The condition surfaces only at the `simulate` step, where `usePubKeysForValidatorSetup` reverts with a bare `CannotUseDisabledOperator`. Because simulate runs before the confirm prompt, the run aborts before the operator is asked go/no-go, and because the whole batch is one transaction, one disabled-operator key fails the entire batch.

**Impact:** Liveness / DoS only; no funds move, since simulate precedes broadcast and the revert is atomic. The operator gets an opaque `CannotUseDisabledOperator` revert rather than a legible gate refusal naming the offending operator, and must manually investigate which operator is disabled before re-running. The trigger is a Swell-side operator disabled on-chain after curation, or a dataset listing an already-disabled operator; there is no attacker-reachable path.

**Recommendation:** Read `op[0]` (already fetched in the same tuple) and add an eighth gate `operators_enabled` that refuses any plan containing a key from a disabled operator, naming the operator. Alternatively, filter disabled operators out of `live_operators()` during chain reads. Either approach replaces the bare simulate revert with a legible, pre-broadcast refusal.

**Status:** Fixed

**Client response:** Update from the client: Addressed in [ede12615](https://github.com/SwellNetwork/eth-staking-deposit-bot/commit/ede12615c831e707413e020ec4dfb340f8637aab). Of the two options we chose the blocking gate (`operators_eligible`), and made it dataset-level: it fires, naming the operator, even if the disabled operator contributed no keys this run — so a stale dataset entry is corrected rather than hidden until the run it happens to be selected in.

**CODESPECT fix review:** Fixed. New `operators_eligible` gate reads the on-chain enabled flag and blocks a disabled operator pre-broadcast instead of an opaque simulate revert.
