---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-4-4
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
title: '`MoleculeOclDidRegistry::usedRequestId` nullifier scope mismatch with typed-data
  binding'
vuln_class: []
---

# `MoleculeOclDidRegistry::usedRequestId` nullifier scope mismatch with typed-data binding

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** `usedRequestId[bytes32]` is a single mapping; two requests for distinct `(oclId, provider, subject)` tuples that share a requestId bytes value (e.g., produced by independent off-chain pipelines) silently DoS each other.

**Files:**

`src/identity/MoleculeOclDidRegistry.sol:218-256`.

**Recommended Mitigation:** Replace with `usedRequestId[oclId][provider][subject][requestId]` so nullifier scope matches typed-data binding scope.

**Molecule:** Fixed in commit [9968086](https://github.com/moleculeprotocol/onchainlabs/commit/9968086).

**Cyfrin:** Verified.
