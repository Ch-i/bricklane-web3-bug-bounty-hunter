---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-3-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[I-02] Open TODOs'
vuln_class: []
---

# [I-02] Open TODOs

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DutchVault.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DutchVault.sol)

**Description:**

There are several TODO sections in the code and it's recommended to complete these TODOs before deployment. In particular, the TODO in `_splitProceeds(...)` function, which states that contribution calculation doesn't exclude new contributions that occurred after the purchase. This will cause `recordAndPullRewards(...)` function being called with inflated `contributorAmount_` value.

**Impact:** Recorded contributors will receive more share from the purchase than they should.

**Recommendation:** Exclude new contributions from the calculation.

**Status:** Fixed

**Client response:** Fixed in [67b3b69cef288936425f47313485286ffb4a87f0](https://github.com/dutch-protocol/Protocol-Contracts/commit/67b3b69cef288936425f47313485286ffb4a87f0)
