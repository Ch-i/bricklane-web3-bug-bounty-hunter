---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-2-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Gracefully handle state where perp market `maxOpenInterest` is updated to be
  smaller than the current open interest
vuln_class: []
---

# Gracefully handle state where perp market `maxOpenInterest` is updated to be smaller than the current open interest

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** `GlobalConfigurationBranch::updatePerpMarketConfiguration` only enforces that `maxOpenInterest != 0` then calls `MarketConfiguration::update` which sets `maxOpenInterest` to an arbitrary non-zero value.

This means that protocol admins can update `maxOpenInterest` to be smaller than the current open interest. This state in turn causes many transactions for that market including liquidations to fail because of the check in `PerpMarket::checkOpenInterestLimits`.

**Recommended Mitigation:** The first option is to prevent `maxOpenInterest` from being updated to be smaller than the current open interest. However there may be a valid reason to do this for example if the protocol admins want to reduce the size of a current market to limit exposure.

So another option is to modify the check in `PerpMarket::checkOpenInterestLimits` to be similar to the `skew` check; the transaction would be allowed if it is reducing the current open interest, even if the reduced value is still greater than the currently configured `maxOpenInterest`.

**Zaros:** Fixed in commit [8a3436c](https://github.com/zaros-labs/zaros-core/commit/8a3436ca522587b9ae631a65ae7f8343ce536e71).

**Cyfrin:** Verified.
