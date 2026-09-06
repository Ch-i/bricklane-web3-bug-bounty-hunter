---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-06-01-protectorate-3-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-06-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-Protectorate.md
tags:
- firm:pashov-audit-group
- report:2023-06-01-protectorate
title: '[L-02] Division before multiplication can lead to rounding errors'
vuln_class: []
---

# [L-02] Division before multiplication can lead to rounding errors

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-06-01-Protectorate.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-Protectorate.md)_

---

In `DutchAuction::priceFunction` there is division before multiplication here:

```solidity
uint256 priceDeclinePerSecond =
            (auctionDetails.startPrice - auctionDetails.minimumPrice) / auctionDuration;

return auctionDetails.startPrice - (timeSinceAuctionStart *
priceDeclinePerSecond);
```

This can lead to rounding errors but without a serious impact to the application. Still you should always do multiplication before division in Solidity.
