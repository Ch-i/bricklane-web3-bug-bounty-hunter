---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-02-06-zunami-protocolv2-2-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-02-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md
tags:
- firm:oxorio
- report:2024-02-06-zunami-protocolv2
title: '[FIXED] Underflow in case of `depositedValue` is lower than `MINIMUM_LIQUIDITY`
  on the first deposit to the strategy in `ZunamiPool`'
vuln_class: []
---

# [FIXED] Underflow in case of `depositedValue` is lower than `MINIMUM_LIQUIDITY` on the first deposit to the strategy in `ZunamiPool`

_Section severity (from Solodit section header): Low_  
_Audit firm: Oxorio_  
_Source report: [2024-02-06-Zunami ProtocolV2.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[ZunamiPool.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/ZunamiPool.sol#L199 "/contracts/ZunamiPool.sol") | contract `ZunamiPool` > function `processSuccessfulDeposit` | 199

##### Description
In the `processSuccessfulDeposit` function of the `ZunamiPool` contract, there is a risk of underflow if `depositedValue` is less than `MINIMUM_LIQUIDITY` during the initial deposit to the strategy. This situation arises because the value of `minted` would be lower than `locked`, leading to an underflow error:
```solidity
if (totalSupply() == 0) {
	minted = depositedValue;
	locked = MINIMUM_LIQUIDITY;
	_mint(MINIMUM_LIQUIDITY_LOCKER, MINIMUM_LIQUIDITY);
} else {
	// ...
}
_mint(receiver, minted - locked);
```
##### Recommendation
We recommend implementing a validation check for the deposit size to ensure that the amount of tokens minted in the pool is not less than `MINIMUM_LIQUIDITY`.

##### Update
Fixed in commit [`9ffa8e1b6128d1ade8459a4e492cee669ed241a1`](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/9ffa8e1b6128d1ade8459a4e492cee669ed241a1/).
