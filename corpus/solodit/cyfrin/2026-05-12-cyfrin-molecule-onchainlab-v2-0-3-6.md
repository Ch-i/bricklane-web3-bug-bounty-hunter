---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-3-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`MoleculeOclDidRegistry::setRelayer` accepts arbitrary oldRelayer unverified'
vuln_class: []
---

# `MoleculeOclDidRegistry::setRelayer` accepts arbitrary oldRelayer unverified

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** `_revokeRole(RELAYER_ROLE, oldRelayer)` is a silent no-op when oldRelayer doesn't hold the role; admin invoking `setRelayer(0xdead, 0xCAFE)` only grants 0xCAFE while `RelayerUpdated(oldRelayer=0xdead, newRelayer=0xCAFE)` misleadingly suggests a rotation. The original (possibly compromised) relayer keeps the role.

**Files:**

`src/identity/MoleculeOclDidRegistry.sol:131-136`.

**Recommended Mitigation:** `if (!hasRole(RELAYER_ROLE, oldRelayer)) revert InvalidRelayer(oldRelayer);` before the revoke.

**Molecule:** Fixed in commit [6a36508](https://github.com/moleculeprotocol/onchainlabs/commit/6a36508).

**Cyfrin:** Verified.
