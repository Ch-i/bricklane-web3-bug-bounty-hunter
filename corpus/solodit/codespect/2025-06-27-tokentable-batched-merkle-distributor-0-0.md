---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-06-27-tokentable-batched-merkle-distributor-0-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-06-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-27-TokenTable-Batched-Merkle-Distributor.md
tags:
- firm:codespect
- report:2025-06-27-tokentable-batched-merkle-distributor
title: '[I-01] Missing token index bounds validation leads to array out-of-bounds
  revert in batch claims'
vuln_class: []
---

# [I-01] Missing token index bounds validation leads to array out-of-bounds revert in batch claims

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-06-27-TokenTable-Batched-Merkle-Distributor.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-27-TokenTable-Batched-Merkle-Distributor.md)_

---

**Files:** [TokenTableMerkleMultitokenDistributorBatched.sol](https://github.com/EthSign/tokentable-evm/tree/442aca0222550cf985e2b94c07ba0255bf972471/src/merkle/core/extensions/TokenTableMerkleMultitokenDistributorBatched.sol)

**Description:**

The `_sendByIndex(...)` function accesses the `tokens` array using a user-provided `tokenIndex` without validating that the index is within the array bounds:

```solidity
function _sendByIndex(address recipient, uint256 tokenIndex, uint256 amount) internal {
    address token = tokens[tokenIndex]; // No bounds checking
    // ...
}
```

While the `packRecipientTimeToken(...)` function validates that `tokenIndex < 2^56` to prevent bit-packing overflow, it doesn’t validate against the actual `tokens.length`. This creates a gap where values like `tokenIndex = 999` pass the bit-packing validation but cause array out-of-bounds reverts when accessing `tokens[999]` in an array that typically will not contain many elements.

**Impact:** Batch claims containing invalid token indices will revert with unnecessary array out-of-bounds errors.

**Recommendation(s):** Add explicit bounds validation in the `packRecipientTimeToken(...)` which will be used for crafting the batches.

**Status:** Acknowledged

**Update from TokenTable:** Acknowledged
