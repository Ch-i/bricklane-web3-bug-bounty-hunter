---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-4-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: Default-value initialisations in `ArmadaCrowdfund` and `RevenueLock` are redundant
vuln_class: []
---

# Default-value initialisations in `ArmadaCrowdfund` and `RevenueLock` are redundant

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** Explicit `= 0` / `= false` assignments at declaration emit a redundant `PUSH0` sequence the compiler cannot elide. Solidity default-initializes every type to zero-equivalent, so the assignment is observable-identical without the redundant opcode.

Affected sites:
- `contracts/crowdfund/ArmadaCrowdfund.sol:491, 492, 505, 564, 567, 736`
- `contracts/governance/RevenueLock.sol:127`

**Impact:** Small but additive gas savings across the affected functions.

**Recommended Mitigation:** Replace explicit-zero declarations with bare declarations:

```solidity
// before
uint256 totalAllocArm = 0;
bool refundMode_ = false;

// after
uint256 totalAllocArm;
bool refundMode_;
```

For the two `armStillOwed = 0` branches in `ArmadaCrowdfund::withdrawUnallocatedArm`, collapse to a single conditional assign so the default-zero path performs no writes.

**Armada:** Fixed in commit [b9c53e8](https://github.com/ship-armada/armada-poc/commit/b9c53e807cc8f8a40164c4b38996aec1196a0c21).

**Cyfrin:** Verified.
