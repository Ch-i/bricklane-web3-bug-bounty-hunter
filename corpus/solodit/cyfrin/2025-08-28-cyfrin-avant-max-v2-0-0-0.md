---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-28-cyfrin-avant-max-v2-0-0-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-08-28T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-28-cyfrin-avant-max-v2-0
title: '`PriceStorage::setPrice` maximum lower and upper bounds can be easily bypassed
  by repeatedly calling the function in the same block'
vuln_class: []
---

# `PriceStorage::setPrice` maximum lower and upper bounds can be easily bypassed by repeatedly calling the function in the same block

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-28-cyfrin-avant-max-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md)_

---

**Description:** `PriceStorage::setPrice` limits the price movement to a maximum lower/upper range delta based on the current price, to prevent sudden extreme changes in price:
```solidity
uint256 lastPriceValue = lastPrice.price;
if (lastPriceValue != 0) {
  uint256 upperBound = lastPriceValue + ((lastPriceValue * upperBoundPercentage) / BOUND_PERCENTAGE_DENOMINATOR);
  uint256 lowerBound = lastPriceValue - ((lastPriceValue * lowerBoundPercentage) / BOUND_PERCENTAGE_DENOMINATOR);
  if (_price > upperBound || _price < lowerBound) {
    revert InvalidPriceRange(_price, lowerBound, upperBound);
  }
}
```

But this can be easily bypassed by repeatedly calling the `setPrice` function multiple times in the same block, each time decreasing or increasing the `lastPrice` by the current maximum allowed lower/upper bound.

**Impact:** The limitation of wild price fluctuations can be trivially bypassed so is ineffective, though only by entities having `SERVICE_ROLE`.

**Recommended Mitigation:** Add a configurable parameter `minPriceUpdateDelay` to the`PriceStorage` contract which only `DEFAULT_ADMIN_ROLE` can change. Then in `setPrice`:
```solidity
error PriceUpdateTooSoon(uint256 lastUpdate, uint256 minWaitTime);

// In setPrice:
if(lastPrice.timestamp != 0) {
    if(block.timestamp < lastPrice.timestamp + minPriceUpdateDelay) {
        revert PriceUpdateTooSoon(lastPrice.timestamp, minPriceUpdateDelay);
    }
}
```

**Avant:**
Acknowledged: the suggestion is valid, and we might consider the change in the future if we automate price setting. Currently, the price is calculated manually after a careful NAV process conducted weekly and will most likely be outsourced to an independent party for increased transparency. Once calculated, the price update transaction is also posted manually and requires a quorum of approvals before being submitted on-chain. This setup ensures that no repeated calls or incorrect parameters are ever attempted, and for now, the current code constraints suit our requirements.
