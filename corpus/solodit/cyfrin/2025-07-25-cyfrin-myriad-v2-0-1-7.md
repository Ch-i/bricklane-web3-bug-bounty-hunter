---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-25-cyfrin-myriad-v2-0-1-7
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-25-cyfrin-myriad-v2-0
title: Unnecessary transfer in `PredictionMarketV3_4::mintAndCreateMarket`
vuln_class: []
---

# Unnecessary transfer in `PredictionMarketV3_4::mintAndCreateMarket`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-25-cyfrin-myriad-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md)_

---

**Description:** [`PredictionMarketV3_4::mintAndCreateMarket`](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/contracts/PredictionMarketV3_4.sol#L381-L390) does a mint of `FantasyERC20` to the user then a transfer to the contract:
```solidity
function mintAndCreateMarket(CreateMarketDescription calldata desc) external nonReentrant returns (uint256 marketId) {
  // mint the amount of tokens to the user
  IFantasyERC20(address(desc.token)).mint(msg.sender, desc.value);

  marketId = _createMarket(desc);
  // transferring funds
  desc.token.safeTransferFrom(msg.sender, address(this), desc.value);

  return marketId;
}
```
The issue is that the second transfer is unnecessary as first `desc.value` is minted to the user, then `desc.value` is transferred to the contract. Consider simplifying this to:
```solidity
function mintAndCreateMarket(CreateMarketDescription calldata desc) external nonReentrant returns (uint256 marketId) {
  // mint the amount of tokens to the user
  IFantasyERC20(address(desc.token)).mint(address(this), desc.value);

  return _createMarket(desc);
}
```
This saves a transfer and doesn't require the user to approve the contract to spend `FantasyERC20` tokens.

**Myriad:** Fixed in [PR#86](https://github.com/Polkamarkets/polkamarkets-js/pull/86), commit [`ba955d8`](https://github.com/Polkamarkets/polkamarkets-js/pull/86/commits/ba955d84cfc73bd41743c9e21ffea151f629c012)

**Cyfrin:** Verified. Mint is now done directly to the contract and transfer removed.
