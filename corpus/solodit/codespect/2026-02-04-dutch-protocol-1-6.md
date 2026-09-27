---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-1-6
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[M-07] User’s contribution can be rebalanced to other collections'
vuln_class: []
---

# [M-07] User’s contribution can be rebalanced to other collections

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DutchVault.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DutchVault.sol)

**Description:**

The `setCollectionAllocations(...)` function has an option to rebalance the funds through collections but it doesn't check if there are any user contributions to the collection, nor it modifies user's contribution data in `AuctionAssist`. Users' contributions are bound to the collection address they have contributed to, and if admin decides to rebalance that allocation to other collections user contribution mapping will still point to the old inactive collection. This will cause users not being able to claim the rewards for their contribution, and because there is no option to withdraw funds from inactive collections, users will lose their contributions.

**Impact:** Users can lose 100% of their contributions.

**Recommendation:** Consider excluding user contributions from rebalancing calculations and adding an option for users to withdraw their funds from inactive collections.

**Status:** Fixed

**Client response:** Fixed in [ceac1ccf5ba85cbac5e71f160a58959c3aed6207](https://github.com/dutch-protocol/Protocol-Contracts/commit/ceac1ccf5ba85cbac5e71f160a58959c3aed6207)

**Client response:** Regression bug fixed here: [Protocol-Contracts issue #114](https://github.com/dutch-protocol/Protocol-Contracts/issues/114)
