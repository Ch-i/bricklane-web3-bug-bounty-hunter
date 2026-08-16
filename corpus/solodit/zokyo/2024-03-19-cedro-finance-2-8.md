---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-2-8
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: No check for staleness of Price in Oracle
vuln_class: []
---

# No check for staleness of Price in Oracle

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved 

**False Stale Data Declaration**: 

There is no check for staleness of price. The Oracle data feeds can return stale pricing data for many reasons. If the returned pricing data is stale, this code will execute with prices that don’t reflect the current pricing resulting in a potential loss of funds for the user and/or the protocol. The contract might incorrectly mark price data as stale (outdated) and revert transactions due to its static `acceptedDelayTime`, even when Chainlink's data update frequency (heartbeat) accommodates longer intervals. This issue could unnecessarily prevent the execution of valid transactions, causing operational inefficiencies and potentially harming user trust.

Smart contracts should always check the `updatedAt` parameter returned from `latestRoundData()` and compare it to a staleness threshold.

The staleness threshold should ideally correspond to the heartbeat of the oracle’s price feed. This can be found on Chainlink’s list of Ethereum mainnet price feeds by checking the “Show More Details” box, which will show the “Heartbeat” column for each feed. For networks other than Ethereum mainnet, make sure to select your desired L1/L2 on that page before reading the data columns.

Acceptance of Actually Stale Data: Conversely, the contract might accept price data as fresh based on its acceptedDelayTime criteria, even when the actual data is considered stale according to Chainlink's heartbeat intervals. This discrepancy can result in the execution of transactions based on outdated price information, exposing the protocol and its users to financial risks, including incorrect valuation of assets and vulnerability to exploitation.

In addition to that, it is advised to use different heartbeats and thus different intervals to check the staleness of each price feed

Missing check for Arbitrum L2 Sequencer: Also for Arbitrum, the Oracle must check whether the L2 Sequencer is down or not. 

For more details, refer- https://medium.com/cyfrin/chainlink-oracle-defi-attacks-93b6cb6541bf 

**Recommendation**: 

It is advised to follow the above 3 recommendations as stated:

Add a staleness price check for the Oracle prices. And use different heartbeats and different intervals to check staleness of price. It is advised to amend the Oracle contract to dynamically adjust its criteria for data freshness based on the heartbeat and deviation thresholds specific to each Chainlink Price Feed. This ensures that the contract's assessment of data freshness accurately reflects the intended update frequency and market conditions, as defined by Chainlink.

Check if L2 Sequencer is down or not for Arbitrum Oracles 
Note# : Recommendation 1 accepted, but as oracle.sol was originally decided to be deployed in bsc, l2 sequencer check was avoided 
Commit ID: 
09bc7206959dc780ce7bf4d02a2c280d36811940
