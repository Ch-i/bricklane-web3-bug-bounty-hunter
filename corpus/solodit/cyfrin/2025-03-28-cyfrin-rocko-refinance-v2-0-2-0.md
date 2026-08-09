---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-28-cyfrin-rocko-refinance-v2-0-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-03-28T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-28-cyfrin-rocko-refinance-v2-0
title: Use `ReentrancyGuardTransient` instead of `ReentrancyGuard` or more gas-efficient
  `nonReentrant` modifiers
vuln_class: []
---

# Use `ReentrancyGuardTransient` instead of `ReentrancyGuard` or more gas-efficient `nonReentrant` modifiers

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-28-cyfrin-rocko-refinance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md)_

---

**Description:** Use [`ReentrancyGuardTransient`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/ReentrancyGuardTransient.sol) instead of `ReentrancyGuard` for more gas-efficient `nonReentrant` modifiers. The OpenZeppelin version would need to be bumped to 5.1.

**Rocko:** Fixed in commit [675f4b2](https://github.com/getrocko/onchain/commit/675f4b2e59cddf6c3f9f2e866f4401564bd0a006).

**Cyfrin:** Verified.
