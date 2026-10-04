---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0-1-6
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0
title: '`DSToken::scheduleOverCapIssuance` includes `block.timestamp` in the operation
  id, so one salt can schedule the same mint repeatedly in different blocks'
vuln_class: []
---

# `DSToken::scheduleOverCapIssuance` includes `block.timestamp` in the operation id, so one salt can schedule the same mint repeatedly in different blocks

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md)_

---

**Description:** The operation id is `keccak256(abi.encode(_to, _amount, _salt, block.timestamp))`, guarded by `require(pendingMints[operationId].readyAt == 0)`. Because the timestamp is part of the preimage, the guard binds only within a single block. The same `_to`, `_amount` and `_salt` submitted in any later block yields a different id and a second, independently executable pending mint.

The salt is the field an operator would expect to prevent this. The governance runbook establishes exactly that convention for the administrative timelocks, deriving the salt from a platform request id so that _"retries are idempotent - same request, same id, revert = already scheduled"_. That property holds there because `TimelockController::hashOperation` is a pure function of its arguments. The mint timelock reuses the same vocabulary and the same operator mental model while adding a term that defeats it.

No attacker is required. Two accidental submissions of one request - a double-clicked approval, a retried job, a transaction replaced under a fresh nonce, a reorg re-mining the schedule at a different timestamp - each create a live pending mint, and each executes.

**Spec-Intent Gap:**

`timelocks.md` FR-12:

> Re-scheduling an identical operation reverts.

Code permits behavior contradicting this commitment for the exceptional-mint path. The shipped documents also disagree with each other: `bc-2132-mint-throttling-flows.md` Flow 11 presents the different-block case as acceptable, which is sound as replay protection but is not idempotency.

**Impact:** A duplicated issuance request mints twice. Recovery is not automatic: the operator must notice that two scheduling events were emitted for one request and cancel the surplus through `cancelOverCapMint`, which is master-gated and therefore delayed after handover. Cancelling the id the platform recorded does not neutralise the other, since they differ and only one is known.

The id is also not computable before broadcasting, so the platform cannot correlate its request without parsing the emitted event.

**Recommended Mitigation:** Derive the id as `keccak256(abi.encode(_to, _amount, _salt))`. The salt then behaves as the runbook already documents it, the duplicate guard becomes genuinely idempotent, and the id becomes precomputable. Existing tombstoning of executed and cancelled operations continues to prevent reuse of a spent salt.

**Securitize:** Fixed in commit [ea6184f](https://github.com/securitize-io/dstoken/commit/ea6184f51263f23ff16d74be6543f250b1c8f3aa) as recommended.

**Cyfrin:** Verified.
