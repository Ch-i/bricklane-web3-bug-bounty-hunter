---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-08-25-hyperwave-corewriter-0-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-08-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-25-Hyperwave-CoreWriter.md
tags:
- firm:codespect
- report:2025-08-25-hyperwave-corewriter
title: '[L-03] Receive of Native token is enabled while withdrawal is not possible'
vuln_class: []
---

# [L-03] Receive of Native token is enabled while withdrawal is not possible

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-08-25-Hyperwave-CoreWriter.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-25-Hyperwave-CoreWriter.md)_

---

**Files:** [`TradeStakeManager.sol`](https://github.com/SwellNetwork/hlp-corewriter/blob/5a19bb4373eaf3eb57d872f81d20177fb5cf9b2b/src/TradeStakeManager.sol#L62)

**Description:**

The `TradeStakeManager` contract contains a `receive()` function which allows receiving of the Native HYPE token by the contract.

There is however no option to withdraw the excess Native asset from the `TradeStakeManager`. The existing `withdrawNative(...)` function allows withdrawal of HYPE from `HyperCoreAccount` only.

**Impact:** Native HYPE asset transferred to the contract cannot be withdrawn.

**Recommendation:** Add a function allowing withdrawal of excess HYPE balance from the `TradeStakeManager` contract.

**Status:** Fixed

**Client response:** Resolved in [0096241fb91c1158c3b3526a06049bad08c7b0eb](https://github.com/SwellNetwork/hlp-corewriter/pull/58/commits/0096241fb91c1158c3b3526a06049bad08c7b0eb)
