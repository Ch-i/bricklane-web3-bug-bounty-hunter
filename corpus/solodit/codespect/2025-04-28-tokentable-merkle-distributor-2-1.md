---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-28-tokentable-merkle-distributor-2-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-28-TokenTable-Merkle-Distributor.md
tags:
- firm:codespect
- report:2025-04-28-tokentable-merkle-distributor
title: '[I-02] getClaimDelegate Function Not Blocked When Delegated Claiming is Disabled'
vuln_class: []
---

# [I-02] getClaimDelegate Function Not Blocked When Delegated Claiming is Disabled

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-28-TokenTable-Merkle-Distributor.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-28-TokenTable-Merkle-Distributor.md)_

---

**Files:** [NFTGatedMerkleDistributor.sol](https://github.com/EthSign/merkle-token-distributor/tree/96fedd0d945693149e0903c84502004bf819996c/src/core/extensions/custom/NFTGatedMerkleDistributor.sol#L32)

**Description:**

The `NFTGatedMerkleDistributor` contract has delegated claims disabled. The following functions:

- `setClaimDelegate();`
- `batchDelegateClaim();`
- `delegateClaim();`

are blocked using revert. However the `getClaimDelegate()` is not.

**Impact:** No impact to the protocol functionality, only inconsistent implementation.

**Status:** Acknowledged

**Update from TokenTable:** Acknowledged.
