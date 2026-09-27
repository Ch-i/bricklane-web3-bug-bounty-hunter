---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-03-swell-eth-staking-deposit-bot-2-2
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
title: '[L-03] Stale or rotated operator address crashes the run with an unhandled
  traceback'
vuln_class: []
---

# [L-03] Stale or rotated operator address crashes the run with an unhandled traceback

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-03-Swell-ETH-Staking-Deposit-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-03-Swell-ETH-Staking-Deposit-Bot.md)_

---

**Files:** [`web3_chain.py` (`pending_keys`)](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/web3_chain.py#L144-L148), [`web3_chain.py` (`active_count`)](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/web3_chain.py#L135-L142), [`cli.py`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/cli.py#L118-L150)

**Description:**

The bot reads each operator’s on-chain state through two paired calls. `active_count` resolves the operator id through the public mapping getter and tolerates an unknown address (`if op_id == 0: return 0`, since the getter never reverts). `pending_keys` has no such guard: [`web3_chain.py:144-148`](https://github.com/SwellNetwork/eth-staking-deposit-bot/blob/9298016aca651fef821aad0b9457dd9f4bdb8689/src/deposit_bot/web3_chain.py#L144-L148)

```python
# @audit no op_id == 0 guard; reverts NoOperatorFound for a stale address
details = self._nor.functions.getOperatorsPendingValidatorDetails(addr).call(block_identifier=bid)
```

On-chain, `getOperatorsPendingValidatorDetails` routes through `_getOperatorIdSafe`, which reverts on the exact `op_id == 0` case `active_count` swallowed:

```solidity
// NodeOperatorRegistry.sol _getOperatorIdSafe
operatorId = getOperatorIdForAddress[_operatorAddress];
if (operatorId == 0) {
    revert NoOperatorFound(_operatorAddress);
}
```

The public mapping returns 0 for any deleted address, and `updateOperatorControllingAddress` deletes the old controlling address. So if an operator rotates their controlling wallet, or the dataset lists a typo’d, not-yet-registered, or since-removed address, `active_count(addr)` (`plan.py:116`) returns 0 gracefully but `pending_keys(addr)` (`plan.py:121`) reverts `NoOperatorFound`. web3 surfaces this as a `ContractLogicError`, which is not a `BroadcastError`; the `build_plan` call at `cli.py:120` is unwrapped, and the only handler (`cli.py:147`) catches `BroadcastError` alone, so the process dies with a raw traceback before any gate runs and with no `*.blocked` witness record. This differs from the disabled-operator case, which reaches a clean simulate revert and a witness record after the gates; here the crash happens during planning, before any gate.

**Impact:** Whole-run liveness DoS with the worst failure shape in the codebase: an unhandled traceback rather than a structured abort, and no witness record. A single stale or typo’d operator row takes down the entire run. No funds move; the 32 ETH per validator stays in the `DepositManager`. The trigger is a fully-trusted config author’s stale/typo’d dataset address or an on-chain rotation (`updateOperatorControllingAddress`) after curation; there is no attacker-reachable path. Applies to both products.

**Recommendation:** Make `pending_keys` mirror `active_count`: resolve the operator id first and return `[]` when `op_id == 0`, so a misconfigured or rotated operator simply contributes no keys and the existing shortfall and witness machinery records it legibly. Alternatively, pre-validate at load that every dataset operator address resolves to a nonzero on-chain operator id, turning the mid-planning crash into a legible refusal.

**Status:** Fixed

**Client response:** Addressed in [ede12615](https://github.com/SwellNetwork/eth-staking-deposit-bot/commit/ede12615c831e707413e020ec4dfb340f8637aab). `pending_keys` now mirrors `active_count` — resolving the operator id first and returning empty for an unresolved address — and the operator is then blocked, named, by the same `operators_eligible` gate as CODESPECT-04.

**CODESPECT fix review:** Fixed. A rotated or unresolved address now yields a clean gate block instead of a raw `NoOperatorFound` traceback.
