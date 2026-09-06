---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-12-cyfrin-shutter-security-council-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-12-cyfrin-shutter-security-council-v2-0
title: Guard replacement during council rotation resets veto state, allowing previously-vetoed
  proposals to execute
vuln_class: []
---

# Guard replacement during council rotation resets veto state, allowing previously-vetoed proposals to execute

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-12-cyfrin-shutter-security-council-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-12-cyfrin-shutter-security-council-v2.0.md)_

---

**Description:** `council` is immutable in `SecurityCouncilAzorius`. Council rotation requires deploying a new guard contract and calling `Azorius.setGuard(newGuard)`. The new guard starts with a clean, empty `vetoedTxHash` mapping.

If there are proposals currently in the execution window (after timelock, before expiry) that were vetoed under the old guard, those vetoes are NOT in the new guard. The instant `Azorius.setGuard(newGuard)` is executed on-chain, the old vetoes become unenforceable.

As per the `CouncilRotation Procedure` on the `OPERATIONS` file. The veto of existing vetoed txs happens after the new council has been set as the guard on the `Azourius` contract. This creates a gap that could be theoretically front-run to execute a txHash that should be vetoed.


**Attack Scenario:**

1. Attacker submits a malicious proposal
2. Council vetoes it under the old guard — `vetoedTxHash[malicious_hash] = true`
3. The proposal is within its execution window (after timelock)
4. Council rotation is triggered
5. New guard is deployed with empty state, `Azorius.setGuard(newGuard)` is called
6. Old guard's veto state is no longer enforced
7. Attacker immediately executes the malicious proposal through the new guard


**Impact:** During council rotation, there is a time window during which previously vetoed proposals can be executed. This is a race condition between the guard switch and any executor of a malicious proposal.

**Recommended Mitigation:**
- In the `OPERATIONS.md` rotation procedure, add: **"Before executing `setGuard(newGuard)`, the new council must pre-veto all currently-vetoed hashes in the new guard."**
- Consider adding an `initialVetoes` parameter to the constructor to batch-initialize veto state atomically at deployment
- Document this gap prominently in the rotation runbook as a mandatory pre-flight step

**Blockful:** Fixed in commit [227d737](https://github.com/blockful/shutter-security-council/commit/227d7376b7387c1f88c252dcdf8b9b3d2377ca91) && [6a53351](https://github.com/blockful/shutter-security-council/commit/6a533516f8c22f65d45ead714fe5049ec7b442f6)

**Cyfrin:** Verified. `SecurityCouncilAzorius` now inherits `Ownable`. Council rotations will happen on the `SecurityCouncilAzorius` contract, no changes on the `Azorius` guard will happen. Council rotation won't disrupt the current veto state
