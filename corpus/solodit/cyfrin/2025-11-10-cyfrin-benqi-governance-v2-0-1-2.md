---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-1-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: '`UniquenessTests` incorrectly refers to the caller being included in the call
  identifier computation'
vuln_class: []
---

# `UniquenessTests` incorrectly refers to the caller being included in the call identifier computation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** `UniquenessTests::test_CallIdIncludesCaller` is implemented based on the assumption that the call identifier will differ when called by two different addresses as the caller is included in the computation; however, this is incorrect and the identifiers differ only because the nonce is incremented between `generateCallId()` invocations:

```solidity
function test_CallIdIncludesCaller() public {
    vm.prank(user1);
    bytes32 id1 = callerId.generateCallId();

    vm.prank(user2);
    bytes32 id2 = callerId.generateCallId();

    assertTrue(id1 != id2);
}
```

**Recommended Mitigation:** Remove this test altogether, or modify it to use snapshots to validate that, for the same nonce, the returned identifiers will be equal when called by distinct addresses.

**BENQI:** Fixed in PR [\#28](https://github.com/aragon/benqi-governance/pull/28).

**Cyfrin:** Verified.
