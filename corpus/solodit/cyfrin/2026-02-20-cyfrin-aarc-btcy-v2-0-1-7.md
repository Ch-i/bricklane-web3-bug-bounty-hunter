---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-1-7
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: '`IBTCYHub` batch processing uses historical Chainlink rounds'
vuln_class: []
---

# `IBTCYHub` batch processing uses historical Chainlink rounds

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** `IBTCYHub::processSubscriptions`/`processRedemptions` accept `priceIds` and fetch pricing via `pricer.getPriceInfos(priceIds)`, which calls `priceFeed.getRoundData(roundId)` for each provided id. This uses historical Chainlink rounds rather than the latest available round at processing time.

**Impact:** Batches may be processed using prices that are older than necessary.

**Recommended Mitigation:** Consider using `latestRoundData` and skip (`priceIds`/`roundIds`).


**Aarc:** Acknowledged. Design choice.
