---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-2-9
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[L-10] withdrawCollectionBalance(...) can withdraw user contributions'
vuln_class: []
---

# [L-10] withdrawCollectionBalance(...) can withdraw user contributions

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DutchVault.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DutchVault.sol)

**Description:**

The `withdrawCollectionBalance(...)` function doesn't check if the collection has any user contributions before withdrawing the balance. This can cause owner mistakenly withdrawing user contributions.

**Impact:** Users can lose 100% of their contributions.

**Recommendation:** Check if there are any user contributions for the collection and let the owner to only withdraw protocol funded assets.

**Status:** Fixed

**Client response:** Fixed here: [PR-89](https://github.com/dutch-protocol/Protocol-Contracts/pull/89)
