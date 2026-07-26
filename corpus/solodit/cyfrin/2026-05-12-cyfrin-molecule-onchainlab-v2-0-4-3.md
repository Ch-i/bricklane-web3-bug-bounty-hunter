---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-4-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`MoleculeOclDidRegistry::_upsertDid` produces colliding version numbers across
  DID rotations'
vuln_class: []
---

# `MoleculeOclDidRegistry::_upsertDid` produces colliding version numbers across DID rotations

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** Walkthrough: link A (v1) → link B (v2) → re-link A (`next.version != 0` branch: `next.version += 1` from existing 1 → 2). A and B both have version=2, contradicting NatSpec "Maintains monotonic version progression."

Off-chain indexers keying history by `(oclId, provider, subject, version)` collapse entries.

**Files:**

`src/identity/MoleculeOclDidRegistry.sol:264-311`.

**Recommended Mitigation:** Track a per-`(oclId, provider, subject)` global counter and assign `next.version = ++globalVersion[oclId][provider][subject]` in both branches.

**Molecule:** Fixed in commit [0396dec](https://github.com/moleculeprotocol/onchainlabs/commit/0396dec).

**Cyfrin:** Verified.
