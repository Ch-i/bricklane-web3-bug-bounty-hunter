---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-2-11
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Impossible to remove a document added with zero uri length
vuln_class: []
---

# Impossible to remove a document added with zero uri length

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Impossible to remove a document added with zero uri length.

**Proof of Concept:** After fixing the bug "Don't add duplicate documentHash to DocumentManager::DocumentStorage::_docHashes when overwriting via _setDocument as this causes panic revert when calling _removeDocument", run this fuzz test:
```solidity
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
        // verify overwriting doesn't duplicate the hash in `_docHashes`
        assertEq($._docHashes.length, 1);
        assertEq($._docHashes[0], docHash);

        // now attempt to remove it
        _removeDocument(docHash);
    }
```

It reverts with `[FAIL: EmptyDocument();` when calling `_removeDocument` at the end.

**Recommended Mitigation:** Don't allowing adding documents with empty uri.

**Remora:** Fixed in commit [1218d18](https://github.com/remora-projects/remora-smart-contracts/commit/1218d1818e1748cd7d9b71e84485f8059d135ab5).

**Cyfrin:** Verified.
