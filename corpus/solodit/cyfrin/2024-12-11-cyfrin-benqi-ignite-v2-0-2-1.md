---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Insufficient validation of Chainlink price feeds
vuln_class: []
---

# Insufficient validation of Chainlink price feeds

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** Validation of the `price` and `updatedAt` values returned by Chainlink `AggregatorV3Interface::latestRoundData` is performed within the following functions:
- [`StakingContract::_validateAndSetPriceFeed`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L923-925)
- [`StakingContract::_getPriceInUSD`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L937-943)
- [`Ignite::_initialisePriceFeeds`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L187-L189)
- [`Ignite::registerWithStake`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L218-L223)
- [`Ignite::registerWithErc20Fee`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L291-L296)
- [`Ignite::registerWithPrevalidatedQiStake`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L373-L378)
- [`Ignite::addPaymentToken`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L806-L808)
- [`Ignite::configurePriceFeed`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L856-L858)

However, there is additional validation shown below that is recommended but currently not present:

```solidity
(uint80 roundId, int256 price, , uint256 updatedAt, ) = priceFeed.latestRoundData();
if(roundId == 0) revert InvalidRoundId();
if(updatedAt == 0 || updatedAt > block.timestamp) revert InvalidUpdate();
```

**Impact:** The impact is limited because the most important price and staleness validation are already present.

**Recommended Mitigation:** Consider including this additional validation and consolidating it into a single internal function.

**BENQI:** Acknowledged, current validation is deemed sufficient.

**Cyfrin:** Acknowledged.
