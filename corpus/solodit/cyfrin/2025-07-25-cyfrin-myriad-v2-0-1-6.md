---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-25-cyfrin-myriad-v2-0-1-6
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-07-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-25-cyfrin-myriad-v2-0
title: '"Weight" and `poolWeight` serves different meanings throughout the code/documentation'
vuln_class: []
---

# "Weight" and `poolWeight` serves different meanings throughout the code/documentation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-25-cyfrin-myriad-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md)_

---

**Description:** The concept weight/variable `poolWeight` is used in multiple places throughout the contract, serving three distinct purposes, which may lead to confusion:

1. In [`PredictionMarketV3_4::addLiquidity`](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/contracts/PredictionMarketV3_4.sol#L630) and [`PredictionMarketV3_4::removeLiquidity`](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/contracts/PredictionMarketV3_4.sol#L751), it represents the minimum or maximum number of outcome shares in the pool.
2. It is also used in [`MarketFees.poolWeight`](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/contracts/PredictionMarketV3_4.sol#L151) as a fee accumulator
3. In the [documentation](https://help.polkamarkets.com/how-polkamarkets-works/trading-and-price-calculation#6ec9ef9b0b8d4b61991c86d35936c4c3) "weight" is used to represent the product of share outcomes.

Using a single variable name (`poolWeight`) for multiple, semantically different roles can lead to misunderstandings for developers, auditors, and integrators. Also mixing the meaning of the word "weight" in the context of the code obscures the intent behind the logic and may cause misinterpretation of core mechanics like fee behavior, share distribution, or price computation.

Consider separating these concerns by using more specific and descriptive variable names for each use case. For example:

* Use `minOutcomeShares` or `baseShares` for liquidity operations
* Use `feeAccumulator` for fee tracking
* Use `priceWeightProduct` or similar for price-related math

This will improve readability and reduce the cognitive load for maintainers and users of the contract.

**Myriad:** Fixed in [PR#82](https://github.com/Polkamarkets/polkamarkets-js/pull/82), commit [`d30be85`](https://github.com/Polkamarkets/polkamarkets-js/pull/82/commits/d30be8566ea49885582f3caa1a2669c948cc4962)

**Cyfrin:** Verified. `poolWeight` in `MarketFees` renamed to `feeAccumulator` and variable `poolWeight` renamed to `baseShares`.
