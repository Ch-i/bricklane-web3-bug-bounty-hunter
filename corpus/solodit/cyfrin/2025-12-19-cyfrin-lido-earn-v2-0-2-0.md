---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-12-19T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-19-cyfrin-lido-earn-v2-0
title: Use `ReentrancyGuardTransient` for faster `nonReentrant` modifiers
vuln_class: []
---

# Use `ReentrancyGuardTransient` for faster `nonReentrant` modifiers

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-19-cyfrin-lido-earn-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md)_

---

**Description:** Use [ReentrancyGuardTransient](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/ReentrancyGuardTransient.sol) for faster `nonReentrant` modifiers:
```solidity
Vault.sol
10:import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
32:abstract contract Vault is ERC4626, ERC20Permit, AccessControl, ReentrancyGuard, Pausable {
```

**Lido:** Fixed in commit [3d89267](https://github.com/lidofinance/defi-interface/commit/3d89267ee409eb0857abb9302dcc42337429e4f9).

**Cyfrin:** Verified.
