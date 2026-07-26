---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-5-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Don't copy entire `Assertion` struct from `storage` to `memory` in `DefaultSession::assertionResolvedCallback`
vuln_class: []
---

# Don't copy entire `Assertion` struct from `storage` to `memory` in `DefaultSession::assertionResolvedCallback`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** The `Assertion` struct is defined as:
```solidity
struct Assertion {
    uint256 sessionId;
    string resultCid;
    string calculationCid;
    address asserter;
    bool resolved;
    address[] winners;
    uint256[] totalXPs;
    uint256[] totalTimes;
}
```

It is very inefficient to copy this entire struct from `storage` to `memory`. Yet `DefaultSession::assertionResolvedCallback` does exactly this even though it only needs 4 fields:
```solidity
if (assertedTruthfully) {
    assertions[assertionId].resolved = true;
    Assertion memory dataAssertion = assertions[assertionId];
    emit DataAssertionResolved(
        dataAssertion.sessionId,
        dataAssertion.resultCid,
        dataAssertion.calculationCid,
        dataAssertion.asserter,
        assertionId
    );
    recordResults(assertions[assertionId].sessionId, assertionId);
```

**Recommended Mitigation:** Use a storage reference like this:
```diff
        if (assertedTruthfully) {
            assertions[assertionId].resolved = true;
-           Assertion memory dataAssertion = assertions[assertionId];
+           Assertion storage dataAssertion = assertions[assertionId];
            emit DataAssertionResolved(
                dataAssertion.sessionId,
                dataAssertion.resultCid,
                dataAssertion.calculationCid,
                dataAssertion.asserter,
                assertionId
            );
```

**Majority Games:**
Fixed in commit [fc5e0fa](https://github.com/Engage-Protocol/engage-protocol/commit/fc5e0faa81eae1edbef05d47c2e7652a236a7895).

**Cyfrin:** Verified.

\clearpage
