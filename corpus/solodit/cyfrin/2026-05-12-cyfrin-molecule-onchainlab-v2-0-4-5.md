---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-4-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`ValidationManager::invalidateNonce, validNonceFrom` are dead code'
vuln_class: []
---

# `ValidationManager::invalidateNonce, validNonceFrom` are dead code

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** `validNonceFrom` is written by `_invalidateNonce` and exposed via a getter, but never read by `_validateUserOp` or any validation gate. The function emits `NonceInvalidated` and rotates the floor, but no validation path rejects pending UserOps as a result.

**Files:**

`src/core/ValidationManager.sol:128-167`, `src/OnChainLab.sol:316-320`.

**Recommended Mitigation:** Either wire the validity floor into `_validateUserOp`, OR remove the entire nonce machinery and document that frontrun protection is via `state` only.

**Molecule:** Fixed in commit [18e0f04](https://github.com/moleculeprotocol/onchainlabs/commit/18e0f04).

**Cyfrin:** Verified.
