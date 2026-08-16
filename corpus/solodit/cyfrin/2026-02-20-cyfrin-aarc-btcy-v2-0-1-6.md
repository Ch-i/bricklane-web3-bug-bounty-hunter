---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-1-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: '`Pricer::updatePrice` allows infinite price changes in the same block'
vuln_class: []
---

# `Pricer::updatePrice` allows infinite price changes in the same block

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** `Pricer::updatePrice` does not contain any rate-limiting check such as `addPrice, addCurrentPrice` which use `MIN_PRICE_UPDATE_INTERVAL`.

It does have a call to `_requireWithinDeviation` but this compares the new price agains the current price for the same `priceId`, and hence this is meaningless since `PRICE_UPDATE_ROLE` can just call `updatePrice` in the same block over and over again, increasing or decreasing the price by the max deviation amount each time.

**Recommended Mitigation:** Implement a time-based rate-limiting restriction in `Pricer::updatePrice` such that `PRICE_UPDATE_ROLE` can't call it for the same `priceId` multiple times in the same block.

**Aarc:** Fixed in commit [c905cbf](https://github.com/aarc-xyz/btcy-contracts-main/pull/11/changes/c905cbffc593bff5788403eb019ca26681545e31).

**Cyfrin:** Verified.
