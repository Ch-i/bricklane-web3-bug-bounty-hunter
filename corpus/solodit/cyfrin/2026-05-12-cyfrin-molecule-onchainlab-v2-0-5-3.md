---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-5-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`MoleculeOclDidRegistry::_upsertDid` re-reads `next.version` after writing
  it'
vuln_class: []
---

# `MoleculeOclDidRegistry::_upsertDid` re-reads `next.version` after writing it

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** `MoleculeOclDidRegistry::_upsertDid` writes `next.version = previousVersion + 1` (or `next.version += 1`) and then re-reads the same storage slot inside the `emit DidLinked(..., next.version, ...)` argument list. The post-write SLOAD costs an avoidable warm SLOAD (~100 gas) on every `linkDid` call. The function is the per-link hot path.

A similar pattern exists for `previous.version` at line 288 - read once for the event after writing the unrelated `previous.active` field. Caching both into locals removes the redundant SLOADs.

```solidity
src/identity/MoleculeOclDidRegistry.sol
286:            DidLinkRecord storage previous = didRecord[oclId][provider][subject][previousDidHash];
287:            previous.active = false;
288:            emit DidDeactivated(oclId, provider, subject, previousDidHash, previous.version, requestId);
...
296:            next.version = previousVersion + 1;
...
299:            next.version += 1;
...
309:        emit DidLinked(oclId, provider, subject, did, newDidHash, next.version, tier, requestHash, proof, attestations);
```

**Recommended Mitigation:** Cache both versions to locals and use them in the emits:

```solidity
uint64 prevVersion = previous.version;       // before mutation
previous.active = false;
emit DidDeactivated(oclId, provider, subject, previousDidHash, prevVersion, requestId);
...
uint64 nextVersion;
if (next.version == 0) {
    uint64 previousVersion =
        previousDidHash == bytes32(0) ? 0 : didRecord[oclId][provider][subject][previousDidHash].version;
    nextVersion = previousVersion + 1;
} else {
    nextVersion = next.version + 1;
}
next.version = nextVersion;
...
emit DidLinked(oclId, provider, subject, did, newDidHash, nextVersion, tier, requestHash, proof, attestations);
```

**Molecule:** Fixed in commit [50f3770](https://github.com/moleculeprotocol/onchainlabs/commit/50f3770).

**Cyfrin:** Verified.
