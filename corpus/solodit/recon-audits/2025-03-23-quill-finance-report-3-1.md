---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-3-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[I-02] Suggested Changes - Change stETH to 110 MCR'
vuln_class: []
---

# [I-02] Suggested Changes - Change stETH to 110 MCR

_Section severity (from Solodit section header): Informational_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Disclosures**

I do not hold any LIDO, I do hold LQTY, stETH and wstETH

**Executive Summary**

stETH doesn't need to have a 120 MCR, I recommend 110, 112 if you want to maintain a relative risk profile against ETH

As it stands even the MCR for ETH is very conservative, so 110 for stETH seems fine as well

120 MCR implies that stETH is MASSIVELY riskier than ETH

While it's factually true that stETH is riskier, Quill has access to 2 tools

1) Debt Limits, which limit the maximum exposure and risk to bad debt
2) Upgradeability, and shutdown

Due to this, Quill could change the risk parameters at a later time

**stETH Tail Event**

stETH presents 3 key risks that must be addressed in a thorough risk analysis

1) Slashing
2) Upgrade Risk and Perceived Governance risk
3) Exit Queue Liquidity Risk


**Slashing**

Slashing is arguably a real risk, but in analyzing slashing, we have to account for the relative amount lost vs the total amount staked and yielding

Slashing risk is a real risk, but in most cases the impact is negligible, definitely not "volatility generating"

The real risk around slashing is if something massive happen, such as the "GETH BUG" causing a massive amount of stake to be lost

This is a real risk, however this would cause similar issues to ETH itself, meaning this black swan can kill Quill in both cases

And I'm not convinced it can be mitigated

**Upgrade Risk and Perceived Governance Risk**

Upgrade risk is a real risk, which can put 100% of funds at risk

Upgrades from lido are behind a timelock

The governance could have failed many times already

Meaning that a future upgrade could change the risk profile of stETH

But as of today this upgrade risk is minimized

In the event of an upgrade, which would be behind a timelock, the branch could be shutdown to cause a 1% haircut to all borrowers

Which is a lot lower than any real risk

The perceived risks of a governance takeover, upgrade, or general fear are instead worth entertaining

These would cause stETH to depreciate, the question is by how much

As long as these changes don't cause stETH to lose 10% of it's value in a matter of minutes, then the system could handle them

**Exit Queue Risk - 1 / 1 stETH Pricing**

Illiquidity can be a huge issue, and liquidation cascades are very common during the Bull Market

Many risk advisors have suggested hardcoding the price of stETH to 1, this can be fine for short burst

From working with Liquity we've discussed this as a tail risk mostly around redemptions, more so than around liquidations

That's because Liquity has a fairly high MCR (110%) for ETH, meaning Collateral has to massively depreciate before it would cause bad debt to be locked in by the system

On the long term, 1/1 par pricing is ignoring the necessary discount that comes from stETH having a redemption queue

In most times, the withdrawal queue takes 7 days, this is a real cause for discount, but fairly limited

If we naively take 15% (currently the degen rate of lending), we can infer the following:

15/365*7 = 0.287671232877

stETH should naturally trade below parity by about 30 BPS

However it doesn't because of liquity and incentives that make it so that there's a fairly deep buffer to conver from stETH back to ETH

As long as that buffer is there, and that buffer is mostly available to Quill, then stETH should be priced at parity with ETH

**Validator Queue Exit Math**

Assuming 100% of stake wanted to exit, with 1 MLN Validators it would take around 277 days (linear interpolation, which is inexact)

If we apply the same idea around delay = discount, this should cause a 15% to 20% discount on stETH

This could lead to wanting a 120 MCR, however this is the absolute worst case which could happen as a black swan, but shouldn't happen for a prolonged amount of time

In am more realistic scenario we'd expect the discount to vary as more people want to exit, which means that stETH shouldn't reprice by more than 10% within an hour

**stETH day to day pricing**

On the day to day, stETH should be priced based on it's liquidity and based on the amount that may need to be liquidated on a % swing

These are the same principles for ETH

**Borrow Caps**

By capping the total amount of borrows against stETH to the amount that is liquidatable you are limiting the maximum exposure of the protocol by a lot

**Methodology**

- Track all borrows on your chain (including other protocols)
- Track the % of stETH that would need to be liquidated if X% price change would happen (generally 5% to 20%)
- Talk to liquidators and investors to have an additional liquidity pool
- Cap the borrow caps at the $ equivalent of this
- Monitor and change this amount based on what happens


