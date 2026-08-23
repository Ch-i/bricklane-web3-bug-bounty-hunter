---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-3-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: Add sanity check to revert if `_treeDepth == 0` in `L1MessageManager::_addL2MerkleRoots`
vuln_class: []
---

# Add sanity check to revert if `_treeDepth == 0` in `L1MessageManager::_addL2MerkleRoots`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** Add sanity check to revert if `_treeDepth == 0` in `L1MessageManager::_addL2MerkleRoots` to prevent adding an L2 Merkle root with `treeDepth == 0` as this would create a state where subsequent calls to `L1MessagingService::claimMessageWithProof` will revert with error `L2MerkleRootDoesNotExist`.

**Linea:**
The depth is always enforced in the circuit and as it forms part of the public input it can never be set to zero - there is a fixed size in the circuit. We have added a comment to note this in commit [54c4670](https://github.com/Consensys/zkevm-monorepo/commit/54c467056b0a95d411f1060f77a9940652b1554c) merged in [PR3214](https://github.com/Consensys/zkevm-monorepo/pull/3214).
