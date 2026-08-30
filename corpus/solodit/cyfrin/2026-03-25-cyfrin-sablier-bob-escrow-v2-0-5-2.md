---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-5-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Use `ReentrancyGuardTransient` for faster `nonReentrant` modifiers
vuln_class: []
---

# Use `ReentrancyGuardTransient` for faster `nonReentrant` modifiers

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** Use [ReentrancyGuardTransient](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/ReentrancyGuardTransient.sol) for faster `nonReentrant` modifiers:
```solidity
SablierBob.sol
10:import { ReentrancyGuard } from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
42:    ReentrancyGuard, // 1 inherited component
```

**Sablier:** Acknowledged.
