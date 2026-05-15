---
affected_contracts: []
derives_from: []
id: rekt-moola-markets-rekt
ingested_at: '2026-05-15T14:50:15Z'
protocol_category: []
published_at: '2022-10-19T00:00:00Z'
related_swc: []
severity: Critical
source: rekt
source_url: https://rekt.news/moola-markets-rekt/
tags:
- rekt
- exploit
- post-mortem
- protocol:moola-market
- protocol:rekt
- loss-bucket:1M-plus
title: Moola Market - REKT
vuln_class: []
---

# Moola Market - REKT

_Loss: $8,400,000_  
_Incident date: 10/19/2022_  
_Pre-exploit audit: N/A_  

> Bear markets offer easy opportunities to market manipulators, who find it easier to move prices when liquidity is low. Lending protocol Moola Market is the latest to fall victim to a “highly profitable trading strategy”, and the first CELO protocol on the rekt.news leaderboard (#63).


_Source: [https://rekt.news/moola-markets-rekt/](https://rekt.news/moola-markets-rekt/)_


---

![](https://raw.githubusercontent.com/RektHQ/Assets/main/images/2022/10/moola-header.png)

Lending protocol [Moola Market](https://moola.market/) is the latest to fall victim to a “[highly profitable trading strategy](https://twitter.com/avi_eisen/status/1581326197241180160)”, and the first CELO protocol on the rekt.news [leaderboard](https://rekt.news/leaderboard/) (#63).

  

Similarly to last week’s [Mango Markets](https://rekt.news/mango-markets-rekt/) case, the exploit was carried out via price manipulation of a collateral asset, this time netting the attacker $8.4M.

  

The Moola team [announced](https://twitter.com/moola_market/status/1582432297835368449) the incident on Twitter, appealing to the CEX-funded attacker to return funds in exchange for a bounty.

  

Fortunately, just six hours later, over 90% of the funds were [returned](https://celoscan.io/tx/0xc3018d2e65bcd7c89d4fa2849017c6169c84c0934ca80c2c8dfd065da90d569d) to the Moola [multisig](https://celoscan.io/address/0xd7f77169d5e6a32c5044052f9a49eb94697b25ed), with the exploiter keeping ~$525k as a bounty, of which $37k was donated to charity…

  

_A guilty conscience or a planned whitehat?_

  

![](https://raw.githubusercontent.com/RektHQ/Assets/main/images/2021/09/rekt-investigates-linebreak.png)

  

_Credit: [FrankResearcher](https://twitter.com/FrankResearcher/status/1582448720985014273)_

  

**This attack was a simple price manipulation which didn’t require any coding.**

  

Using initial funding of 243k CELO (~$180k), the attacker supplied 60k CELO in order to borrow 1.8M of the protocol’s native token, MOO, which could itself be used as collateral to borrow against other assets.

  

Then, using the remaining CELO to buy MOO on Ubeswap, the attacker [pumped the price](https://twitter.com/BeosinAlert/status/1582622616439107585) of their MOO collateral…

![](https://raw.githubusercontent.com/RektHQ/Assets/main/images/2022/10/moola-chart.png)


…allowing them to borrow the remaining assets on the protocol, draining all liquidity:

  

- 8.8M CELO ($6.5M)
- 765k cEUR ($0.7M)
- 1.8M MOO ($0.6M)
- 644k cUSD ($0.6M)

  

**Attacker's address: [0x95b5579b323ddc6cd290bd4da6e56ba019588efc](https://celoscan.io/address/0x95b5579b323ddc6cd290bd4da6e56ba019588efc)**

  

![](https://raw.githubusercontent.com/RektHQ/Assets/main/images/2021/03/rekt-linebreak.png)

  

In addition to returning the majority of the funds, the whitehat also donated 50k CELO ($37k) of the bounty to [Impact Market](https://twitter.com/mbarrbosa/status/1582515890767421441), a protocol focused on providing UBI for vulnerable families in developing countries.

  

Bear markets offer easy opportunities to market manipulators, who find it easier to move prices when liquidity is low. Especially when smaller protocols allow use of their native tokens as collateral, whose [dollar value](https://www.coingecko.com/en/coins/moola-market) dies away as the bear drags on.

  

Moola Markets have learned their lesson, and are [proposing](https://twitter.com/Moola_Market/status/1582588119114608640) to remove MOO as a viable collateral asset via protocol governance.

  

But anyone with deep enough pockets can stress test DeFi markets in their current state.

  

_[Who will be next?](https://twitter.com/avi_eisen/status/1582763707742183424)_

  

![](https://raw.githubusercontent.com/RektHQ/Assets/main/images/2021/08/rekt-outline-conc.png)
