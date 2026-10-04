---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-02-hyperwave-sub-account-strategy-framework-1-10
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
title: '[I-11] Missing zero-address validation in SubAccountFundManager constructor'
vuln_class: []
---

# [I-11] Missing zero-address validation in SubAccountFundManager constructor

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md)_

---

**Files:** [SubAccountFundManager.sol](https://github.com/SwellNetwork/boring-vault/blob/6f6cd157b9aa4f63263e70339bbc37106cede493/src/base/Roles/SubAccountFundManager.sol)

**Description:**

The constructor in `SubAccountFundManager` assigns all three immutables directly from constructor arguments with no `address(0)` validation. In contrast, `YieldBasisDecoderAndSanitizer` does check the passed argument for `address(0)` before usage.

**Impact:** Since these variables are immutable, a deployment-time mistake is unrecoverable without redeploying the contract.

**Recommendation:** Add zero-address checks for constructor arguments.

**Status:** Fixed

**Client response:** fixed in [PR-87](https://github.com/SwellNetwork/boring-vault/pull/87).

**CODESPECT fix review:** Fixed in commit [`7830842`](https://github.com/SwellNetwork/boring-vault/commit/7830842d50e9e6effdf19341be277d825909b2c6).
