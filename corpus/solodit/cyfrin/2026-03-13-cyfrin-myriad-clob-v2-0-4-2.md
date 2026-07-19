---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-4-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: Consider switching to `ReentrancyGuardTransient`
vuln_class: []
---

# Consider switching to `ReentrancyGuardTransient`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** `NegRiskAdapter` inherits `ReentrancyGuard` and `MyriadCTFExchange` / `PredictionMarketV3ManagerCLOB` inherit `ReentrancyGuardUpgradeable`. Both variants store the lock flag in a regular storage slot (`_status`). Because the slot is cold at the start of each transaction, each guarded function call costs approximately:

OpenZeppelin ≥ 5.1.0 (the project already depends on v5.3.0) ships `ReentrancyGuardTransient` and `ReentrancyGuardTransientUpgradeable`, which store the flag in transient storage.

Affected in-scope contracts:

| Contract | Current base | Transient replacement |
|---|---|---|
| `NegRiskAdapter` | `ReentrancyGuard` | `ReentrancyGuardTransient` |
| `MyriadCTFExchange` | `ReentrancyGuardUpgradeable` | `ReentrancyGuardTransientUpgradeable` |
| `PredictionMarketV3ManagerCLOB` | `ReentrancyGuardUpgradeable` | `ReentrancyGuardTransientUpgradeable` |

**Recommended Mitigation:** Replace the base contract import and inheritance for each affected contract. For the upgradeable variants the `__ReentrancyGuard_init()` call in `initialize()` can be removed (the transient variant needs no initialization):

```solidity
// NegRiskAdapter
import "@openzeppelin/contracts/utils/ReentrancyGuardTransient.sol";
contract NegRiskAdapter is ReentrancyGuardTransient, ERC1155Holder { ... }

// MyriadCTFExchange / PredictionMarketV3ManagerCLOB
import "@openzeppelin/contracts-upgradeable/utils/ReentrancyGuardTransientUpgradeable.sol";
contract MyriadCTFExchange is ..., ReentrancyGuardTransientUpgradeable, ... { ... }
// remove: __ReentrancyGuard_init();
```

**Myriad:** Fixed in commit [`5993fc7`](https://github.com/Polkamarkets/polkamarkets-js/commit/5993fc77c583b4c6626e512380a27a5be9a0795d)

**Cyfrin:** Verified.
