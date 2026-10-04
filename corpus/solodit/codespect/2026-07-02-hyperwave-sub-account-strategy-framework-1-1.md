---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-02-hyperwave-sub-account-strategy-framework-1-1
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
title: '[I-02] Slippage floors collapse to zero on deposit(...) and withdraw(...)'
vuln_class: []
---

# [I-02] Slippage floors collapse to zero on deposit(...) and withdraw(...)

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md)_

---

**Files:** [YieldBasisDecoderAndSanitizer.sol](https://github.com/SwellNetwork/boring-vault/blob/6f6cd157b9aa4f63263e70339bbc37106cede493/src/base/DecodersAndSanitizers/hyperwave/aprimeusd/YieldBasisDecoderAndSanitizer.sol)

**Description:**

`deposit(...)` and `withdraw(...)` compute `minAllowed = (expected * (slippageBase - maxSlippage)) / slippageBase` (with `expected = preview_deposit(assets, debt, false) / preview_withdraw(shares)`) and revert only when `provided < minAllowed`, with no zero guard. When `expected` is small enough that `minAllowed` truncates to `0`, a `provided` of `0` passes, removing the only on-chain slippage bound, since these arguments are not in the merkle leaf.

**Impact:** When the floor is `0`, a `deposit(...)` / `withdraw(...)` passes with `minShares` / `minAssets = 0`, so the call runs with no on-chain slippage protection and accepts any output amount, exposing it to value loss from price movement or sandwiching. In practice the floor reaches `0` only for dust-level inputs (the previews return `0` or revert for sufficiently small assets / shares), so a meaningful deposit or withdraw is not affected on the current pool. The gap matters for other LTs or pool states where the previews can return `0` over a wider range, which is relevant since multiple pools are planned.

**Recommendation:** Revert when `expectedShares` / `expectedAssets` is `0`, and when the provided `minShares` / `minAssets` is `0`.

**Status:** Fixed

**Client response:** fixed in [PR-87](https://github.com/SwellNetwork/boring-vault/pull/87).

**CODESPECT fix review:** Fixed in commit [`7bdc0d9`](https://github.com/SwellNetwork/boring-vault/commit/7bdc0d97c6085e6e82162cf8552cfc5f71ae5b3b).
