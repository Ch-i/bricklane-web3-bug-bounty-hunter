---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-0-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: '`SwellLib.BOT` can subtly rug-pull withdrawals by setting `_processedRate
  = 0` when calling `swEXIT::processWithdrawals`'
vuln_class: []
---

# `SwellLib.BOT` can subtly rug-pull withdrawals by setting `_processedRate = 0` when calling `swEXIT::processWithdrawals`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** When users create a withdrawal request, their `swETH` is [burned](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swEXIT.sol#L202-L205) then the current exchange rate `rateWhenCreated` is [fetched](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swEXIT.sol#L213) from `swETH::swETHToETHRate`:
```solidity
uint256 rateWhenCreated = AccessControlManager.swETH().swETHToETHRate();
```

However `SwellLib.BOT` can [pass an arbitrary value](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swEXIT.sol#L111) for `_processedRate` when calling `swEXIT::processWithdrawals`:
```solidity
function processWithdrawals(
  uint256 _lastTokenIdToProcess,
  uint256 _processedRate
) external override checkRole(SwellLib.BOT) {
```

The [final rate](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swEXIT.sol#L150-L152) used is the lesser of `rateWhenCreated` and `_processedRate`:
```solidity
uint256 finalRate = _processedRate > rateWhenCreated
  ? rateWhenCreated
  : _processedRate;
```

This final rate is [multiplied](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swEXIT.sol#L158) by the requested withdrawal amount to determine the actual amount sent to the user requesting a withdrawal:
```solidity
uint256 requestExitedETH = wrap(amount).mul(wrap(finalRate)).unwrap();
```

Hence `SwellLib.BOT` can subtly rug-pull all withdrawals by setting `_processedRate = 0` when calling `swEXIT::processWithdrawals`.

**Recommended Mitigation:** Two possible mitigations:
1) Change `swEXIT::processWithdrawals` to always fetch the current rate from `swETH::swETHToETHRate`
2) Only allow `swEXIT::processWithdrawals` to be called by the `RepricingOracle` contract which [calls it correctly](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/RepricingOracle.sol#L130-L132).

**Swell:** Fixed in commits [c6f8708](https://github.com/SwellNetwork/v3-contracts-lst/commit/c6f870847bdf276aee1bf9aeb1ed71771a2aba04), [64cfbdb](https://github.com/SwellNetwork/v3-contracts-lst/commit/64cfbdbf67e28d84f2a706982e28925ab51fd5e6).

**Cyfrin:**
Verified.

\clearpage
