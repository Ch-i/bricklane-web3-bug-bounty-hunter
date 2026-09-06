---
affected_contracts: []
derives_from: []
id: solodit-hexens-2023-02-27-polygonzkevm-3-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-02-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md
tags:
- firm:hexens
- report:2023-02-27-polygonzkevm
title: 11. INCORRECT INDEX SIZE IN VERIFYMERKLEPROOF
vuln_class: []
---

# 11. INCORRECT INDEX SIZE IN VERIFYMERKLEPROOF

_Section severity (from Solodit section header): Informational_  
_Audit firm: Hexens_  
_Source report: [2023-02-27-PolygonZkEvm.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md)_

---

**Severity:** Informational

**Path:** DepositContract.sol:L90-L112

**Description:**  

In the contract DepositContract.sol
The index is of size uint64, and as the merkle tree levels are 32, the most significant bits of the index can be manipulated to double spend with the same index.

As the functions calling this context are using correct size of index (uint32) this issue is with lowered severity, although potentially this can bring to critical impact attack vectors if the code will be refactored and mislead by the parameter’s uint64 size.

```
function verifyMerkleProof(
       bytes32 leafHash,
       bytes32[] memory smtProof,
       uint64 index,
       bytes32 root
   ) public pure returns (bool) {
       bytes32 node = leafHash;

       // Check merkle proof
       uint256 currrentIndex = index; 
       for (
           uint256 height = 0;
           height < _DEPOSIT_CONTRACT_TREE_DEPTH;
           height++
       ) {
           if ((currrentIndex & 1) == 1)
               node = keccak256(abi.encodePacked(smtProof[height], node));
           else node = keccak256(abi.encodePacked(node, smtProof[height]));
           currrentIndex /= 2;
       }

       return node == root;
   }

```

**Remediation:** The index should be checked to be lower than 2**_DEPOSIT_CONTRACT_TREE_DEPTH (since the leaf traversing will be done for _DEPOSIT_CONTRACT_TREE_DEPTH levels).

**Status:** Fixed

- - -