**Price Analysis**

Below I provided all data and analyses of it

Even if you check all prices from back in 2021, the maximum swing that happened in an hour is contained at about 2%

The maximum swing in a day is less than 5%

Meaning that stETH has had volatility, but this is fairly limited against ETH

If we look at the last year, which has had incredible volatility for ETH

The relative price changes for stETH have been very contained, between 1.4 and 2% in an hour

These can lead to a best case of setting the MCR to 110 (same as ETH as roughly the same risk parameters, given a borrow cap of available liquidity)

And a more conservative MCR of 112 (the extra 2%), which should hold under most circumnstances, barring extreme volatility due to a perceived governance risk. For those scenarios you may want to shutdown the branch temporarily if necessary

**All Data Info**

Data was scraped from CL, with a Recon Pro tool

All data is public 

NOTE: Not all prices scraped where the exact prices from the aggregator, this is due to the methodology

**All Prices**

```ts
pricesWithinTimePeriod 1265
mean 994826037804453500
STANDARD DEVIATION 9789739730572964
as percent of mean 0.9840654907041415
getHighestAndLowestPrice 1011099584285630300 935019330000000000


interval 604800

eth_usd_swings.pointsOfBiggestNegativeSwing [
  { date: 1652457558, price: 956120080000000000 },
  { date: 1651872078, price: 998995978974146300 }
]
deviation 4.291899054305995
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1652895059, price: 984201283138867600 },
  { date: 1652457558, price: 956120080000000000 }
]
deviation 2.936995438780826


interval 86400

eth_usd_swings.pointsOfBiggestNegativeSwing [
  { date: 1655197624, price: 941991810710835000 },
  { date: 1655154105, price: 962272040061608300 }
]
deviation 2.1075359676329115
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1655154105, price: 962272040061608300 },
  { date: 1655109764, price: 940974924073828400 }
]
deviation 2.2633032446366244


interval 14400

eth_usd_swings.pointsOfBiggestNegativeSwing [
  { date: 1733800235, price: 987343063643981400 },
  { date: 1733791463, price: 1005061173410059600 }
]
deviation 1.762888691238828
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1652462990, price: 976665000054923600 },
  { date: 1652457558, price: 956120080000000000 }
]
deviation 2.1487803137576242


interval 3600

eth_usd_swings.pointsOfBiggestNegativeSwing [
  { date: 1725412283, price: 982523475032176500 },
  { date: 1725412223, price: 996572661455605200 }
]
deviation 1.4097503340005673
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1725414119, price: 1000884598543477800 },
  { date: 1725412283, price: 982523475032176500 }
]
deviation 1.8687719914987213
```

**Last Year**

Price changes
```ts
pricesWithinTimePeriod 422
mean 998928145333159300
STANDARD DEVIATION 2765111607703231.5
as percent of mean 0.2768078585653446
getHighestAndLowestPrice 1011099584285630300 982523475032176500


interval 604800

eth_usd_swings.pointsOfBiggestNegativeSwing [
  { date: 1733800235, price: 987343063643981400 },
  { date: 1733791463, price: 1005061173410059600 }
]
deviation 1.762888691238828
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1723157987, price: 1011099584285630300 },
  { date: 1722824399, price: 984642681457643900 }
]
deviation 2.6869547020671702


interval 86400

eth_usd_swings.pointsOfBiggestNegativeSwing [
  { date: 1733800235, price: 987343063643981400 },
  { date: 1733791463, price: 1005061173410059600 }
]
deviation 1.762888691238828
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1725414119, price: 1000884598543477800 },
  { date: 1725412283, price: 982523475032176500 }
]
deviation 1.8687719914987213


interval 14400

eth_usd_swings.pointsOfBiggestNegativeSwing [
  { date: 1733800235, price: 987343063643981400 },
  { date: 1733791463, price: 1005061173410059600 }
]
deviation 1.762888691238828
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1725414119, price: 1000884598543477800 },
  { date: 1725412283, price: 982523475032176500 }
]
deviation 1.8687719914987213


interval 3600

eth_usd_swings.pointsOfBiggestNegativeSwing [
  { date: 1725412283, price: 982523475032176500 },
  { date: 1725412223, price: 996572661455605200 }
]
deviation 1.4097503340005673
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1725414119, price: 1000884598543477800 },
  { date: 1725412283, price: 982523475032176500 }
]
deviation 1.8687719914987213
```
