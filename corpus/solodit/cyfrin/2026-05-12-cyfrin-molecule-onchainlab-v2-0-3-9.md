---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-3-9
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`ERC7484Registry::revoke` allows revoking an already revoked attestation'
vuln_class: []
---

# `ERC7484Registry::revoke` allows revoking an already revoked attestation

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** When calling `ERC7484Registry::revoke`, the function only checks whether the attestation exists by verifying that `attestation.createdAt` is non-zero. It does not check whether the attestation has already been revoked by inspecting `attestation.revocationTime`.

> src/ERC7484Registry/ERC7484Registry.sol#revoke
```solidity
    function revoke(address module) external {
        AttestationRecord storage attestation = _attestations[module][msg.sender];
>>      if (attestation.createdAt == 0) revert AttestationNotFound();
        attestation.revocationTime = uint48(block.timestamp);
        emit ModuleRevoked(module, msg.sender, uint48(block.timestamp));
    }
```

As a result, calling `revoke` on an already revoked attestation will succeed without reverting. The `revocationTime` will be overwritten with the current block timestamp and a `ModuleRevoked` event will be emitted again, even though the attestation was already in a revoked state.

**Impact:**
- An already revoked attestation can be revoked again, causing the `revocationTime` to be updated to a more recent timestamp and emitting a duplicate `ModuleRevoked` event. This leads to incorrect off-chain state tracking for any system that relies on this event to monitor the revocation status and timing of module attestations.

**Recommended Mitigation:** A check should be added to revert if `attestation.revocationTime` is already non-zero, preventing a revocation from being applied to an attestation that has already been revoked.

```diff
    function revoke(address module) external {
        AttestationRecord storage attestation = _attestations[module][msg.sender];
        if (attestation.createdAt == 0) revert AttestationNotFound();
+       if (attestation.revocationTime != 0) revert AttestationAlreadyRevoked();
        attestation.revocationTime = uint48(block.timestamp);
        emit ModuleRevoked(module, msg.sender, uint48(block.timestamp));
    }
```
**Molecule:** Fixed in commit [769ecf1](https://github.com/moleculeprotocol/onchainlabs/commit/769ecf1).

**Cyfrin:** Verified.
