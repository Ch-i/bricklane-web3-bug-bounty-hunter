---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-2-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-08-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md
tags:
- firm:cyfrin
- report:2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2
title: '`setApprovalForAll()` function is double initialized in the child contract'
vuln_class: []
---

# `setApprovalForAll()` function is double initialized in the child contract

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md)_

---

**Description:** At the moment, there is a double function initialization of the ERC1155 `setApprovalForAll()` function both in the parent `RWASegWrap` and the child `SecuritizeRWASegWrap` contracts:

```
    // @inheritdoc IERC1155
    function setApprovalForAll(address, bool) public virtual pure override {
        revert FeatureNotSupported();
    }

```


```
    // @inheritdoc IERC1155
    function setApprovalForAll(address, bool) public virtual pure override {
        revert FeatureNotSupported();
    }
```

**Impact:** Increased deployment costs.

**Recommended Mitigation:** Remove `setApprovalForAll()` implementation from the  `SecuritizeRWASegWrap`.

**Securitize**
Fixed in commit [b78f30](https://github.com/securitize-io/bc-rwa-seg-wrap-sc/commit/b78f305a0dcc6a1e7eb425d05bae150f23d2d184).

**Cyfrin:** Verified.
