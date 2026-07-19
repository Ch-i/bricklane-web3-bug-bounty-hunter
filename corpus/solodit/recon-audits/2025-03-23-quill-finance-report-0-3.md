---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-0-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[M-04] `QuillSimplePriceFeed` not having a `fetchRedemptionPrice` can open
  up to Oracle Drift Arbitrage via Redemptions'
vuln_class: []
---

# [M-04] `QuillSimplePriceFeed` not having a `fetchRedemptionPrice` can open up to Oracle Drift Arbitrage via Redemptions

_Section severity (from Solodit section header): Medium_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Impact**

The pricing of a redemption in the `QuillSimplePriceFeed` is as follows:

https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/Quill/PriceFeeds/QuillSimplePriceFeed.sol#L28-L31

```solidity
    function fetchRedemptionPrice() external returns (uint256, bool) {
        // Use same price for redemption as all other ops in WETH branch
        return fetchPrice(); /// @audit this may be underpriced due to Oracle Drift | You must raise the Redemption Fee to cover against it
    }
```

Meaning the price is the same as the one for borrowing

This is generally fine because the MCR for assets is expected to be above `110%` which makes oracle imprecisions somewhat negligible

However, for redemptions the base fee is typically 50 BPS

This seems to not be an issue currently as all Price Feeds I can see on: https://data.chain.link/feeds have a 50 BPS threshold

It's worth noting that the realized Deviation Threshold (the actual price change before the Price Feed finishes it's round) can still be greater than this, leading to some arbitrage in-spite of the settings looking correct

**Mitigation**

Ensure that no oracle or composite usage of oracle prossibly under-prices the asset by more than the Redemption Base Fee

As otherwise the system will naturally open itself up to Arbitrage
