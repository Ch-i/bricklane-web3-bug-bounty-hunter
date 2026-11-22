---
affected_contracts: []
derives_from: []
id: rekt-kava-lend-rekt
ingested_at: '2026-11-22T12:45:15Z'
protocol_category: []
published_at: '2026-11-18T00:00:00Z'
related_swc: []
severity: Critical
source: rekt
source_url: https://rekt.news/kava-lend-rekt/
tags:
- rekt
- exploit
- post-mortem
- protocol:kava-lend
- protocol:rekt
- loss-bucket:1M-plus
title: Kava Lend -  Rekt
vuln_class: []
---

# Kava Lend -  Rekt

_Loss: $3,760,000_  
_Incident date: 11/14/2026_  
_Pre-exploit audit: N/A_  

> A dormant BUSD market remained exploitable as Kava’s lending protocol was being wound down. An accounting flaw inflated a few thousand BUSD into a 1.25 billion BUSD claim, worth about $3.76 million at pre-attack prices.


_Source: [https://rekt.news/kava-lend-rekt/](https://rekt.news/kava-lend-rekt/)_


---

![](https://raw.githubusercontent.com/RektHQ/Assets/main/images/2023/01/kava-lend-rekt-header.png)


_[An attacker squeezed Kava Lend’s BUSD net supply to two hundred-millionths of a BUSD](https://x.com/GoPlusSecurity/status/2122289204298432745). The resulting exploit [took roughly $3.76 million in KAVA](https://x.com/GoPlusSecurity/status/2122289195133833376), valued at pre-sell-off prices._

**On November 14, an attacker targeted Kava Lend’s largely inactive BUSD market. [The stablecoin’s issuer, Paxos, had stopped minting new tokens in February 2023](https://www.paxos.com/newsroom/paxos-will-halt-minting-new-busd-tokens), but the lending market remained open.**  
  
[The attacker manipulated its net supply](https://bitquery.io/investigations/kava-hack), the denominator in its deposit-interest calculation, to just 0.00000002 BUSD, then let ordinary interest do the rest.

The protocol’s books [valued a deposit of a few thousand BUSD at more than 1.26 billion BUSD](https://bitquery.io/investigations/kava-hack).

Over the next 98 minutes, [127 loans pulled 55.2 million KAVA from the lending pool](https://x.com/GoPlusSecurity/status/2122289213622342094).  
  
**A [liquidation loop cleared the debt and reopened borrowing capacity](https://x.com/GoPlusSecurity/status/2122289213622342094), without recovering the collateral needed to cover it.**

[The pool held 55.3 million KAVA when the loop began](https://bitquery.io/investigations/kava-hack). Bitquery counted 519 KAVA when it ended.

Kava's first public word arrived more than seven hours after the [opening transaction](https://mintscan.io/kava/tx/6C00E9ED86CB8BE0F49040AA8E693C4184BBBDC4A65FF733804AE1C2FB678AE1), describing ["unexpected behavior originating from a dApp within the Kava ecosystem."](https://x.com/KAVA_CHAIN/status/2121565899568083114)

**That dApp was already on its way out. Governance had [begun voting on limits to Kava Lend’s debt in April](https://kava.valopers.com/proposals/215), yet the dormant BUSD market at the center of the attack [still accepted borrows](https://mintscan.io/kava/tx/D5D8F728D9E11569B3FA40744FF1580BA3EF18C504F0382FE590149E683E337F).**

_If Kava Lend was already being switched off, why was that market still switched on?_

![](https://raw.githubusercontent.com/RektHQ/Assets/main/images/2021/09/rekt-investigates-linebreak.png)
_Credit: [GoPlus Security](https://x.com/GoPlusSecurity/status/2122289204298432745), [Paxos](https://www.paxos.com/newsroom/paxos-will-halt-minting-new-busd-tokens), [Bitquery](https://bitquery.io/investigations/kava-hack), [Kava](https://x.com/KAVA_CHAIN/status/2121565899568083114), [Axelar](https://www.axelar.network/blog/kava-binance-bridge), [The Block](https://www.theblock.co/news/defi/2026-11-14-kava-lend-loses-roughly-3-8-million-to-hack-sending-kava-token-down-nearly-40-440350), [ScaleBit](https://x.com/scalebit_/status/2122234232462573649)_

  
**[The loop finished at 05:42 UTC](https://bitquery.io/investigations/kava-hack). For more than four hours afterward, [KAVA’s price on BNB Chain remained broadly steady](https://bitquery.io/investigations/kava-hack).**

Bitquery's reconstruction follows the attacker-controlled wallets as they consolidated their haul and sent [roughly 4.4 million KAVA to exchange and swap-service deposit addresses between 06:10 and 10:06 UTC](https://bitquery.io/investigations/kava-hack).

Then the cash-out reached the BNB Chain.

The attacker bridged [roughly 49.2 million KAVA through LayerZero](https://x.com/GoPlusSecurity/status/2122289216717455834).

_[At 10:04 UTC, 48.2 million KAVA arrived](https://bitquery.io/investigations/kava-hack) on BNB Chain in a single transfer._  
  
**Three minutes later, the seller started dumping. Over the next 35 minutes, [48.4 million KAVA left the wallet in 46 transfers](https://bitquery.io/investigations/kava-hack). Most of the selling went through MetaMask Swaps; [Bitquery also identified smaller amounts routed through CoW Protocol and Decent](https://bitquery.io/investigations/kava-hack).**  
  
KAVA had traded at [$0.068 on BNB Chain before the selling began](https://bitquery.io/investigations/kava-hack); by the end of that 35-minute burst, [the price there was down 36%](https://bitquery.io/investigations/kava-hack).

[Kava spoke at 11:28 UTC](https://x.com/KAVA_CHAIN/status/2121565899568083114), after the bulk of that selling had cleared, saying its teams were investigating with high priority.

**[Thirty-three minutes later came the line that would anchor its messaging](https://x.com/KAVA_CHAIN/status/2121574325765476462):** "This is not an infinite mint."

_The event, Kava said, [was isolated and contained within Kava Lend](https://x.com/KAVA_CHAIN/status/2121574325765476462). Partner exchanges had paused deposits and withdrawals as a standard precaution._

**At 14:05 UTC, [Kava announced that the Axelar bridge had been paused](https://x.com/KAVA_CHAIN/status/2121605522520510950) “out of an abundance of caution,” halting cross-chain withdrawals through that route.**  
  
[Axelar’s own 2024 notice described its role in moving stranded BEP3 assets](https://www.axelar.network/blog/kava-binance-bridge), including BUSD, out of Kava.

The attacker’s [KAVA transfers to BNB Chain had used a different bridge, LayerZero](https://x.com/GoPlusSecurity/status/2122289216717455834).

Those three posts named the lending application and denied a mint. They did not identify the accounting flaw, quantify the loss, or name an attacker wallet.

_The detailed reconstruction came from outside researchers and reporters._

**[The Block published an onchain analysis late on November 14](https://www.theblock.co/news/defi/2026-11-14-kava-lend-loses-roughly-3-8-million-to-hack-sending-kava-token-down-nearly-40-440350), laying out the roughly 243,000-fold inflation and the 127 loans, and noting that Kava had yet to put a figure on the losses.**

[Bitquery's investigation, with observations timestamped through 16:20 UTC that day](https://bitquery.io/investigations/kava-hack), followed the proceeds across five chains and identified 612,416 USDT blocked at Relay.

[ScaleBit published its code-level breakdown at 07:44 UTC on November 16](https://x.com/scalebit_/status/2122234232462573649), about two hours before Kava posted its report.

_[Kava posted its report at 09:52 UTC](https://x.com/KAVA_CHAIN/status/2122266605677580750). The report said [roughly 53.9 million KAVA had been withdrawn from the lending pool, the vulnerability had been blocked, and some of the stolen funds had been frozen](https://medium.com/@Kava_Chain/hard-lend-security-incident-579888f8dd73)._

**[A proposal would follow to permanently disable new lending and borrowing](https://medium.com/@Kava_Chain/hard-lend-security-incident-579888f8dd73) through the required seven-day governance process.**

[It described the cause as a lending-accounting vulnerability that inflated the value of BUSD collateral](https://medium.com/@Kava_Chain/hard-lend-security-incident-579888f8dd73). It said individual user deposits were "largely unaffected."

Ninety minutes later, [GoPlus posted a seven-part thread with the transactions](https://x.com/GoPlusSecurity/status/2122289195133833376), the state values, and [both attacker wallets](https://x.com/GoPlusSecurity/status/2122289220433985583).

**Kava confirmed the damage. The blow-by-blow still came from outside.**

_What had Kava Lend's own books been recording while the pool emptied?_

  
### Two Base Units

_**[Kava Lend passes interest to depositors through one running number per market](https://bitquery.io/investigations/kava-hack):** The supply index._  
  
**As the index rises, each deposit's value rises in proportion.**

**[The supply index grows by dividing the interest earned since the previous block by the market's net supply](https://x.com/GoPlusSecurity/status/2122289195133833376):** Cash plus outstanding loans, minus reserves.

In a healthy market, the index changes gradually. [By November, Kava Lend’s BUSD market was largely inactive](https://bitquery.io/investigations/kava-hack).

[Bitquery's reconstruction shows about 440,145 BUSD owed to lenders](https://bitquery.io/investigations/kava-hack), against just 0.003 BUSD in cash, 5,084 BUSD in outstanding loans and 7,618 BUSD in reserves.

**Reserves were larger than cash and outstanding loans put together. [ScaleBit calculates that the market’s net supply was negative](https://x.com/scalebit_/status/2122234232462573649).**

_**[ScaleBit](https://x.com/scalebit_/status/2122234232462573649) and [GoPlus](https://x.com/GoPlusSecurity/status/2122289195133833376) point to the same issue in the [public code](https://github.com/Kava-Labs/kava/blob/master/x/hard/keeper/interest.go#L211-L216):** The supply-interest calculation returns a neutral factor when net supply is exactly zero, but does not guard against a positive denominator that is vanishingly small._

[ScaleBit notes that a utilization-ratio calculation](https://x.com/scalebit_/status/2122234232462573649) in the same file checks for negative supply.

The attacker then changed the market’s state until the denominator stood at just two base units.

At 04:00:49 UTC, [the main wallet repaid all 37 outstanding BUSD loans in a single transaction](https://x.com/GoPlusSecurity/status/2122289199823114372).  
  
_[The main wallet paid on behalf](https://x.com/GoPlusSecurity/status/2122289195133833376) of the existing borrowers._

  

**Repayment of 37 BUSD Loans:** [6C00E9ED86CB8BE0F49040AA8E693C4184BBBDC4A65FF733804AE1C2FB678AE1](https://mintscan.io/kava/tx/6C00E9ED86CB8BE0F49040AA8E693C4184BBBDC4A65FF733804AE1C2FB678AE1)

[A second transaction deposited 3,801.60356061 BUSD](https://x.com/GoPlusSecurity/status/2122289204298432745), then borrowed and withdrew 1,267.20118686 BUSD.

**Net-Supply Setup Transaction:** [D5D8F728D9E11569B3FA40744FF1580BA3EF18C504F0382FE590149E683E337F](https://mintscan.io/kava/tx/D5D8F728D9E11569B3FA40744FF1580BA3EF18C504F0382FE590149E683E337F)

**[GoPlus records the resulting state](https://x.com/GoPlusSecurity/status/2122289204298432745):** 635,124,161,944 base units of cash, plus 126,720,118,686 in borrows, minus 761,844,280,628 in reserves.  
  
_**[Net supply](https://x.com/GoPlusSecurity/status/2122289204298432745):** 2 base units, or 0.00000002 BUSD._

**The attacker’s small BUSD loan remained open through the index spike. [ScaleBit’s code analysis says interest accrual is skipped when the market’s prior borrow balance is zero](https://x.com/scalebit_/status/2122234232462573649); keeping the loan open allowed interest to accrue.**

At 04:01:18 UTC, the interest calculation divided [16,759 base units of interest, 0.00016759 BUSD](https://x.com/scalebit_/status/2122234232462573649), by a [net supply of two base units](https://bitquery.io/investigations/kava-hack). Deposits grew [roughly 8,380-fold in that block](https://bitquery.io/investigations/kava-hack).

With net supply still so small, the index continued climbing in successive blocks. [By 04:03:58 UTC, it had climbed from 2.76 to 671,187](https://www.scalebit.xyz/blog/how-5-200-turned-into-55-2-million-kava-a-deep-dive-into-the-kava-lend-exploit-32266d).

The index made [the attacker’s deposit appear to be worth about 1.26 billion BUSD on the pool’s books](https://bitquery.io/investigations/kava-hack).

_[No BUSD was minted](https://x.com/scalebit_/status/2122234232462573649). The index changed the value recorded for the deposit; it did not create tokens._

**[The main wallet then deposited one base unit of BUSD](https://x.com/GoPlusSecurity/status/2122289209050624008), repaid its earlier loan with interest, and withdrew 7,618.44761922 BUSD from the pool, while retaining the inflated BUSD claim.**

**Cash Withdrawal, Claim Retained:** [C59113E2E5C9C0B45782814F3190679A25C8DBA6ACA36B3B0C6BC0433FE02509](https://mintscan.io/kava/tx/C59113E2E5C9C0B45782814F3190679A25C8DBA6ACA36B3B0C6BC0433FE02509)

**Main Wallet:**
[kava1uzx5924cqsutcw365ajs8kkc3rr4vtlyzms255](https://www.mintscan.io/kava/address/kava1uzx5924cqsutcw365ajs8kkc3rr4vtlyzms255)

The main wallet had [withdrawn the pool’s BUSD cash but retained its inflated deposit claim](https://x.com/GoPlusSecurity/status/2122289209050624008).

_If anyone later deposited BUSD, Bitquery says, [the main wallet could withdraw it against that claim](https://bitquery.io/investigations/kava-hack)._  
  
**Before the loop, [Kava Lend's KAVA pool held 55.3 million KAVA; after it, Bitquery reports, 519 remained](https://bitquery.io/investigations/kava-hack).**

[Borrowing KAVA required collateral the protocol would accept and room under the market’s borrowing cap](https://x.com/GoPlusSecurity/status/2122289195133833376). GoPlus reports the KAVA market’s maximum limit at the equivalent of 448,358 KAVA; [Kava’s documentation defines it as a market-level cap on borrowing](https://docs.kava.io/docs/cosmos/modules/hard/state/).  
  
Bitquery found [total outstanding KAVA loans already sitting just under the market’s cap](https://bitquery.io/investigations/kava-hack).

The attacker used a second wallet.

**The main wallet sent BUSD to the helper, [which deposited it as collateral](https://x.com/GoPlusSecurity/status/2122289213622342094). The main wallet then withdrew that BUSD against its inflated claim and sent it back to the helper.**

  

_**[They repeated the cycle](https://bitquery.io/investigations/kava-hack):** The helper’s credited collateral grew on paper while the same real BUSD moved back and forth._

The helper borrowed KAVA worth about half of its credited collateral. In the following block, [the main wallet liquidated the helper](https://x.com/GoPlusSecurity/status/2122289213622342094).  
  
[Bitquery found that this one-block interval had held](https://bitquery.io/investigations/kava-hack) in nine out of ten rounds.

[The first liquidation auction recorded a lot of 0 BUSD against a maximum bid of 31,392,966,446 ukava](https://x.com/GoPlusSecurity/status/2122289213622342094). The loan closed anyway, [reopening room under the market’s borrowing cap](https://bitquery.io/investigations/kava-hack).

**First KAVA Loan (31,392.966444 KAVA - Hard Borrow #6):** [3B32EFCF3937ABE337F10510F2FEB317D22CB660C8F97A0D090026B2F6B32EBE](https://mintscan.io/kava/tx/3B32EFCF3937ABE337F10510F2FEB317D22CB660C8F97A0D090026B2F6B32EBE)

**First Liquidation (0 BUSD auction lot):** [3F79C5AD67A30F8C776E7A9FBB4AB041ACBE334CADAB0E24417C98AFB804F3AB](https://mintscan.io/kava/tx/3F79C5AD67A30F8C776E7A9FBB4AB041ACBE334CADAB0E24417C98AFB804F3AB)

**Helper Wallet:**
[kava1v2s266sll8ca5xrs06swmsc00nwwt7u77eufk4](https://www.mintscan.io/kava/address/kava1v2s266sll8ca5xrs06swmsc00nwwt7u77eufk4)

_[ScaleBit traces that outcome to the liquidation routine](https://x.com/scalebit_/status/2122234232462573649). In its reading of the code, SeizeDeposits returns without an error when the collateral’s dollar value is zero, and the calling function then deletes the borrow as if the seizure had worked._

**[Bitquery reports auction lots of 0, 1 or 2 base units of BUSD across the liquidations](https://bitquery.io/investigations/kava-hack). The app closed each loan, leaving the helper with the borrowed KAVA and no corresponding debt.**  
  
[Early loans were small because little capacity remained under the cap](https://x.com/GoPlusSecurity/status/2122289213622342094). Bitquery says the two wallets [repaid about 1.3 million KAVA in loans owed by other borrowers, freeing more room](https://bitquery.io/investigations/kava-hack). [After about six minutes, individual loans had risen to roughly 445,720 KAVA](https://x.com/GoPlusSecurity/status/2122289213622342094).

Between 04:04:21 and 05:42:04 UTC, [the helper submitted 127 borrows totaling 55,205,050.601443 KAVA](https://x.com/GoPlusSecurity/status/2122289213622342094).

**The helper’s debts were erased. [After repaying other borrowers’ loans, the two wallets retained 53.9 million KAVA](https://bitquery.io/investigations/kava-hack).**

_Where did those coins go?_

### Five Chains, One Locked Door

  
_Six minutes after the last loan, [at 05:48 UTC](https://bitquery.io/investigations/kava-hack), the helper wallet [sent 53,932,564.485351 KAVA to the main wallet](https://x.com/GoPlusSecurity/status/2122289216717455834)._

**That transfer is consistent with [Kava's later estimate of roughly 53.9 million KAVA taken](https://medium.com/@Kava_Chain/hard-lend-security-incident-579888f8dd73).**  
  
[Bitquery says 55.2 million KAVA was borrowed in total](https://bitquery.io/investigations/kava-hack), and about 1.3 million went to repay loans owed by other borrowers.

**Kava Lend Module Account (the drained pool):** [kava1a42xtwfzphuuu9mdp0es6633wu5mm8fhm789v3](https://www.mintscan.io/kava/address/kava1a42xtwfzphuuu9mdp0es6633wu5mm8fhm789v3)A third wallet did the selling, [so Bitquery calls it the seller](https://bitquery.io/investigations/kava-hack). It was eight days old. On November 6, it appeared on Kava, BNB Chain and Ethereum, and sent 16 coins across the bridge as a test.

**Seller Wallet, Kava:**
[kava1xltn9y20smxxav0gwsv7xpr2ww0szyzzga76lv](https://www.mintscan.io/kava/address/kava1xltn9y20smxxav0gwsv7xpr2ww0szyzzga76lv)

  
**Seller Wallet, Kava EVM and BNB Chain:**
[0x37d732914f86cc6eb1e87419e3046a739f011042](https://bscscan.com/address/0x37d732914f86cc6eb1e87419e3046a739f011042)

_The main wallet took a quieter exit first. [Between 06:10 and 10:06 UTC, it sent about 4.4 million KAVA to exchange and swap-service deposit addresses](https://bitquery.io/investigations/kava-hack)._

**[Bitquery identifies two Ethereum payouts](https://bitquery.io/investigations/kava-hack) that it links to those Kava deposits through timing and amounts.**

[At 06:28 UTC, 663,900 KAVA went to a deposit address on Kava](https://bitquery.io/investigations/kava-hack). Seventeen minutes later, [44,219 USDT reached the seller on Ethereum](https://etherscan.io/tx/0x8673f1a19d2f9c5fa712631f566cc9e6d2011fe3e8b2e97fb46db5f8178a48bc) from a wallet [Bitquery labels as HitBTC's](https://bitquery.io/investigations/kava-hack).

**HitBTC-Labeled Payout, Ethereum (44,219 USDT):** [0x8673f1a19d2f9c5fa712631f566cc9e6d2011fe3e8b2e97fb46db5f8178a48bc](https://etherscan.io/tx/0x8673f1a19d2f9c5fa712631f566cc9e6d2011fe3e8b2e97fb46db5f8178a48bc)

[At 09:21 UTC, 170,000 KAVA went to another deposit address](https://bitquery.io/investigations/kava-hack). At 09:42 UTC, [11,162 USDC arrived](https://etherscan.io/tx/0x43b7fc6bf3ee36dfce7f26969d852664bdbea50974a98749560b154d743efa5f) from a wallet [Bitquery labels as Bybit's](https://bitquery.io/investigations/kava-hack).

**Bybit-Labeled Payout, Ethereum (11,162 USDC):** [0x43b7fc6bf3ee36dfce7f26969d852664bdbea50974a98749560b154d743efa5f](https://etherscan.io/tx/0x43b7fc6bf3ee36dfce7f26969d852664bdbea50974a98749560b154d743efa5f)

**The bulk went through LayerZero.**

_**[GoPlus counts three transfers through the LayerZero contract on Kava EVM](https://x.com/GoPlusSecurity/status/2122289216717455834):** 149,045.86 KAVA, then 48,209,645.86 KAVA, both including fees, followed by roughly 849,080.97 more._  
  
[The first two minted 48,358,600 KAVA on BNB Chain](https://x.com/GoPlusSecurity/status/2122289216717455834). All three came to about 49.21 million.

**LayerZero Contract, Kava EVM:**  
[0x964fef44181763f5ee8eddfa124c9ad476570e2a](https://www.mintscan.io/kava/evm/contract/0x964fef44181763f5ee8eddfa124c9ad476570e2a)

**KAVA Token, BNB Chain:**
[0x9bafc8d4b487cebff201721702507a3e2c67ad79](https://bscscan.com/token/0x9bafc8d4b487cebff201721702507a3e2c67ad79)

**Bridge Transfer, Source Side (Kava, block 23,488,570):** [0x062c77201dc1dfd6f07d4186d964538640a4f067f2fd3e5a9f3b36e7ae1ba248](https://mintscan.io/kava/tx/0x062c77201dc1dfd6f07d4186d964538640a4f067f2fd3e5a9f3b36e7ae1ba248?height=23488570)

**Bridge Transfer, Destination Side (48.2 million KAVA lands on BNB Chain):** [0x76c349063269fbf3aad7e4f227e80bda0f62b15ae0a99e309f5462487d5f67c1](https://bscscan.com/tx/0x76c349063269fbf3aad7e4f227e80bda0f62b15ae0a99e309f5462487d5f67c1)

_[Bitquery counts 48.4 million KAVA leaving the seller’s wallet during the main selling burst](https://bitquery.io/investigations/kava-hack), including 14,000 KAVA in trading-app fees. Most of the selling went through MetaMask Swaps. Bitquery’s published per-venue figures add up to more than its stated total; the article does not explain the difference._

**Example Sale Transaction 1, BNB Chain:** [0x5973dc1e5e0f67dec2d26a87aff7c5795b06a1090e308a75fdb4962f58aa0130](https://bscscan.com/tx/0x5973dc1e5e0f67dec2d26a87aff7c5795b06a1090e308a75fdb4962f58aa0130)

**Example Sale Transaction 2, BNB Chain:** [0xa3e2e8b63ad6e995bfead481150405311d9b784e26d1749197046b70214529b0](https://bscscan.com/tx/0xa3e2e8b63ad6e995bfead481150405311d9b784e26d1749197046b70214529b0)

[Bitquery places the main selling burst between 10:07 and 10:42 UTC](https://bitquery.io/investigations/kava-hack). Two hours after selling began, its reconstruction puts KAVA on BNB Chain 52% below the starting price.

_[The proceeds came to about $2.09 million](https://bitquery.io/investigations/kava-hack). Bitquery counts roughly 3,333 BNB and a little USDT._

**[The roughly $2.09 million raised on BNB Chain represented that exit route's proceeds](https://bitquery.io/investigations/kava-hack), not the attacker's total proceeds across the operation.**

In Bitquery’s November 14 snapshot, [the seller’s KAVA balance on BNB Chain was zero](https://bitquery.io/investigations/kava-hack). On Kava, Bitquery reported [921 KAVA across the three principal wallets](https://bitquery.io/investigations/kava-hack) and [about 300,000 KAVA across two other associated wallets](https://bitquery.io/investigations/kava-hack).

Between 10:45 and 11:50 UTC, [the BNB left BNB Chain by four routes](https://bitquery.io/investigations/kava-hack).

[The largest share went to Hyperliquid](https://bitquery.io/investigations/kava-hack). LI.FI carried 750 BNB to Arbitrum as 450,776 USDC. Chainflip turned another 1,083 BNB into 347 ETH on Ethereum. The seller split the ETH across new wallets, each of which swapped its ETH to USDC on Arbitrum through LI.FI and deposited the USDC on Hyperliquid.

_[Eight Hyperliquid accounts received $1.17 million in USDC](https://bitquery.io/investigations/kava-hack), including about $41,000 from the morning's exchange payouts. Each bought XMR1, a Hyperliquid token named after Monero, within a minute of its deposit._

**[Bitquery now identifies the eight accounts as deposit addresses of a Monero swap service](https://bitquery.io/investigations/kava-hack). They still held 2,190 XMR1 on November 17. Bitquery’s interpretation is that the seller was most likely paid in Monero while the service retained the XMR1. Bitquery could not observe those Monero payments and did not verify what backs XMR1 or what holders can redeem.**

**Hyperliquid Account 1:**
[0x8ff50f64a158b255e4f29cb84a2d54446b181c89](https://app.hyperliquid.xyz/explorer/address/0x8ff50f64a158b255e4f29cb84a2d54446b181c89)

**Hyperliquid Account 2:**
[ ](https://bitquery.io/investigations/kava-hack)[0x43518ec23efc8260b05a0eadfdfd68d0a8853fdd](https://app.hyperliquid.xyz/explorer/address/0x43518ec23efc8260b05a0eadfdfd68d0a8853fdd)

**Hyperliquid Account 3:**  
[0xa09895c550704665197db865d451acb68d6444ed](https://app.hyperliquid.xyz/explorer/address/0xa09895c550704665197db865d451acb68d6444ed)

**Hyperliquid Account 4:**  
[0x764796099b205e625342df7f5402809ee5e71925](https://app.hyperliquid.xyz/explorer/address/0x764796099b205e625342df7f5402809ee5e71925)

**Hyperliquid Account 5:**  
[0x6da8249bce36356b973c11a4c826b6948d5a42b8](https://app.hyperliquid.xyz/explorer/address/0x6da8249bce36356b973c11a4c826b6948d5a42b8)

**Hyperliquid Account 6:**  
[0x8e83ea331caec2f61edc0bfd1fa2c214db7799dd](https://app.hyperliquid.xyz/explorer/address/0x8e83ea331caec2f61edc0bfd1fa2c214db7799dd)

**Hyperliquid Account 7:**  
[0x34db14cef0becbef6f111a81126455a85e01f0d8](https://app.hyperliquid.xyz/explorer/address/0x34db14cef0becbef6f111a81126455a85e01f0d8)

**Hyperliquid Account 8:**  
[0xe8b1beeb424f3d8059e5b23b6f6171a6f8451c50](https://app.hyperliquid.xyz/explorer/address/0xe8b1beeb424f3d8059e5b23b6f6171a6f8451c50)

A smaller share went south through Bridgers. [500 BNB became 4,025 SOL, then 303,426 USDC](https://bitquery.io/investigations/kava-hack), which moved to a Solana wallet paying out to more than 100,000 addresses a month.

**Solana Wallet That Received the SOL:** [Em3FN5PRGt8nB7zHQnDneQg1CwxsFsKAVHahKcBYauG3](https://explorer.solana.com/address/Em3FN5PRGt8nB7zHQnDneQg1CwxsFsKAVHahKcBYauG3)

[Bitquery traces 303,426 USDC to a Solana address](https://bitquery.io/investigations/kava-hack) that [Arkham labels as Mayan Finance](https://arkm.com/explorer/entity/mayan-finance). Bitquery’s published trace ends at that address; it did not follow the USDC onward.

**Mayan Finance–Labeled Recipient, Solana:** [D8cJRpXaCWVK8c3doDq7Ymoz2XE4WyhFhbgNytWwqptA](https://explorer.solana.com/address/D8cJRpXaCWVK8c3doDq7Ymoz2XE4WyhFhbgNytWwqptA)

_[The remaining 1,000 BNB took the fourth route](https://bitquery.io/investigations/kava-hack) and hit the locked door. The seller initiated the transaction through MetaMask’s Meta Bridge; the route passed through LI.FI and deposited approximately 612,416 USDT into Relay._

**According to Bitquery, [the order requested ETH on Ethereum, but Relay’s record showed it blocked under BLOCKED_WALLET, with no payout or refund identified as of 16:20 UTC on November 14](https://bitquery.io/investigations/kava-hack).**

**Relay Deposit, BNB Chain:** [0xb844e460490048f6f424f1859c814954586991e1bb854935fb512500781ca79f](https://bscscan.com/tx/0xb844e460490048f6f424f1859c814954586991e1bb854935fb512500781ca79f)

[Bitquery reported that this deposit was marked withdrawable](https://bitquery.io/investigations/kava-hack), but did not verify whether the seller could actually reclaim the funds.

**[Kava governance had been voting on limits to Kava Lend](https://kava.valopers.com/proposals/215) since April.**  
  
_What had those votes actually changed?_

### Retirement, Accelerated

_Kava’s report said [the planned retirement of HARD Lend’s legacy lending functionality was being accelerated](https://medium.com/@Kava_Chain/hard-lend-security-incident-579888f8dd73)._  
  
**Accelerated implies something was already moving.**

It was. On April 27, [kava1me2recm86t27c24q0kple0cdd5jlglqnqz9l3t submitted Proposal 215, the first phase of a wind-down covering Kava's Mint and Lend products](https://kava.valopers.com/proposals/215).

[Its description called for capping CDP and Lend debt near current usage](https://kava.valopers.com/proposals/215), leaving incentive schedules unchanged and extending incentive claims to June 30.

[Phase 2 arrived on August 7 as Proposal 221](https://kava.valopers.com/proposals/221), submitted by kava1m7hc4fr82cwndags3tz3susmwlq6sku02zthtf. Its description promised to finalize the Phase 1 parameters and align deprecated market limits.

_It was crushed. On August 14, [62.91% voted no and 31.37% voted NoWithVeto. Yes drew 0.18%](https://kava.valopers.com/proposals/221)._

**A second Phase 2 attempt, [Proposal 222](https://kava.valopers.com/proposals/222), went up on September 28 from kava12mg9h7s6mselrh0ks2xa9zaydtazarx6632ahs. Its description called for ending incentives, closing claims on November 1, and setting Lend borrow limits near outstanding balances.**  
  
[It passed on October 5 with 92.53% in favor](https://kava.valopers.com/proposals/222) and told users to close positions before Phase 3.

[Thirteen days after the stated claims deadline](https://kava.valopers.com/proposals/222), the [BUSD market still let an attacker borrow 1,267.20118686 BUSD](https://mintscan.io/kava/tx/D5D8F728D9E11569B3FA40744FF1580BA3EF18C504F0382FE590149E683E337F).

[Proposal 215 described capping CDP and Lend debt near current usage](https://kava.valopers.com/proposals/215), while [Proposal 222 described setting Lend borrow limits near outstanding balances](https://kava.valopers.com/proposals/222). Those descriptions outlined limits on lending, not a complete borrowing shutdown.

_Between them, [the rejected Proposal 221 called for finalizing Phase 1 adjustments and aligning “deprecated market limits”](https://kava.valopers.com/proposals/221). Its description did not name BUSD, so it does not establish that the rejected proposal would have closed the route the attacker later used._

**[GoPlus put the KAVA market’s configured borrowing cap at 448,358 KAVA](https://x.com/GoPlusSecurity/status/2122289195133833376).**

[Proposal 222’s description called for setting Lend borrow limits near outstanding balances](https://kava.valopers.com/proposals/222), but the description does not specify the KAVA cap.

**[Kava’s developer documentation describes a procedure for retiring a money market](https://docs.kava.io/docs/cosmos/modules/hard/state/):** Enable the maximum-borrow-limit check and set the limit to zero to prevent new borrowing; zero the base rate, base multiplier and jump multiplier to stop interest accumulating; and remove the relevant rewards. The documentation describes the procedure, not whether those steps were taken for BUSD.

The published attack reconstructions describe borrowing and interest accrual remaining possible.  
  
_[GoPlus says the attacker borrowed and withdrew 1,267.20118686 BUSD](https://x.com/GoPlusSecurity/status/2122289204298432745), leaving net supply at two base units._  
  
**[ScaleBit says a tiny outstanding borrow allowed interest to continue accruing](https://www.scalebit.xyz/blog/how-5-200-turned-into-55-2-million-kava-a-deep-dive-into-the-kava-lend-exploit-32266d), driving the supply index upward.**

[Kava documentation says funds left in a retired market](https://docs.kava.io/docs/cosmos/modules/hard/state/), can be reimbursed or reallocated through a chain upgrade.  
  
[Kava’s November 16 incident report did not specify whether that mechanism would be used](https://medium.com/@Kava_Chain/hard-lend-security-incident-579888f8dd73). It said remaining positions would be addressed through an orderly process, with further guidance to follow.

The pool was left with almost no available KAVA. [Bitquery reported 519 KAVA after the borrowing loop](https://bitquery.io/investigations/kava-hack).  
  
_Kava’s report did not say whether lenders would be made whole._

**[Kava’s incident report described individual user deposits as “largely unaffected”](https://medium.com/@Kava_Chain/hard-lend-security-incident-579888f8dd73), but did not provide a breakdown of whose deposits made up the drained pool.**

KAVA’s market price also fell sharply. [ScaleBit reported a seven-day decline of 49.2%, an all-time low of $0.03195 and approximately $37.70 million erased from market capitalization](https://www.scalebit.xyz/blog/how-5-200-turned-into-55-2-million-kava-a-deep-dive-into-the-kava-lend-exploit-32266d). The market-cap decline was not a measure of realized losses to Kava or its treasury.

Recovery remained unresolved. In its November 16 report, [Kava said a portion of the attacker’s funds had been frozen and that ecosystem contributors, partners, exchanges, other venues and law enforcement were continuing efforts to trace, freeze and recover the proceeds](https://medium.com/@Kava_Chain/hard-lend-security-incident-579888f8dd73).  
  
Upbit’s response introduced a separate uncertainty for KAVA holders. [According to BlockchainReporter, the exchange suspended KAVA deposits and withdrawals on November 14, designated the token a trading-caution item on November 16 and set the review to run until December 14–18](https://blockchainreporter.net/upbit-kava-trading-caution-designation/). The review could be extended or lead to termination of trading support; the caution designation was not itself a final delisting decision.

_The inflated BUSD claim raised another unresolved question. [ScaleBit warned that the attacker’s roughly 1.26 billion BUSD deposit claim could be used to withdraw real BUSD](https://www.scalebit.xyz/blog/how-5-200-turned-into-55-2-million-kava-a-deep-dive-into-the-kava-lend-exploit-32266d) subsequently deposited into the market unless the relevant market parameters were frozen or zeroed._  
  
**[Kava said it had blocked the identified exploit](https://medium.com/@Kava_Chain/hard-lend-security-incident-579888f8dd73), but whether the inflated BUSD claim remained usable was unclear.**  
  
Governance was moving toward additional restrictions. On November 16, [Kava announced Proposal 223, “Freeze Kava Lend Borrowing and Restore the USD 10 Minimum”](https://gov.1xp.com/proposals/kava_2222-10/223).  
  
[Its published description calls for setting every Kava Lend borrowing cap to zero and restoring the USD 10 minimum](https://gov.1xp.com/proposals/kava_2222-10/223), blocking new borrowing while permitting repayments under the normal minimum-debt rule.

[Kava also announced Proposal 224, “Restore Kava Stability Committee Lend Risk Permissions”](https://www.mintscan.io/kava/proposals/224). [](https://gov.1xp.com/proposals/kava_2222-10/224) The proposal’s published description calls for adding BitGo WBTC and Meson mBTC to Committee 1’s MoneyMarkets whitelist while preserving its existing membership and voting rules.

**Kava governance can vote on shutting lending down.**  
  
_Who decides what the pool’s remaining lenders get back?_

![](https://raw.githubusercontent.com/RektHQ/Assets/main/images/2021/03/rekt-linebreak.png)

_[ScaleBit found no compromised key and no manipulated oracle](https://x.com/scalebit_/status/2122234232462573649) behind the Kava Lend exploit._  
  
**[Its analysis points instead to an accounting edge case where the protocol's safeguards](https://x.com/scalebit_/status/2122234232462573649) did not stop.**

A stablecoin [Paxos stopped minting in 2023](https://www.paxos.com/newsroom/paxos-will-halt-minting-new-busd-tokens) sat in a largely inactive market until an attacker reduced its net supply to [two base units, two hundred-millionths of a BUSD](https://x.com/GoPlusSecurity/status/2122289204298432745).

The resulting index spike turned a deposit of a few thousand BUSD into an accounting claim of [more than 1.25 billion BUSD](https://x.com/GoPlusSecurity/status/2122289195133833376).

[ScaleBit](https://x.com/scalebit_/status/2122234232462573649) and [GoPlus](https://x.com/GoPlusSecurity/status/2122289213622342094) say the liquidation path then closed KAVA debts while recovering little or no BUSD collateral.

_In Bitquery's on-chain reconstruction, the loop left a pool that had held [55.3 million KAVA with just 519 remaining after 98 minutes](https://bitquery.io/investigations/kava-hack)._

**[Hours passed between the theft and the main sell-off](https://bitquery.io/investigations/kava-hack). The detailed public reconstruction came largely from outside Kava.**

What comes next returns to the governance process that moved Kava Lend toward retirement in 2026.

[Proposal 215 described capping Kava CDP and Lend debt](https://kava.valopers.com/proposals/215) near current usage.  
  
A follow-up, [Proposal 221, sought to finalize those adjustments and align deprecated-market limits](https://kava.valopers.com/proposals/221), but voters rejected it.  
  
_The wind-down direction became explicit in [Proposal 222, which later passed under the title “End Incentives, Limit Borrowing, and Signal Protocol Wind-Down.”](https://kava.valopers.com/proposals/222)_  
  
**[Kava’s documentation sets out the market-level steps for that process](https://docs.kava.io/docs/cosmos/modules/hard/state/): Before a market is deprecated, its borrow-limit check should be enabled, the limit set to zero, and the base rate, base multiplier and jump multiplier zeroed.**  
  
Whether those settings were applied to BUSD, and whether [the rejected Proposal 221](https://kava.valopers.com/proposals/221) would have blocked the exploit, remains unclear.  
  
[Kava's Security Incident report said protective measures were in force](https://medium.com/@Kava_Chain/hard-lend-security-incident-579888f8dd73), and that it planned to submit a proposal to permanently disable new lending and borrowing. The report does not say whether existing lenders will be made whole.

As of November 18, [Proposal 223, "Freeze Kava Lend Borrowing and Restore the USD 10 Minimum,"](https://kava.valopers.com/proposals/223) was still in the voting process, which closes on November 23rd.  
  
**A protocol marked for retirement still had a market the attacker could use.**  
  
_How many other wind-downs are leaving the lights on in markets nobody is watching?_

![](https://raw.githubusercontent.com/RektHQ/Assets/main/images/2021/08/rekt-outline-conc.png)
