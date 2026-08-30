---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-06-02T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-02-cyfrin-evo-soulboundtoken-v2-0
title: Use named returns where this can eliminate local function variables and for
  `memory` returns
vuln_class: []
---

# Use named returns where this can eliminate local function variables and for `memory` returns

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md)_

---

**Description:** Using named returns is more gas efficient where this can eliminate local function variables and for `memory` returns:
```diff
-   function batchMintAsAdmin(address[] calldata accounts) external onlyAdmin returns (uint256[] memory) {
+   function batchMintAsAdmin(address[] calldata accounts) external onlyAdmin returns (uint256[] memory tokenIds) {
        _revertIfEmptyArray(accounts);
        uint256 startId = _incrementTokenIdCounter(accounts.length);

-      uint256[] memory tokenIds = new uint256[](accounts.length);
+      tokenIds = new uint256[](accounts.length);
        for (uint256 i = 0; i < accounts.length; ++i) {
            _mintAsAdminChecks(accounts[i]);
            tokenIds[i] = startId + i;
            _safeMint(accounts[i], tokenIds[i]);
        }
-      return tokenIds;
    }
```

Gas Result:
```diff
{
-  "batchMintAsAdmin": "252114"
+  "batchMintAsAdmin": "252102"
}
```

**Evo:**
Fixed in commit [b4fcadb](https://github.com/contractlevel/sbt/commit/b4fcadbd9c5684cc4e3b1ee3c39f72c406aaf658).

**Cyfrin:** Verified.
