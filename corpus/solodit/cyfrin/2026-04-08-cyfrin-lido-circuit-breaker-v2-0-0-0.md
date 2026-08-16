---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-08-cyfrin-lido-circuit-breaker-v2-0-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-04-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-08-cyfrin-lido-circuit-breaker-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-08-cyfrin-lido-circuit-breaker-v2-0
title: Missing named mapping value parameters in `Registry.Storage`
vuln_class: []
---

# Missing named mapping value parameters in `Registry.Storage`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-08-cyfrin-lido-circuit-breaker-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-08-cyfrin-lido-circuit-breaker-v2.0.md)_

---

**Description:** Three mappings in `Registry.Storage` declare named keys but omit names for their value types, reducing readability and ABI clarity:

```solidity
// Registry.sol lines 18-21
mapping(address pausable => address) pauser;
mapping(address pausable => uint256) oneBasedIndex;
mapping(address pauser => uint256) pausableCount;
```

**Recommended Mitigation:**
```diff
-mapping(address pausable => address) pauser;
-mapping(address pausable => uint256) oneBasedIndex;
-mapping(address pauser => uint256) pausableCount;
+mapping(address pausable => address pauser) pauser;
+mapping(address pausable => uint256 oneBasedIndex) oneBasedIndex;
+mapping(address pauser => uint256 pausableCount) pausableCount;
```

**Lido:** Fixed in commit [cabcfec](https://github.com/lidofinance/circuit-breaker/commit/cabcfec9f22380a8905435102dad94d829231abd).

**Cyfrin:** Verified.
