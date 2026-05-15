---
affected_contracts: []
derives_from: []
id: rekt-sovryn-rekt
ingested_at: '2026-05-15T14:50:15Z'
protocol_category: []
published_at: '2022-10-09T00:00:00Z'
related_swc: []
severity: Critical
source: rekt
source_url: https://rekt.news/sovryn-rekt/
tags:
- rekt
- exploit
- post-mortem
- protocol:sovryn
- protocol:rekt
- loss-bucket:1M-plus
title: Sovryn - REKT
vuln_class: []
---

# Sovryn - REKT

_Loss: $1,111,000_  
_Incident date: 10/04/2022_  
_Pre-exploit audit: Unaudited_  

> More fuel for the maxis. ~$1.1M was stolen from Sovryn, a “DeFi” protocol on the controversial “Bitcoin smart contract network” RSK.


_Source: [https://rekt.news/sovryn-rekt/](https://rekt.news/sovryn-rekt/)_


---

![](https://raw.githubusercontent.com/RektHQ/Assets/main/images/2022/10/sovryn-header.png)

_More fuel for the maxis._
 
**On the 4th of October, ~$1.1M was stolen from Sovryn, a “DeFi” protocol on the controversial “Bitcoin smart contract network”, [RSK](https://www.rsk.co/)  (apparently “the most secure smart contract network in the world”).**

The devs placed contracts into “maintenance mode” preventing further losses and the attack was announced via a rather self-congratulatory written [thread](https://twitter.com/EdanYago/status/1577411283359440897) on Twitter.
  
But, isn’t pausing contracts somewhat _centralised,_ for a protocol catering to Bitcoiners?

While truly Bitcoin-native DeFi apps remain impossible, good marketing attracts investors, and Sovryn was heavily-shilled by [Anthony Pompliano](https://www.sovryn.app/blog/sovryn-begins-trading-as-anthony-pompliano-leads-9m-investment) upon launch last year, based on an [erroneous claim](https://twitter.com/APompliano/status/1402704745647816704) that it had higher TVL than Uniswap v3, at almost $2B.

 The TVL turned out to be miscounted, including native staked SOV, leading to DeFiLlama’s [addition of the staking toggle](https://twitter.com/DefiLlama/status/1402762264361549826) to their TVL metrics, and dropping Sovryn’s figure to just $52M.

Since then, [TVL is down](https://defillama.com/protocol/sovryn) approx 90% since peak and the native token [SOV](https://www.coingecko.com/en/coins/sovryn) has dropped 99% from its ATH of one year ago.  

![](https://raw.githubusercontent.com/RektHQ/Assets/main/images/2021/09/rekt-investigates-linebreak.png)

_Credit: [BeosinAlert](https://twitter.com/BeosinAlert/status/1578375800427945984)_

**The protocol lost funds from two legacy lending pools: the RBTC (RSK-bridged BTC) pool, for 45 RBTC (~$900k), and the USDT pool, for 211k USDT.**

According to [Beosin’s analysis](https://twitter.com/BeosinAlert/status/1578375800427945984), the exploit was down to the “_external call of callTokensToSend function._”

**Attacker’s address: [0xc92ebecda030234c10e149beead6bba61197531a](https://explorer.rsk.co/address/0xc92ebecda030234c10e149beead6bba61197531a)**

Example tx: [0xf5ea62…](https://explorer.rsk.co/tx/0xf5ea6266a56f4e0135b73f63050afca7146bc940ac73da8b5fade9d8031582e2)

>The attacker first deploys the attack contract and transfers into 0.03 RBTC.
>
>Then invokes the attack contract to borrow 8.20 RBTC to three pair addresses via flashloan, then deposits the entire 8.23 RBTC.
>
>The attacker uses the LP to borrow 52,999 side tokens.
>
>The closeWithDeposit function is then called to repay the collateral. 26,900 side tokens were swapped for 4.17 RBTCs. Notice that the attacker minted 26,000 side tokens into 22,653 Load Token, while in the closeWithDeposit function, there is no such mint function.
>
>Then we found that the attacker used the side tokens to call the attack contract externally, and used the attack contract to call the mint function.
>
>Because in the tokenPrice function, it relies on the number of side tokens to calculate the Load token price, and the total number of tokens has not been updated at this time, resulting in the attacker getting more Load tokens.
>
>Finally, the attacker calls the burn function to burn 22,653 Load Token to get 27,086 side token.
>
>Then the attacker calls the related function in a loop to get the side token, and finally converts them to RBTC.
>
>The stolen funds were deposited into Tornado cash.

An [update](https://www.sovryn.app/blog/interim-exploit-update) posted on October 7th assures that no Sovryn individuals need to worry, stating that:

>Roughly half of the funds have been recovered so far
>
>Potential remaining user losses will be fully covered by the Exchequer

And five days after the attack, [a final announcement:](https://twitter.com/SovrynBTC/status/1578770047643762689)

>”All user funds stuck on the ETH bridge have been unstuck. There is only once [sic] exception: the user bridging in USDT to XUSD.”

![](https://raw.githubusercontent.com/RektHQ/Assets/main/images/2021/03/rekt-linebreak.png)

**There is no shortage of BTC-focused projects on Ethereum, including bridged assets such as WBTC/renBTC and protocols like [Badger](https://rekt.news/badger-rekt/), but the scale of Bitcoin adoption remains low.**

Even the largest of these, WBTC, with a [TVL of ~$5B](https://defillama.com/protocol/wbtc), barely scratches the surface of Bitcoin’s $387 billion market cap.

**BTC maxis don’t trust their coins to be wrapped onto other networks. Many are suspicious of Ethereum, DeFi and any experimentation regarding what they believe to be a pure cryptocurrency.**  

_This incident will only give the bitcoiners even more reasons to cling onto their digital gold._

![](https://raw.githubusercontent.com/RektHQ/Assets/main/images/2021/08/rekt-outline-conc.png)
