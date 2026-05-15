---
affected_contracts: []
derives_from: []
id: rekt-merlin2-rekt
ingested_at: '2026-05-15T14:50:15Z'
protocol_category: []
published_at: '2021-05-27T00:00:00Z'
related_swc: []
severity: Critical
source: rekt
source_url: https://rekt.news/merlin2-rekt/
tags:
- rekt
- exploit
- post-mortem
- protocol:merlin-labs
- protocol:rekt-2
- loss-bucket:under-1M
title: Merlin Labs - REKT 2
vuln_class: []
---

# Merlin Labs - REKT 2

_Loss: $550,000_  
_Incident date: 05/26/2021_  
_Pre-exploit audit: Unaudited_  

> Once was not enough for Merlin Labs. Just 8 hours after the first attack, they lost another ~200 ETH, yet still they remain at the bottom of the leaderboard. Must try harder.


_Source: [https://rekt.news/merlin2-rekt/](https://rekt.news/merlin2-rekt/)_


---

![](https://raw.githubusercontent.com/RektHQ/Assets/main/images/2021/05/merlin2-header.png) 
**Once was not enough for Merlin Labs.**

After we [wrote about](https://www.rekt.news/merlinlabs-rekt/) their $680k loss, a reader [pointed out](https://twitter.com/dmosinee/status/1397645029880045570?s=20) that the story did not end there.

**Just 8 hours after the first attack, they lost another ~200 ETH to a completely different exploit.**

[Transaction Details.](https://bscscan.com/tx/0x664cbe3af9d7627819e1955a90d777d6cf492021eede057bc52686186da192e5)

This is the [address of the second hacker.](https://bscscan.com/address/0xf6f6cc59ca893bd11180654b285b1a0652fca36a)

The second attack took advantage of a mistake in their new priceCalculator that mispriced only BAND. 

>credit: [watchpug](https://twitter.com/WatchPug_)

![](https://raw.githubusercontent.com/RektHQ/Assets/main/images/2021/05/merlin2-analysis.png) 

**~$550,000 dollars lost due to a fix that did more damage than good.**

The Merlin team have outlined a [compensation plan](https://merlinlab.medium.com/our-road-ahead-fa2fafc8167d) for those who lost out in the [initial attack](https://www.rekt.news/merlinlabs-rekt/), and the one which came afterward.

When we mentioned that Merlin Labs “Must try harder”, we didn’t mean to climb up the [leaderboard…](https://www.rekt.news/leaderboard/)

This second attack gave them another chance, but they remain in position #28.

_Must try harder._ 

![](https://raw.githubusercontent.com/RektHQ/Assets/main/images/2021/03/rekt-text-linebreak.png)
