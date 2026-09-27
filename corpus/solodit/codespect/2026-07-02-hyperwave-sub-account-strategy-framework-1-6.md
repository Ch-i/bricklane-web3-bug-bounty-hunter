---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-02-hyperwave-sub-account-strategy-framework-1-6
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-07-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md
tags:
- firm:codespect
- report:2026-07-02-hyperwave-sub-account-strategy-framework
title: '[I-07] maxSlippage and slippageBase are global, not configurable per poolId'
vuln_class: []
---

# [I-07] maxSlippage and slippageBase are global, not configurable per poolId

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md)_

---

**Files:** [YieldBasisDecoderAndSanitizer.sol](https://github.com/SwellNetwork/boring-vault/blob/6f6cd157b9aa4f63263e70339bbc37106cede493/src/base/DecodersAndSanitizers/hyperwave/aprimeusd/YieldBasisDecoderAndSanitizer.sol)

**Description:**

`isAllowedPoolId` and `poolIdToLT` are configured per `poolId`, but `maxSlippage` and `slippageBase` are single values shared by the whole decoder. The team confirmed support for multiple pools is planned, so one slippage band would govern every pool the decoder serves.

**Impact:** With multiple pools enabled, the same slippage band applies to every pool. This band is a secondary check; the strategist-provided `min_shares` and `min_assets`, enforced by the LT, are the primary protection.

**Recommendation:** Configure `maxSlippage` and `slippageBase` per `poolId`.

**Status:** Fixed

**Client response:** Fixed in [PR-87](https://github.com/SwellNetwork/boring-vault/pull/87).

**CODESPECT fix review:** Fixed in commit [`9e24f4d`](https://github.com/SwellNetwork/boring-vault/commit/9e24f4d09d8137b50e9c172f436624f4bf13055d).
