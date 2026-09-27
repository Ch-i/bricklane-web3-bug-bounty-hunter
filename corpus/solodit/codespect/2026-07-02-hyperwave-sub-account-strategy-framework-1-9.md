---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-02-hyperwave-sub-account-strategy-framework-1-9
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
title: '[I-10] Direct manage(...) call will execute successfully even when the contract
  is paused'
vuln_class: []
---

# [I-10] Direct manage(...) call will execute successfully even when the contract is paused

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md)_

---

**Files:** [SubAccountWithMerkleVerification.sol](https://github.com/SwellNetwork/boring-vault/blob/6f6cd157b9aa4f63263e70339bbc37106cede493/src/base/Roles/SubAccountWithMerkleVerification.sol)

**Description:**

`manage(...)` in `SubAccountWithMerkleVerification.sol` is declared `public requiresAuth`, meaning it is independently callable as an external entry point and not restricted to being invoked only internally by `manageWithMerkleVerification(...)`. The `isPaused` check is only enforced in the `manageWithMerkleVerification(...)`, and since `manage(...)` itself contains no `isPaused` check, it can be called while contract is paused.

**Impact:** The `pause()` mechanism can be silently bypassed.

**Recommendation:** Add the `isPaused` check directly inside `manage(...)` function.

**Status:** Fixed

**Client response:** fixed in [PR-87](https://github.com/SwellNetwork/boring-vault/pull/87).

**CODESPECT fix review:** Fixed in commit [`fee2ad4`](https://github.com/SwellNetwork/boring-vault/commit/fee2ad4572a3e8066f959d7314f073ca5f5f5122).
