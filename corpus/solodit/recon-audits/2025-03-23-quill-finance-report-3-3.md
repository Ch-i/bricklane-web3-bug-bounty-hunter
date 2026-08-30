---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-3-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[I-04] Economic Analysis off of CL Price Feeds'
vuln_class: []
---

# [I-04] Economic Analysis off of CL Price Feeds

_Section severity (from Solodit section header): Informational_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Methodology**

I fetch all prices from CL

I run a script to find the biggest deltas given a period of 1 week or 1 day

I use these periods to identify high volatility periods

I determine the % change as follows:

```js
- pointsOfBiggestNegativeSwing

(Highest - Lowest) / Highest * 100
= -%

- pointsOfBiggestPositiveSwing

(Highest - Lowest) / Lowest * 100
= +%
```

Because of the uniqueness of the chain I then looked at the liquidity sources for various assets

Overall the key issue for scroll is the lack of liquidity

This makes most assets extremely risk to Quill

Here are some rational limitations given the current state of scroll:

- 25k SCR 

SCR is illiquid and even this amount could cause bad debt to the protocol, more so than liquidation risk and premium caps are necessary
Generally speaking a 150% CR seems fine, but the reality is that SCR is subject to "exit scam" risk, a single seller will always be able to cause bad debt to your project, so I believe the issue cannot be solved via CR, but rather by limiting it or ideally removing it until it's better distributed.

- 300 wstETH

Value above this will incurr too much slippage, until you've gone through some liquidations, I believe that this should be the max cap for wstETH, this can be raised if you find someone that is willing to take the delay risk tied with bridging out wstETH back onto mainnet


- 65 weETH 

After this value slippage becomes too big of a factor

- 400 WETH (Limited by Liquidity)

Similarly, however based on the amount of QUILL and based on growth, I'd expect WETH to be the token that could most likely grow


**Initial Takeaways**

It seems clear that Scroll is behaving as ETH Beta

When reviewing the prices and looking at them something felt off

I'm not realizing that Scroll has only 14% Circulating Supply

I believe the economic analysis then needs to be conducted with the main modelling assuming a certain amount of actors dumping
Because I believe SCR is not trading at it's fair market price, but rather as a pegged ETH Beta, due to supply games

**Scroll Illiquidity**

As said above, I'm very surprised by the behaviour of SCR, this leads me to believe that the price for the token is "forced", it's there because of supply and perhaps incentive games, but I don't see how this price is real in any way

A quick tour around Exchanges will illustrate my point thoroughly


**Concentrated Ownership**

The ownership of Scroll is alarming

The SCR token is distributed over multiple gnosis safes

However, each safe belongs to the same group of signers and has the same threshold

There is factually no advantage, nor protection being setup on these safes afaict

https://scrollscan.com/address/0x212499e4e77484e565e1965ea220d30b1c469233#readProxyContract

```js
[ getOwners method Response ]
[[0x558A9596940AD909C9e6695Ecd1864b27dE0138f]
[0xba5D4c4475992cc50ae9Cb561a216840Ece68A76]
[0x108493124adf60F401E051e6A05043d8967bff6f]
[0x33fCB6845F6Cf2Da11fA2D68cf0a9F04C8A69be6]
[0x1Da431d2D5ECA4Df735F69fB5ea10c8E630b8f50]]
```

getThreshold
3

https://scrollscan.com/address/0xee198f4a91e5b05022dc90535729b2545d3b03df#readProxyContract
https://scrollscan.com/address/0x206367ebd1fb54f4f33818821feab16f606eebb7#readProxyContract
https://scrollscan.com/address/0x4cb06982dd097633426cf32038d9f1182a9ada0c#readProxyContract
https://scrollscan.com/address/0xff120e015777e9aa9f1417a4009a65d2eda78c13#readProxyContract
https://scrollscan.com/address/0x86e3730739cf5326eeba4cb8a2bf57dd91a2e455#readProxyContract


**Sword of Damocles**

https://scrollscan.com/token/0xd29687c813d741e2f938f4ac377128810e217b1b?a=0x687b50a70d33d71f9a82dd330b8c091e4d772508

This is just an EOA with 72 MLN tokens

Crunching some basic numbers:
>>> 1e9 - 242e6 - 200e6 - 180e6 - 105e6 - 96e6 - 83e6 
94000000.0
>>> 94000000 / 1e6
94.0
>>> 76/94 * 100
80.85106382978722
>>> 


$94MLN is the circulating market cap
$76MLN are in one EOA





**Off of CL I'm looking for the largest swings**

