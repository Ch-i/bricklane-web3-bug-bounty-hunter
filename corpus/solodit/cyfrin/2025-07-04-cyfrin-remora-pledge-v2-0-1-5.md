---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-1-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: '`DocumentManager::hasSignedDocs` incorrectly returns `true` when there are
  no documents to sign'
vuln_class: []
---

# `DocumentManager::hasSignedDocs` incorrectly returns `true` when there are no documents to sign

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `DocumentManager::hasSignedDocs` incorrectly returns `true` when there are no documents to sign:
```solidity
function hasSignedDocs(address signer) public view returns (bool, bytes32) {
    DocumentStorage storage $ = _getDocumentStorage();
    uint256 numDocs = $._docHashes.length;

    // @audit when numDocs = 0, the `for` loop is bypassed
    // skipping to the `return (true, 0x0);` statement
    for (uint256 i = 0; i < numDocs; ++i) {
        bytes32 docHash = $._docHashes[i];
        if (
            $._documents[docHash].needSignature &&
            $._signatureRecords[signer][docHash] == 0
        ) return (false, docHash);
    }

    return (true, 0x0);
}
```

**Impact:** Upstream contracts incorrectly assume users have signed docs and allow user actions which should be prohibited.

**Proof Of Concept:**
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
    function test_hasSignedDocs_TrueWhenNoDocs() external {
        // verify no docs
        assertEq(_getDocumentStorage()._docHashes.length, 0);

        // hasSignedDocs returns true even though no docs to sign
        (bool hasSigned, ) = hasSignedDocs(address(0x1337));
        assertTrue(hasSigned);
    }
}
```

**Recommended Mitigation:** When no docs exist, it is impossible for users to have signed them. Hence in this case `DocumentManager::hasSignedDocs` should either revert with a specific error such as `EmptyDocument` or `return (false, 0x0)`.

**Remora:** Fixed in commit [7454e55](https://github.com/remora-projects/remora-smart-contracts/commit/7454e55e4017aab9d286637fbe5ccf3c705324ba).

**Cyfrin:** Verified.
