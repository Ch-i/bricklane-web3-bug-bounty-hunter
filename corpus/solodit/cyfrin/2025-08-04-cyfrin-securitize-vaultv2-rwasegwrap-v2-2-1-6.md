---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-1-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-08-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md
tags:
- firm:cyfrin
- report:2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2
title: Missing `notEmptyURI` modifier during initialization
vuln_class: []
---

# Missing `notEmptyURI` modifier during initialization

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md)_

---

**Description:** Currently, there is no `notEmptyURI` modifier present in the `initialize()` function that checks for the empty URI and, if it's empty, reverts the transaction:

```
//RWASegWrap.sol#L98-103
    modifier notEmptyUri(string memory newUri) {
        if (bytes(newUri).length == 0) {
            revert EmptyUriInvalid();
        }
        _;
    }
```

```
//RWASegWrap.sol#L131-147
   function initialize(
        string memory baseNameArg,
        string memory baseSymbolArg,
        string memory uriArg,
        address liquidationAssetArg,
        address assetArg,
        address vaultDeployerArg
    )
    public
    virtual
    override
    onlyProxy
    initializer
    addressNotZero(liquidationAssetArg)
    addressNotZero(assetArg)
    addressNotZero(vaultDeployerArg)
    {

```


**Impact:** Insufficient validation, `projectURI` may not be set during the initialization process.

**Recommended Mitigation:** Add the `notEmptyUri` modifier that checks for the empty URI.

**Securitize**
Fixed in commit [0946fb](https://github.com/securitize-io/bc-securitize-vault-sc/commit/0946fbac2f4dd161c31c2cc8125c1203d6b46590).

**Cyfrin:** Verified.

\clearpage