**0x6bF14CB0A831078629D993FDeBcB182b21A8774C - ETH / USD**

```js
pricesWithinTimePeriod 12520
mean 296623020987.87286
STANDARD DEVIATION 55803492279.62583
as percent of mean 18.812933700755245
getHighestAndLowestPrice 409921000000 174995423003


interval 1 Week

eth_usd_swings.pointsOfBiggestNegativeSwing [
  { date: 1722820388, price: 217303390000 },
  { date: 1722247086, price: 339447816000 }
]
deviation 35.98327054783584
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1731401978, price: 342694000000 },
  { date: 1730836693, price: 240278000000 }
]
deviation 42.623960578996


interval One Day

eth_usd_swings.pointsOfBiggestNegativeSwing [
  { date: 1722820388, price: 217303390000 },
  { date: 1722738242, price: 291707960000 }
]
deviation 25.506527144476966
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1716292174, price: 381035000000 },
  { date: 1716205947, price: 309105437400 }
]
deviation 23.27023529738788


interval 4 Hours

eth_usd_swings.pointsOfBiggestNegativeSwing [
  { date: 1722820388, price: 217303390000 },
  { date: 1722809531, price: 275053760000 }
]
deviation 20.99603001246011
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1716243802, price: 366926000000 },
  { date: 1716232916, price: 317582000000 }
]
deviation 15.537404512850225


interval One Hour

eth_usd_swings.pointsOfBiggestNegativeSwing [
  { date: 1722820388, price: 217303390000 },
  { date: 1722817067, price: 267641000000 }
]
deviation 18.80788444221924
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1716235256, price: 346141010000 },
  { date: 1716232916, price: 317582000000 }
]
deviation 8.992641270600979
```

**23% on a day**
The real risk is liquidity crunch making liquidations impossible

**18% in an hour**

If there was going to be a day in which Quill was going to lock-in bad debt, it was going to be that day

It's worth noting that Liquity had no bad debt even during that day

This is a key advantage of the Stability Pool, even though it could technically result in risky behaviour for the "economic system", the system is a lot more resilient because of it

Ultimately all SP stakers are taking the liquidation at face value which is a huge advantage to the system

However, this swing shows how even ETH may need a borrow cap as otherwise it could cause damage to the system



**0x26f6F7C468EE309115d19Aa2055db5A74F8cE7A5 - SCR USD**

```js
pricesWithinTimePeriod 8280
mean 87985535.4692029
STANDARD DEVIATION 20027569.770544685
as percent of mean 22.7623434508219
getHighestAndLowestPrice 144111474 53601588


interval 1 Week

eth_usd_swings.pointsOfBiggestNegativeSwing [
  { date: 1734574388, price: 95669702 },
  { date: 1734071585, price: 144111474 }
]
deviation 33.6140979308837
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1734071585, price: 144111474 },
  { date: 1733778351, price: 86669799 }
]
deviation 66.27646038500677


interval One Day

eth_usd_swings.pointsOfBiggestNegativeSwing [
  { date: 1734129342, price: 118921555 },
  { date: 1734071585, price: 144111474 }
]
deviation 17.479468012380472
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1733808664, price: 116083620 },
  { date: 1733778351, price: 86669799 }
]
deviation 33.937797640444515


interval 4 Hours

eth_usd_swings.pointsOfBiggestNegativeSwing [
  { date: 1734078367, price: 122305169 },
  { date: 1734071585, price: 144111474 }
]
deviation 15.131553647144017
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1733808664, price: 116083620 },
  { date: 1733801040, price: 90725025 }
]
deviation 27.95104768502406


interval One Hour

eth_usd_swings.pointsOfBiggestNegativeSwing [
  { date: 1734074465, price: 129019596 },
  { date: 1734071585, price: 144111474 }
]
deviation 10.47236391461793
eth_usd_swings.pointsOfBiggestPositiveSwing [
  { date: 1733808664, price: 116083620 },
  { date: 1733805125, price: 99448009 }
]
deviation 16.727947766153868
```



**0x45c2b8C204568A03Dc7A2E32B71D67Fe97F908A9**

SEQUENCER

JUST GET BIGGEST UPTIME AND DOWNTIME

The transition from round 18446744073709551721 (value 1) to round 18446744073709551720 (value 0), with times 1734366945 and 1734377886 respectively. We calculate the difference between the two timestamps.

Seems like biggest downtime was 3 hours

Would a 1 day downtime kill the project?
In what way?
How is Scroll Priced? Can it be DOSSed relatively easily?
