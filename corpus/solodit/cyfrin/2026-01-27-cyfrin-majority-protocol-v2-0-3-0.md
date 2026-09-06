---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-3-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Prevent negative assertion following previous truthful assertion in `DefaultSession::assertionResolvedCallback`
vuln_class: []
---

# Prevent negative assertion following previous truthful assertion in `DefaultSession::assertionResolvedCallback`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** `DefaultSession::assertionResolvedCallback` does not handle the state where:
* it is first called with `assertedTruthfully = true` for given `assertionId`
* it is later called with `assertedTruthfully = false` for the same `assertionId`

**Impact:** In this state `delete assertions[assertionId];` is executed even though the results have already been recorded based on the first truthful assertion.

**Recommended Mitigation:** `DefaultSession::assertionResolvedCallback` should revert if `assertions[assertionId].resolved`:
```diff
    function assertionResolvedCallback(bytes32 assertionId, bool assertedTruthfully) public override {
        require(msg.sender == address(optimisticOracle), NotOptimisticOracle(msg.sender));
+       require(!assertions[assertionId].resolved, AssertionAlreadyResolved(assertionId));
```

**Majority Games:**
Fixed in commit [99ec735](https://github.com/Engage-Protocol/engage-protocol/commit/99ec735d6b0a42c22fd0af6ae6ec8c91ef2e922d).

**Cyfrin:** Verified.
