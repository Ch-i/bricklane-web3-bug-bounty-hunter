---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-16-cyfrin-ethena-timelock-v2-0-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-05-16T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-16-cyfrin-ethena-timelock-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-16-cyfrin-ethena-timelock-v2-0
title: Use `ReentrancyGuardTransient` for more efficient `nonReentrant` modifiers
vuln_class: []
---

# Use `ReentrancyGuardTransient` for more efficient `nonReentrant` modifiers

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-16-cyfrin-ethena-timelock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-16-cyfrin-ethena-timelock-v2.0.md)_

---

**Description:** Use [`ReentrancyGuardTransient`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/ReentrancyGuardTransient.sol) for more efficient `nonReentrant` modifiers:
```diff
- import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
+ import {ReentrancyGuardTransient} from "@openzeppelin/contracts/utils/ReentrancyGuardTransient.sol";

- contract EthenaTimelockController is TimelockController, ReentrancyGuard {
+ contract EthenaTimelockController is TimelockController, ReentrancyGuardTransient {
```

**Ethena:** Fixed in commit [89d4190](https://github.com/ethena-labs/timelock-contract/commit/89d41901be3387c11c2150c19eb99883ed807d79#diff-8ca72e61ebf9a693737b5c9052aa3814e8b291e3d6dd0341fe88b5b5e781427bR5-R19).

**Cyfrin:** Verified.

\clearpage
