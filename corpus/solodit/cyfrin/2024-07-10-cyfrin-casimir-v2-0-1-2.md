---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-1-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: Spamming `requestUnstake()` to cause a denial of service in the unstake queue
vuln_class: []
---

# Spamming `requestUnstake()` to cause a denial of service in the unstake queue

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:**
- The function `requestUnstake()` allows users to request any amount, even `amount = 0`.
- The contract processes all unstake requests in a First-In-First-Out (FIFO) queue, handling earlier requests before later ones.
- The `remove()` function has a time complexity of O(n), which consumes gas.

This means an attacker could repeatedly call `requestUnstake()` to enlarge the unstake queue, causing the gas consumption of `fulfillUnstake()` to exceed the block gas limit.

**Impact:** Excessive gas usage when calling `fulfillUnstake()` could exceed the block gas limit, causing a DOS.

**Recommended Mitigation:** Consider setting a minimum unstake amount for the `requestUnstake()` function that is substantial enough to make spamming impractical.

**Casimir:**
Fixed in [4a5cd14](https://github.com/casimirlabs/casimir-contracts/commit/4a5cd145c247d9274c3f21f9e9c1b5557a230a01)

**Cyfrin:** Verified.
