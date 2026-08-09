---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: Precision loss in `swETH::reprice` from unnecessary division before multiplication
vuln_class: []
---

# Precision loss in `swETH::reprice` from unnecessary division before multiplication

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** `swETH::reprice` [L281-286](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swETH.sol#L281-L286) performs unnecessary [division before multiplication](https://dacian.me/precision-loss-errors#heading-division-before-multiplication) when calculating node operator rewards which negatively impacts node operator rewards due to precision loss:

```solidity
UD60x18 nodeOperatorRewardPortion = wrap(nodeOperatorRewardPercentage)
  .div(wrap(rewardPercentageTotal));

nodeOperatorRewards = nodeOperatorRewardPortion
  .mul(rewardsInSwETH) // @audit mult after division
  .unwrap();
```

Refactor to perform division after multiplication:

```solidity
nodeOperatorRewards = wrap(nodeOperatorRewardPercentage)
  .mul(rewardsInSwETH)
  .div(wrap(rewardPercentageTotal))
  .unwrap();
```

A similar issue occurs when calculating operators reward share [L310-313](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swETH.sol#L310-L313):

```solidity
uint256 operatorsRewardShare = wrap(operatorActiveValidators)
  .div(totalActiveValidators)
  .mul(wrap(nodeOperatorRewards)) // @audit mult after division
  .unwrap();
```

This can be similarly refactored to prevent the precision loss by performing multiplication first:

```solidity
uint256 operatorsRewardShare = wrap(operatorActiveValidators)
  .mul(wrap(nodeOperatorRewards))
  .div(totalActiveValidators)
  .unwrap();
```

This issue has not been introduced in the new changes but is in the mainnet code ([1](https://github.com/SwellNetwork/v3-core-public/blob/master/contracts/lst/contracts/implementations/swETH.sol#L267-L272), [2](https://github.com/SwellNetwork/v3-core-public/blob/master/contracts/lst/contracts/implementations/swETH.sol#L296-L299)).

There is still one potential precision loss remaining as `rewardsInSwETH` which has had a [division performed](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swETH.sol#L239) then gets [multiplied](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swETH.sol#L285) but attempting to refactor this out resulted in a "stack too deep" error so it may be unavoidable.

**Swell:** Acknowledged.
