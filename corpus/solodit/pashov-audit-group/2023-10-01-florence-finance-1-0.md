---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-10-01-florence-finance-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-10-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-10-01-Florence%20Finance.md
tags:
- firm:pashov-audit-group
- report:2023-10-01-florence-finance
title: '[L-01] Missing Arbitrum Sequencer availability check'
vuln_class: []
---

# [L-01] Missing Arbitrum Sequencer availability check

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-10-01-Florence Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-10-01-Florence%20Finance.md)_

---

The `getFundingTokenExchangeRate` method in `LoanVault` makes use of Chainlink price feeds by calling the `latestRoundData` method. While there are sufficient validations for the price feed answer, a check is missing for the L2 sequencer availability which has to be there since the protocol is moving from Ethereum to Arbitrum. In case the L2 Sequencer is unavailable the protocol will be operating with a stale price and also when the sequencer is back up then all of queued transactions will be executed on Arbitrum before new ones can be done. This can result in the `LoanVault::getFundingTokenExchangeRate` using a stale price, which means that a user might receive more or less shares from the `LoanVault` than he should have had. Still, since all of the funding requests are first approved off-chain, the probability of this happening is much lower. For a fix you can follow the [Chainlink docs](https://docs.chain.link/data-feeds/l2-sequencer-feeds) to add a check for sequencer availability.
