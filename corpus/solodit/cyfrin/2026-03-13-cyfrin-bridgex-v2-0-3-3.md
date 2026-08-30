---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-3-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: For reentrancy protection use `transient` keyword or `ReentrancyGuardTransient`
  instead of declaring a `storage` variable
vuln_class: []
---

# For reentrancy protection use `transient` keyword or `ReentrancyGuardTransient` instead of declaring a `storage` variable

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** For reentrancy protection use `transient` keyword or [ReentrancyGuardTransient](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/ReentrancyGuardTransient.sol) instead of declaring a `storage` variable:
```solidity
PublicBridge.sol
67:    uint256 private _locked = 1;

PrivateChainBridge.sol
71:    uint256 private _locked = 1;
```

Both solutions require increasing the solidity version but this should be fine as the current version 0.8.18 is relatively old.

**BridgeX:**
Acknowledged; some of our chains are a bit older and don't have TSTORE and other modern opcodes like that. We'll make a note of it because the chain we will be deploying this on first is more modern, but we tend to like to keep these contracts as consistent as possible for all brands.
