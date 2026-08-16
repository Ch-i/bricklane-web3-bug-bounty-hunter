---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-0-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Incorrect use of `investorExists` modifier in `PublicStockOnRamp::swap`
vuln_class: []
---

# Incorrect use of `investorExists` modifier in `PublicStockOnRamp::swap`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** `PublicStockOnRamp::swap` functions incorrectly validates investor registration. These functions use the `investorExists` modifier which checks if `msg.sender` is a registered wallet, but they also have the `onlyRole(OPERATOR_ROLE)` modifier, meaning `msg.sender` is always the operator, not the actual investor.
The actual investor is passed as the `_investorWallet` , but this address is never validated against the registry:

```solidity
 function swap(
        uint256 _liquidityAmount,
        uint256 _minOutAmount,
        address _investorWallet,
        bytes memory _investorSignature,
        uint8 _marketStatus,
        uint256 _anchorPrice,
        uint256 _anchorPriceExpiresAt
    )
        public
        whenNotPaused
        investorExists <--------
        initializedNavProvider
        validateMinSubscriptionAmount(_liquidityAmount)
        nonZeroAnchorPrice(_anchorPrice)
        onlyRole(OPERATOR_ROLE)
    {...}
```
The `investorExists` modifier checks `_msgSender()` which resolves to `msg.sender`:

```solidity
 modifier investorExists() {
        IDSRegistryService registryService = IDSRegistryService(dsToken.getDSService(dsToken.REGISTRY_SERVICE()));
        if (!registryService.isWallet(_msgSender())) {
            revert InvestorNotRegisteredError();
        }
        _;
    }

```

Since the operator calls the function, the modifier validates whether the operator is registered, not whether `_investorWallet` (the actual investor receiving the tokens) is registered.

**Impact:** * If operators themselves had valid investor wallets, then they could execute swaps for completely unregistered investors, bypassing the entire investor registration system
* If operators don't themselves have valid investor wallets then calls to `PublicStockOnRamp::swap` will revert resulting in denial of service

**Recommended Mitigation:** Replace the `investorExists` modifier with an inline check that validates the `_investorWallet` parameter instead of `msg.sender`:

```solidity
modifier investorWalletExists(address _wallet) {
    IDSRegistryService registryService = IDSRegistryService(
        dsToken.getDSService(dsToken.REGISTRY_SERVICE())
    );
    if (!registryService.isWallet(_wallet)) {
        revert InvestorNotRegisteredError();
    }
    _;
}
```

**Securitize:** Fixed in commit [090cd62](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/090cd62fd656fb0aaf969de1bcc0a84db5523581).

**Cyfrin:** Verified.
