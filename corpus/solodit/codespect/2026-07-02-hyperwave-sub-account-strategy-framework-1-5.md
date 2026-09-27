---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-02-hyperwave-sub-account-strategy-framework-1-5
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
title: '[I-06] Merkle authorization assumes the decoder and target share the same
  function for a given selector'
vuln_class: []
---

# [I-06] Merkle authorization assumes the decoder and target share the same function for a given selector

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md)_

---

**Files:** [SubAccountWithMerkleVerification.sol](https://github.com/SwellNetwork/boring-vault/blob/6f6cd157b9aa4f63263e70339bbc37106cede493/src/base/Roles/SubAccountWithMerkleVerification.sol), [CreateAprimeUSDYieldBasisMerkleRoot.s.sol](https://github.com/SwellNetwork/boring-vault/blob/6f6cd157b9aa4f63263e70339bbc37106cede493/script/CreateAprimeUSDYieldBasisMerkleRoot.s.sol)

**Description:**

`_verifyCallData(...)` builds the leaf from `bytes4(targetData)` and the decoder-returned addresses, then `manage(...)` sends the same `targetData` to `target`, so both dispatch on the same selector. The binding is only complete when the decoder function and the target function for that selector share the same signature and the decoder returns all of that function’s address parameters. Nothing on-chain enforces this.

**Impact:** In the deployed roots the binding holds: the decoder functions are exact-signature mirrors of the bound targets, with spender / receiver / newOwner bound. A future leaf for a `(target, selector)` whose target function differs in signature from the decoder function (a cross-signature selector collision, `1/2^32`) could bind the wrong address or none. It is not reachable today and depends on a governance-authored leaf.

**Recommendation:** In the merkle tooling, assert each leaf’s signature resolves to the same selector on both decoder and target, and that the decoder returns every address parameter of the target function.

**Status:** Acknowledged

**Client response:** We implement the decoder and sanitizer and always have to ensure that the decoder and sanitizer is compatible with target contract.

**CODESPECT fix review:** Acknowledged.
