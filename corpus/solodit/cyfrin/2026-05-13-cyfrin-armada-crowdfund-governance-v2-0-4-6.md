---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-4-6
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
title: Use named return variable to eliminate redundant local in 4 functions
vuln_class: []
---

# Use named return variable to eliminate redundant local in 4 functions

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** A local variable is declared solely to accumulate the return value and returned at the end. Converting the unnamed return to a named return parameter removes the local declaration line and the explicit `return` statement, saving the redundant stack allocation.

1. `ArmadaRedemption::circulatingSupply` at `contracts/governance/ArmadaRedemption.sol:196-203`. Local `total` declared at `:197`, returned at `:202`. Change `returns (uint256)` to `returns (uint256 total)`, replace `uint256 total = armToken.totalSupply();` with `total = armToken.totalSupply();`, drop `return total;`.

2. `ArmadaGovernor::_createRatificationProposal` at `contracts/governance/ArmadaGovernor.sol:645-667`. Local `ratId` declared at `:645`, returned at `:667`. Change `returns (uint256)` to `returns (uint256 ratId)`, replace `uint256 ratId = ++proposalCount;` with `ratId = ++proposalCount;`, drop `return ratId;`.

3. `ArmadaGovernor::proposeStewardSpend` at `contracts/governance/ArmadaGovernor.sol:716-730`. Local `proposalId` declared at `:716`, returned at `:730`. Change `returns (uint256)` to `returns (uint256 proposalId)`, replace `uint256 proposalId = ++proposalCount;` with `proposalId = ++proposalCount;`, drop `return proposalId;`.

4. `ArmadaGovernor::propose` at `contracts/governance/ArmadaGovernor.sol:803-817`. Local `proposalId` declared at `:803`, returned at `:817`. Same fix as (3).

**Armada:** Fixed in commit [78e1d7d](https://github.com/ship-armada/armada-poc/commit/78e1d7de913687609d5956a5cca4b82f233fb592).

**Cyfrin:** Verified.
