---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-2-11
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[M-12] Pull Based Oracle may allow for profitable self-liquidations'
vuln_class: []
---

# [M-12] Pull Based Oracle may allow for profitable self-liquidations

_Section severity (from Solodit section header): Medium_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Executive Summary**

Pull based oracle allow using more than one price within the last 5 minutes, this opens up to a myriad of combinations that may allow for self-liquidations

**Description**

The likelihood that a price moves by 10% is fairly low

However, when you start adding more collaterals and debt types, the likelihood that the combination of any two Collateral and Debt asset to have high volatility between each other raises

Meaning that when considering risk parameters, you shouldn't simply look at a debt or collateral price against USD, but also the ratio and correlation between those assets, as the correlation may open up to higher swings that may cause the protocol to lock-in bad debt


**Proof Of Concept**

A sample scenario would look as follows:
- Find coll and asset that have 11% difference in price from current price to new price
- Open up a trove
- Borrow as much as possible
- Deposit into the stability pool
- Update the prices
- Get liquidated, with bad debt

The likelihood of the profitability is reduced the more deposits are done in the stability pool and the higher opening fees are

**Mitigation**

Unfortunately this is a statistical risk, and to mitigate it you'd need to:
- Research all historical Pyth Prices
- Check for realized volatility of assets
- Add a buffer to account for errors or additional realized volatility
- Move the MICR to a value that is consistent with this risk
