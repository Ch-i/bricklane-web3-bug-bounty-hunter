---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-1-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Don't add duplicate `documentHash` to `DocumentManager::DocumentStorage::_docHashes`
  when overwriting via `_setDocument` as this causes panic revert when calling `_removeDocument`
vuln_class: []
---

# Don't add duplicate `documentHash` to `DocumentManager::DocumentStorage::_docHashes` when overwriting via `_setDocument` as this causes panic revert when calling `_removeDocument`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `DocumentManager::_setDocument` intentionally allows overwriting but when overwriting it adds an additional duplicate `documentHash` to `_docHashes`:
```solidity
function _setDocument(
    bytes32 documentName,
    string calldata uri,
    bytes32 documentHash,
    bool needSignature
) internal {
    DocumentStorage storage $ = _getDocumentStorage();
    $._documents[documentHash] = DocData({
        needSignature: needSignature,
        docURI: uri,
        docName: documentName,
        timestamp: SafeCast.toUint32(block.timestamp)
    });

    // @audit duplicate if overwriting
    $._docHashes.push(documentHash);
    emit DocumentUpdated(documentName, uri, documentHash);
}
```

**Impact:** Once the hash has been duplicated in `_docHashes`, it is impossible to remove the document by calling `_removeDocument` as it panic reverts.

**Proof of Concept:**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {DocumentManager} from "../../../contracts/RWAToken/DocumentManager.sol";

import {UnitTestBase} from "../UnitTestBase.sol";

contract DocumentManagerTest is UnitTestBase, DocumentManager {
    function setUp() public override {
        UnitTestBase.setUp();
        initialize();
    }

    function initialize() public initializer {
        __RemoraDocuments_init("NAME", "VERSION");
    }

    // this is incorrect and should be changed once bug is fixed
    function test_setDocumentOverwrite(string calldata uri) external {
        bytes32 docName = "0x01234";
        bytes32 docHash = "0x5555";
        bool needSignature = true;

        // add the document
        _setDocument(docName, uri, docHash, needSignature);

        // verify its hash has been added to `_docHashes`
        DocumentStorage storage $ = _getDocumentStorage();
        assertEq($._docHashes.length, 1);
        assertEq($._docHashes[0], docHash);

        // ovewrite it
        _setDocument(docName, uri, docHash, needSignature);
        // this duplicates the hash in `_docHashes`
        assertEq($._docHashes.length, 2);
        assertEq($._docHashes[0], docHash);
        assertEq($._docHashes[1], docHash);

        // now attempt to remove it, reverts with
        // panic: array out-of-bounds access
        _removeDocument(docHash);
    }
}
```

**Recommended Mitigation:** In `DocumentManager::_setDocument` check if the `documentHash` already exists and if so, don't add it to `_docHashes`.

Alternatively use [`EnumerableSet`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/structs/EnumerableSet.sol) for `DocumentManager::DocumentStorage::_docHashes` which doesn't allow duplicates.

In `_removeDocument` break out of the loop once the element has been deleted:
```diff
        uint256 dHLen = $._docHashes.length;
        for (uint i = 0; i < dHLen; ++i) {
            if ($._docHashes[i] == documentHash) {
                $._docHashes[i] = $._docHashes[dHLen - 1];
                $._docHashes.pop();
+               break;
            }
        }
```

**Remora:** Fixed in commit [1218d18](https://github.com/remora-projects/remora-smart-contracts/commit/1218d1818e1748cd7d9b71e84485f8059d135ab5).

**Cyfrin:** Verified.
