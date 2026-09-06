---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-3-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[I-04] Exchange Rate Feeds'
vuln_class: []
---

# [I-04] Exchange Rate Feeds

_Section severity (from Solodit section header): Informational_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

Question is if these are creating realistic arbitrages and delays between the prices on SCROLL and the Prices on Mainnet
I'd need to normalize them and find the relative deltas to see if that's the case

- The main question here is: Arbitrage
- Value Leak due to not using Market Rate (in case of exploit, in case of big liquidity crunch)
----


**0x57bd9E614f542fB3d6FeF2B744f3B813f0cc1258 - weETH / eETH Exchange Rate**

```js
pricesWithinTimePeriod 200
mean 1047992809278279200
STANDARD DEVIATION 4586508011714059
as percent of mean 0.43764689710730437
getHighestAndLowestPrice 1055895708780116400 1040176765876107400


interval 1 Week

eth_usd_swings.pointsOfBiggestNegativeSwing []
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1723638354, price: 1045578046819054700 },
  { date: 1723119744, price: 1044895476259292500 }
]
deviation 0.06532429082818567


interval One Day

eth_usd_swings.pointsOfBiggestNegativeSwing []
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1730897218, price: 1052073665612945800 },
  { date: 1730810818, price: 1051990739275359400 }
]
deviation 0.0078828011018


interval 4 Hours

eth_usd_swings.pointsOfBiggestNegativeSwing []
eth_usd_swings.pointsOfBiggestPositiveSwing []


interval One Hour

eth_usd_swings.pointsOfBiggestNegativeSwing []
eth_usd_swings.pointsOfBiggestPositiveSwing []
```

0.007882801101796958 - Below dev

So you have to expect each operation to be due to time and not price




**0xE61Da4C909F7d86797a0D06Db63c34f76c9bCBDC - wstETH-ETH Exchange Rate**

```js
pricesWithinTimePeriod 400
mean 1168659431678961200
STANDARD DEVIATION 11860049778819950
as percent of mean 1.014842259201309
getHighestAndLowestPrice 1188596651060688600 1147270030912712700


interval 1 Week

eth_usd_swings.pointsOfBiggestNegativeSwing []
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1723243491, price: 1175451889673963300 },
  { date: 1722724889, price: 1174628840044321500 }
]
deviation 0.07006891041519739


interval One Day

eth_usd_swings.pointsOfBiggestNegativeSwing []
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1733865222, price: 1187362676214505200 },
  { date: 1733778822, price: 1187251706061207600 }
]
deviation 0.009346809335470692


interval 4 Hours

eth_usd_swings.pointsOfBiggestNegativeSwing []
eth_usd_swings.pointsOfBiggestPositiveSwing []


interval One Hour

eth_usd_swings.pointsOfBiggestNegativeSwing []
```

0.0093468093354653 - Below dev
