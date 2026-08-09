---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-2-8
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Refactor identical code from `SecuritizeAmmNavProvider::_pricingFromCurveBuy,
  _pricingFromCurveSell` into internal function
vuln_class: []
---

# Refactor identical code from `SecuritizeAmmNavProvider::_pricingFromCurveBuy, _pricingFromCurveSell` into internal function

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** `SecuritizeAmmNavProvider::_pricingFromCurveBuy, _pricingFromCurveSell` are virtually identical except for the very last line; refactor the identical code into an internal function to avoid unnecessary code duplication:
```solidity
function _computeExecPrice(
    uint256 curvePriceWad,
    uint256 anchorPriceWad
) internal view returns (uint256 execPriceWad) {
    require(anchorPriceWad > 0, "anchor=0");
    require(priceScaleFactor > 0, "scaleFactor = 0");

    uint256 mWad = (curvePriceWad * baseBaseline) / quoteBaseline;
    uint256 baseExecPriceWad = (anchorPriceWad * mWad) / WAD;

    if (baseExecPriceWad >= anchorPriceWad) {
        uint256 diff = baseExecPriceWad - anchorPriceWad;
        execPriceWad = anchorPriceWad + (diff / priceScaleFactor);
    } else {
        uint256 diff = anchorPriceWad - baseExecPriceWad;
        execPriceWad = anchorPriceWad - (diff / priceScaleFactor);
    }
}

function _pricingFromCurveBuy(...) internal view returns (uint256 baseOut, uint256 execPriceWad) {
    execPriceWad = _computeExecPrice(curvePriceWad, anchorPriceWad);
    baseOut = (amountInQuote * WAD) / execPriceWad;
}

function _pricingFromCurveSell(...) internal view returns (uint256 quoteOut, uint256 execPriceWad) {
    execPriceWad = _computeExecPrice(curvePriceWad, anchorPriceWad);
    quoteOut = (amountInBase * execPriceWad) / WAD;
}
```

**Securitize:** Acknowledged.
