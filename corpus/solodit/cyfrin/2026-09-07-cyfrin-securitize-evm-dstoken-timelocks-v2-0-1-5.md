---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0-1-5
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
title: A single `TimelockController::scheduleBatch` containing `updateDelay` set to
  zero converts a delayed controller into an instant one for the cost of one delay
vuln_class: []
---

# A single `TimelockController::scheduleBatch` containing `updateDelay` set to zero converts a delayed controller into an instant one for the cost of one delay

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md)_

---

**Description:** `TimelockController::updateDelay` requires only that the caller be the controller itself and enforces no floor on the new value, so zero is accepted. `scheduleBatch` produces one operation id for N calls and `executeBatch` runs them atomically.

A compromised proposer can package `updateDelay` to zero, revocation of every honest canceller, and a self-grant of `PROPOSER_ROLE` into a single operation. After one `minDelay` and one `executeBatch`, `schedule` with a zero delay followed by `execute` in the same block is permanently available.

**Impact:** Total cost of full, permanent capture of the master timelock is one `minDelay`, defended against by exactly one operation id. The runbook's monitoring section alerts on raw `CallScheduled` without decoding calldata and without flagging operations whose target is the controller itself, so the decisive operation is not distinguished from routine traffic. `verify-governance` prints `getMinDelay` but never asserts it, so a mutated delay is never caught.

**Recommended Mitigation:** Alert specifically on `MinDelayChange` and on any scheduled operation targeting a timelock itself. Consider wrapping `TimelockController` to enforce a `minDelay` floor in `updateDelay`. Convert the `getMinDelay` print in `verify-governance` into an assertion against an expected value, and re-run it on a schedule rather than only at setup.

**Securitize:** Yes the particular scenario is possible but we haven't implemented any on-chain solution at this time. For mitigation in commit [3f4837b](https://github.com/securitize-io/dstoken/commit/3f4837b63856e09d8901c92bbc8cffbe79fdb98a) we've enhanced the `verify-governance` script to enforce expected delays and added monitoring guidance for `MinDelayChange`.

**Cyfrin:** Verified.
