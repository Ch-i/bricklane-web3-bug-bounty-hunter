---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-4-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: Use `calldata` instead of `memory` for external array parameters in `ArmadaGovernor::propose,
  proposeStewardSpend`
vuln_class: []
---

# Use `calldata` instead of `memory` for external array parameters in `ArmadaGovernor::propose, proposeStewardSpend`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ArmadaGovernor::proposeStewardSpend` and `ArmadaGovernor::propose` take `address[] memory`, `uint256[] memory`, `bytes[] memory`, `string memory` parameters but only read them. Solidity 0.8.x supports passing `calldata` directly to external functions that only read the inputs, which avoids the full calldata-to-memory copy on every call and is materially cheaper when the arrays are non-trivial.

**Impact:** Reduced gas cost on proposal creation hot paths (`propose` and `proposeStewardSpend`). The savings scale with the size of the `targets` / `values` / `calldatas` arrays and the description string.

**Recommended Mitigation:**
```solidity
function proposeStewardSpend(
    address[] calldata tokens,
    address[] calldata recipients,
    uint256[] calldata amounts,
    string calldata description
) external returns (uint256) { ... }

function propose(
    ProposalType proposalType,
    address[] calldata targets,
    uint256[] calldata values,
    bytes[] calldata calldatas,
    string calldata description
) external returns (uint256) { ... }
```

Note: the `RevenueLock` constructor cannot take `calldata` for reference types in 0.8.17; skip it.

**Armada:** Acknowledged.
