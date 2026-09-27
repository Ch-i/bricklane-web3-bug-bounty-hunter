---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-02-hyperwave-sub-account-strategy-framework-1-4
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
title: '[I-05] Authorized wrap/unwrap leaves cannot execute against the non-payable
  sub-account'
vuln_class: []
---

# [I-05] Authorized wrap/unwrap leaves cannot execute against the non-payable sub-account

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md)_

---

**Files:** [SubAccountWithMerkleVerification.sol](https://github.com/SwellNetwork/boring-vault/blob/6f6cd157b9aa4f63263e70339bbc37106cede493/src/base/Roles/SubAccountWithMerkleVerification.sol), [CreateAprimeUSDYieldBasisMerkleRoot.s.sol](https://github.com/SwellNetwork/boring-vault/blob/6f6cd157b9aa4f63263e70339bbc37106cede493/script/CreateAprimeUSDYieldBasisMerkleRoot.s.sol)

**Description:**

The merkle root authorizes wrap (`WETH.deposit(...)`) and unwrap (`WETH.withdraw(...)`) leaves, but `SubAccountWithMerkleVerification` has no `receive(...)` / `fallback(...)` and a non-payable constructor, so it cannot hold or receive native ETH.

**Impact:** The unwrap reverts because `WETH.withdraw(...)` sends native ETH to the sub-account, and the wrap cannot be funded because the sub-account holds no native ETH. Both leaves are non-functional. No value is lost or frozen: WETH stays usable as an ERC20 through the `approve(...)` / `deposit(...)` / `withdraw(...)` leaves.

**Recommendation:** Remove the wrap/unwrap leaves from the root, or add `receive() external payable` if native-ETH flows are intended.

**Status:** Fixed

**Client response:** Fixed in commit [PR-86](https://github.com/SwellNetwork/boring-vault/pull/86/changes/86764e136ebb4708413f049a7d335154fe63b8d1).

**CODESPECT fix review:** Fixed in commit [`86764e1`](https://github.com/SwellNetwork/boring-vault/commit/86764e136ebb4708413f049a7d335154fe63b8d1).
