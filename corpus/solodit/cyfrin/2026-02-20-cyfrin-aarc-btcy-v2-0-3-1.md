---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-3-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Use `ReentrancyGuardTransient` for faster `nonReentrant` modifiers
vuln_class: []
---

# Use `ReentrancyGuardTransient` for faster `nonReentrant` modifiers

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** Use [ReentrancyGuardTransient](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/ReentrancyGuardTransient.sol) for faster `nonReentrant` modifiers:
```solidity
DepositWithdraw.sol
5:import {ReentrancyGuard} from "openzeppelin-contracts/utils/ReentrancyGuard.sol";
20:contract DepositWithdraw is AccessControlEnumerable, ReentrancyGuard, Pausable, IDepositWithdraw {

IBTCYHub.sol
7:import {ReentrancyGuardUpgradeable} from "openzeppelin-contracts-upgradeable/utils/ReentrancyGuardUpgradeable.sol";
33:    ReentrancyGuardUpgradeable,
151:        __ReentrancyGuard_init();
```

**Aarc:** Fixed in commit [3a3e350](https://github.com/aarc-xyz/btcy-contracts-main/commit/3a3e3509086449ff6819ceeee5ec1e39c24cbaea).

**Cyfrin:** Verified.
