---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-3-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Use `ReentrancyGuardTransientUpgradeable` for faster `nonReentrant` modifiers
vuln_class: []
---

# Use `ReentrancyGuardTransientUpgradeable` for faster `nonReentrant` modifiers

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** Use [ReentrancyGuardTransientUpgradeable](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/master/contracts/utils/ReentrancyGuardTransientUpgradeable.sol) for faster `nonReentrant` modifiers:
```solidity
bridge/USDCBridgeV2.sol
27:import {ReentrancyGuardUpgradeable} from "@openzeppelin/contracts-upgradeable/utils/ReentrancyGuardUpgradeable.sol";
51:contract USDCBridgeV2 is IUSDCBridge, IWormholeReceiver, BaseRBACContract, ReentrancyGuardUpgradeable {
86:        __ReentrancyGuard_init();
```

**Securitize:** Acknowledged.
