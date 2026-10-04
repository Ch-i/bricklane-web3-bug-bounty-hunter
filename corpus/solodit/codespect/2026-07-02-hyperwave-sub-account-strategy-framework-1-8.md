---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-02-hyperwave-sub-account-strategy-framework-1-8
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-07-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md
tags:
- firm:codespect
- report:2026-07-02-hyperwave-sub-account-strategy-framework
title: '[I-09] Interleaved verify/execute makes the YieldBasis slippage floor depend
  on a live preview'
vuln_class: []
---

# [I-09] Interleaved verify/execute makes the YieldBasis slippage floor depend on a live preview

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md)_

---

**Files:** [SubAccountWithMerkleVerification.sol](https://github.com/SwellNetwork/boring-vault/blob/6f6cd157b9aa4f63263e70339bbc37106cede493/src/base/Roles/SubAccountWithMerkleVerification.sol), [YieldBasisDecoderAndSanitizer.sol](https://github.com/SwellNetwork/boring-vault/blob/6f6cd157b9aa4f63263e70339bbc37106cede493/src/base/DecodersAndSanitizers/hyperwave/aprimeusd/YieldBasisDecoderAndSanitizer.sol)

**Description:**

`manageWithMerkleVerification(...)` verifies and executes each call in the same loop iteration: `_verifyCallData(i)` is followed immediately by `manage(i)`, so call `i` is verified only after calls `0..i-1` have already changed state. For `deposit` and `withdraw`, the decoder derives the slippage floor from the live `ILT.preview_deposit(...)` / `preview_withdraw(...)` value (`deposit_crvusd` and `redeem_crvusd` include no floor).

**Impact:** An earlier call in the same batch can move the state a later call’s preview reads, so the decoder’s slippage floor for that later call is computed against already-mutated state. The strategist-provided `min_shares` / `min_assets` still cap the loss, but if `lt` is spot-priced (set via `setPoolLT(...)`), the decoder’s floor can be manipulated.

**Recommendation:** Verify all calls in the batch before executing any of them, or document that the decoder floor is a secondary check dependent on live preview state.

**Status:** Fixed

**Client response:** fixed in [PR-87](https://github.com/SwellNetwork/boring-vault/pull/87).

**CODESPECT fix review:** Fixed in commit [`91e80ac`](https://github.com/SwellNetwork/boring-vault/commit/91e80ac18ccd65416775f0148d8ebde1830f2bf1).
