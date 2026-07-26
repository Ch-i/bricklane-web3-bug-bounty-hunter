---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-ethcf-swapboard-v2-0-2-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-ethcf-swapboard-v2-0
title: Use `ReentrancyGuardTransient` instead of `ReentrancyGuard` for faster `nonReentrant`
  modifiers
vuln_class: []
---

# Use `ReentrancyGuardTransient` instead of `ReentrancyGuard` for faster `nonReentrant` modifiers

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-ethcf-swapboard-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md)_

---

**Description:** Use [ReentrancyGuardTransient](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/ReentrancyGuardTransient.sol) instead of `ReentrancyGuard` for faster `nonReentrant` modifiers:
```solidity
Swapboard.sol
4:import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
19:///      - Reentrancy protected via OpenZeppelin ReentrancyGuard
27:contract Swapboard is ISwapboard, ReentrancyGuard {
```

**ETHCF:** Fixed in commit [572f3c5](https://github.com/ETHCF/swapboard/commit/572f3c5d724b78fc3a2f304557a23c018f9fc31d).

**Cyfrin:** Verified.
