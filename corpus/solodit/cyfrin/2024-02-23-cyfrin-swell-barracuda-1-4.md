---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-1-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: '`swETH::reprice` may run out of gas or become exorbitantly expensive when
  scaling to large number of validator operators due to iterating over them all'
vuln_class: []
---

# `swETH::reprice` may run out of gas or become exorbitantly expensive when scaling to large number of validator operators due to iterating over them all

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** `swETH::reprice` [loops](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swETH.sol#L303-L321) through all validator operators to pay out their share of rewards:
```solidity
// @audit may run out of gas for larger number of validator operators
// or make repricing exorbitantly expensive
for (uint128 i = 1; i <= totalOperators; ) {
  (
    address rewardAddress,
    uint256 operatorActiveValidators
  ) = nodeOperatorRegistry.getRewardDetailsForOperatorId(i);

  if (operatorActiveValidators != 0) {
    uint256 operatorsRewardShare = wrap(operatorActiveValidators)
      .div(totalActiveValidators)
      .mul(wrap(nodeOperatorRewards))
      .unwrap();

    _transfer(address(this), rewardAddress, operatorsRewardShare);
  }

  // Will never overflow as the total operators are capped at uint128
  unchecked {
    ++i;
  }
}
```
If Swell scales to a large number of validators `swETH::reprice` may revert due to out of gas or make the reprice operation exorbitantly expensive. `NodeOperatorRegistry::getNextValidatorDetails` may be similarly [affected](https://github.com/SwellNetwork/v3-contracts-lst/blob/c9a1e6c06d0f5b358f5c3d4b7644db7a33952444/contracts/implementations/NodeOperatorRegistry.sol#L117-L125).

Currently this represents a low risk for Swell as the protocol uses a small set of ["permissioned group of professional node operators"](https://docs.swellnetwork.io/swell/sweth-liquid-staking/sweth-v1.0-system-design/node-operators-set).

However Swell intends to [transition away from](https://docs.swellnetwork.io/swell/sweth-liquid-staking/sweth-v1.0-system-design/node-operators-set) this: _"The subsequent iterations will see the operator set **expand** and ultimately be permissionless.."_

As Swell expands the operator set this issue will become a more serious concern and may require mitigation.

**Swell:** Acknowledged.
