---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-21T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-21-cyfrin-illuvium-stakingv3-v2-0
title: Unused `factory` storage in `L2RevenueDistributorV3`
vuln_class: []
---

# Unused `factory` storage in `L2RevenueDistributorV3`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md)_

---

**Description:** `L2RevenueDistributorV3` stores [`IAerodromeFactory public factory`](https://github.com/0xKaizenLabs/staking-contracts-v3/blob/c78653ed5f2e5a6d5ace13c303a8765fe30679b0/src/L2RevenueDistributorV3.sol#L54) and accepts it in `initialize`, but never reads or uses it. Swaps rely on `routes[i].factory`, and reserve math uses the LP pair address directly; no logic references the `factory` variable.

* If not needed: stop passing it to `initialize` and remove the public variable.
* If intended for safety: enforce it by checking `routes[i].factory == address(factory)` in swap functions to pin swaps to the approved factory.

**Illuvium:** Fixed in commit [5f273bc](https://github.com/0xKaizenLabs/staking-contracts-v3/commit/5f273bc8a196170162400c33a43efe2fb84f0013).

**Cyfrin:** Verified.
