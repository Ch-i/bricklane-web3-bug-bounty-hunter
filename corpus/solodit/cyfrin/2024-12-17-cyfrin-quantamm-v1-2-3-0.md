---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-quantamm-v1-2-3-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-quantamm-v1-2
title: Use of solidity `assert` instead of foundry asserts in test suite
vuln_class: []
---

# Use of solidity `assert` instead of foundry asserts in test suite

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-quantamm-v1.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md)_

---

**Description:** In [`QuantAMMWeightedPool8Token`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/test/foundry/QuantAMMWeightedPool8Token.t.sol#L312) tests `assert` is used instead of foundry `assertEq`

Foundry [`assertEq`](https://book.getfoundry.sh/reference/forge-std/std-assertions) provides better error information when failing such as the two values compared. Consider using `assertEq` instead of solidity `assert`

**QuantAMM:** Fixed in [`414d4bc`](https://github.com/QuantAMMProtocol/QuantAMM-V1/commit/414d4bc3d8699f1e4620f0060226b4e23ff3b010) and [`ca1e441`](https://github.com/QuantAMMProtocol/QuantAMM-V1/pull/27/commits/ca1e441d4feb2a1ffe202121857207f3e15fbc2f)

**Cyfrin:** Verified
