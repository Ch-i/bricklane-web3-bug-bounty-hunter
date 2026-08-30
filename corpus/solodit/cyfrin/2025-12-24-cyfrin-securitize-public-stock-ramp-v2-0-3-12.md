---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-3-12
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Refactor away unnecessary local variables in `SecuritizeAmmNavProvider::_curveBuy,
  _curveSell`
vuln_class: []
---

# Refactor away unnecessary local variables in `SecuritizeAmmNavProvider::_curveBuy, _curveSell`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** In `SecuritizeAmmNavProvider::_curveBuy, _curveSell` the local variables `X, Y, kLocal` are only read once so there is no need to use them to cache storage, just read the storage slots directly when required:
```solidity
function _curveBuy(uint256 amountInQuote) internal view initialized returns (uint256 curvePriceWad, uint256 newBase, uint256 newQuote) {
    require(amountInQuote > 0, "amountInQuote=0");

    newQuote = quoteReserves + amountInQuote;
    newBase = k / newQuote;

    uint256 deltaBase = baseReserves - newBase;
    require(deltaBase > 0, "deltaBase=0");

    curvePriceWad = (amountInQuote * WAD) / deltaBase;
}

function _curveSell(uint256 amountInBase) internal view initialized returns (uint256 curvePriceWad, uint256 newBase, uint256 newQuote) {
    require(amountInBase > 0, "amountInBase=0");

    newBase = baseReserves + amountInBase;
    newQuote = k / newBase;

    uint256 deltaQuote = quoteReserves - newQuote;
    require(deltaQuote > 0, "deltaQuote=0");

    curvePriceWad = (deltaQuote * WAD) / amountInBase;
}
```

**Securitize:** Fixed in commit [5ca8229](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/5ca82293e642b42741dcded549d89e2f74a0f757).

**Cyfrin:** Verified.

\clearpage
