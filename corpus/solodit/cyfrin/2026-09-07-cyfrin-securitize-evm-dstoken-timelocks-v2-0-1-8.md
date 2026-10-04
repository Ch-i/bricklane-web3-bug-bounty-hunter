---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0-1-8
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
title: 'Governance script gaps: the pre-handover checklist asserts stored values rather
  than installed behaviour or reachable authority'
vuln_class: []
---

# Governance script gaps: the pre-handover checklist asserts stored values rather than installed behaviour or reachable authority

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md)_

---

**Description:** `verify-governance` is the only gate before a handover the runbook describes as irreversible, and FR-15 requires it to fail loudly on drift. It reads storage slots and compares them to each other or to an operator-supplied argument. It does not establish that the authority it reports is reachable, that the code enforcing it is installed, or that the values it prints are sane. Six gaps share that shape, and each fix is a small edit to the same two scripts.

1. **`verify-governance` treats two unset slots as agreement.** Its comparison helper is `const same = (a: string, b?: string) => !!b && a.toLowerCase() === b.toLowerCase();`. The `!!b` guard exists for the optional command-line argument, not for the zero address, which arrives from a chain read as a truthy string. Both drift checks compare one chain read against another, so on a token that was never wired all four reads are zero, both checks pass, and the expected-address checks are skipped because their arguments were omitted.

   **Recommended:** reject the zero address explicitly rather than relying on truthiness, and require the expected timelock addresses so agreement is asserted against an intended value. Verifying an unwired token should be an explicit mode that reports it, not a silent pass.

2. **`verify-governance` reads no timelock role and asserts no delay.** Its entire timelock interface is `getMinDelay`, and that value is printed rather than checked, so it can never contribute a failure. No proposer, executor, canceller or admin membership is ever queried.

   **Recommended:** assert per controller that the temporary admin has been renounced and the controller self-administers, that proposer, canceller and executor membership matches an expected list, that at least one canceller is not also a proposer, since `TimelockController` grants `CANCELLER_ROLE` to every proposer and a canceller drawn only from that set cannot act against a compromised proposer, that no proposer or canceller is itself a controller, and that each delay equals its expected value with the master delay at least as long as each domain delay. `TimelockController` does not inherit `AccessControlEnumerable`, so assert against an operator-supplied expected-holder list or reconstruct membership from role events.

3. **`verify-governance` never asserts the mint-throttle configuration.** It contains no reference to the allowance, the window, the exceptional-mint delay or the grace period. All four are appended storage and read zero after an upgrade, so a token can pass the checklist in production with the control disabled and the exceptional path instant.

   **Recommended:** check that the allowance and window are non-zero, and that the exceptional-mint delay is non-zero and exceeds the master delay where a master timelock is registered, behind an opt-out for tokens intentionally running uncapped.

4. **Neither script checks that a service resolves the same trust service as the token.** Every service consumer resolves roles through its own registry entry, and `onlyComplianceAdmin` reaches the master principal through the compliance service's own pointer. Both scripts read the trust service from the token instead, and never compare the two.

   **Recommended:** assert that each governed service resolves the same trust service as the token, and after handover, that master authority holds on that instance too.

5. **Neither script validates the proposer set before the irreversible step.** The proposer list is split from a string with no address validation and no confirmation that the operator controls the resulting accounts. After handover the master timelock is the sole holder of master authority and of every owner, so a mistyped but checksum-valid proposer leaves nothing able to schedule anything, permanently.

   **Recommended:** before surrendering master authority, assert that each operator-supplied proposer holds the proposer and canceller roles, and refuse the handover otherwise. A dry-run that schedules and cancels a no-op operation would prove the set is live.

6. **Both scripts wrap their checks in over-broad `try` blocks, so failures read as successes.** In `verify-governance` the assertion sits inside the `try`, so an unreadable owner adds nothing to the failure list and the run still reports success. In `setup-governance` the ownership transfer sits inside the same `try` as the probe, so a reverted transfer is reported as a missing interface. Every service in the handover map is Ownable by construction, so the tolerant branch is dead for every legitimate entry.

   **Recommended:** probe with a `getCode` pre-check, classify the failure, and treat a definitively absent interface, an empty address and an indeterminate transport error as three distinct outcomes, all of them failures. Keep state-changing calls outside the handler.

**Securitize:** Mostly fixed in [76ceec4](https://github.com/securitize-io/dstoken/commit/76ceec4b9848b70b43cda04d3148119d02031098):
* 1 - fixed
* 2 - partially fixed; expected delays can be checked but role membership checks not implemented
* 3 - not done. Asserting the allowance is enabled only makes sense alongside the opt-out you mention, since some tokens may legitimately run uncapped, and that's a policy call we haven't made. Note the allowance is now share-denominated (issue 6), so any such assertion should test for non-zero rather than a magnitude
* 4 - fixed
* 5 - fixed with some limitations
* 6 - fixed

**Cyfrin:** Verified.
