---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-02-hyperwave-sub-account-strategy-framework-1-7
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
title: '[I-08] withdraw(...) reuses the deposit pool allowlist, so disabling a pool
  freezes existing positions'
vuln_class: []
---

# [I-08] withdraw(...) reuses the deposit pool allowlist, so disabling a pool freezes existing positions

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md)_

---

**Files:** [YieldBasisDecoderAndSanitizer.sol](https://github.com/SwellNetwork/boring-vault/blob/6f6cd157b9aa4f63263e70339bbc37106cede493/src/base/DecodersAndSanitizers/hyperwave/aprimeusd/YieldBasisDecoderAndSanitizer.sol)

**Description:**

`deposit(...)` and `withdraw(...)` both check the same `isAllowedPoolId[poolId]` flag. `setAllowedPoolId(poolId, false)`, which governance uses to stop new deposits, also makes the `withdraw(...)` decoder revert for positions already in that pool.

**Impact:** Disabling a pool blocks the standard exit for positions already in it, and the revert aborts the whole `manageWithMerkleVerification(...)` batch. No funds are lost: re-enabling the pool restores the exit, and the pdao-only `manage` path can unwind the position without the decoder. It is reachable only through a `GOVERNANCE_ROLE` write.

**Recommendation:** Track entry and exit allowlists separately, or document that disabling a pool also blocks withdrawals from it.

**Status:** Fixed

**Client response:** Fixed in this PR [PR-87](https://github.com/SwellNetwork/boring-vault/pull/87).

**CODESPECT fix review:** Fixed in commit [`82337c5`](https://github.com/SwellNetwork/boring-vault/commit/82337c59c614ba5f21703d54d1604da787f3ad3f).
