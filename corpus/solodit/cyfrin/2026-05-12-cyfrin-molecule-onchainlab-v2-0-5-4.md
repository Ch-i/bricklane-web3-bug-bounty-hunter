---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-5-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`MoleculeOclDidRegistry::_linkDid` discards `_upsertDid`''s return value'
vuln_class: []
---

# `MoleculeOclDidRegistry::_linkDid` discards `_upsertDid`'s return value

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** `MoleculeOclDidRegistry::_upsertDid` is declared `returns (bool mutated)` but the only caller (`_linkDid`) ignores the return value. The unused return forces the callee to allocate, set, and return a stack slot it never produces useful information for. Either consume the value (e.g., emit a different event for the no-op branch, surface to relayers) or drop the return entirely.

```solidity
src/identity/MoleculeOclDidRegistry.sol
244:        _upsertDid(
245:            req.oclId,
...
255:        );
...
275:    ) internal returns (bool mutated) {
```

**Recommended Mitigation:** If callers truly never need it, change the signature to no return:

```solidity
function _upsertDid(...) internal {
    ...
    if (previousDidHash == newDidHash) return;
    ...
}
```

Hot path: invoked per `linkDid` and per element of `linkDidBatch`.

**Molecule:** Fixed in [468d036](https://github.com/moleculeprotocol/onchainlabs/commit/468d036).

**Cyfrin:** Verified.


\clearpage
