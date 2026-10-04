---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-02-hyperwave-sub-account-strategy-framework-1-3
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
title: '[I-04] Merkle leaf binds decoder and target addresses but not their code'
vuln_class: []
---

# [I-04] Merkle leaf binds decoder and target addresses but not their code

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md)_

---

**Files:** [SubAccountWithMerkleVerification.sol](https://github.com/SwellNetwork/boring-vault/blob/6f6cd157b9aa4f63263e70339bbc37106cede493/src/base/Roles/SubAccountWithMerkleVerification.sol)

**Description:**

`_verifyManageProof(...)` builds the leaf from the decoder and target addresses, the value flag, the selector, and the decoded address args, but not from their `codehash`, so the proof never covers the code deployed at those addresses.

**Impact:** If the code behind a whitelisted decoder or target address changes, a previously generated proof still verifies, so governance must re-issue `manageRoot` whenever a whitelisted integration changes. The path is pdao-only, the in-scope decoders are immutable, and any harm requires a third-party target to upgrade to hostile behaviour.

**Recommendation:** Bind `target.codehash` (and `decoder.codehash`) into the leaf, or whitelist immutable protocol-controlled adapters instead of raw upgradeable endpoints.

**Status:** Acknowledged

**Client response:** This is a deliberate design. Typically, the `argumentAddresses` arguments encoded in the decoder will not be changed unless the target contract function is changed. In case it changed, `manageRoot` will be updated via pdao.

**CODESPECT fix review:** Acknowledged.
