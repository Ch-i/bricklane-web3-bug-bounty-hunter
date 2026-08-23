---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-3-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-07-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-18-cyfrin-securitize-redemptions-v2-0
title: Missing slippage control for investors during the buy
vuln_class: []
---

# Missing slippage control for investors during the buy

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-18-cyfrin-securitize-redemptions-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md)_

---

**Description:** The protocol allows investors to buy `dsToken` with `stableCoinToken` using the function `SecuritizeSwap::buy()`.
The function calculates the amount of `dsToken` to send to the caller based on the `navProvider.rate()` and there is no way for an investor to predict what rate will be applied to his purchase.

```solidity
SecuritizeSwap.sol
104:     function buy(
105:         string memory _senderInvestorId,
106:         address _investorWallet,
107:         uint256 _stableCoinAmount,
108:         uint256 _blockLimit,
109:         uint256 _issuanceTime
110:     ) public override whenNotPaused {
111:         require(_blockLimit >= block.number, "Transaction too old");//@audit-ok
112:         require(stableCoinToken.balanceOf(_investorWallet) >= _stableCoinAmount, "Not enough stable tokens balance");
113:         require(IDSRegistryService(dsToken.getDSService(DS_REGISTRY_SERVICE)).isInvestor(_senderInvestorId), "Investor not registered");
114:         require(navProvider.rate() > 0, "NAV Rate must be greater than 0");
115:         (uint256 dsTokenAmount, uint256 currentNavRate) = calculateDsTokenAmount(_stableCoinAmount);
116:         stableCoinToken.transferFrom(_investorWallet, issuerWallet, _stableCoinAmount);
117:
118:         dsToken.issueTokensCustom(_investorWallet, dsTokenAmount, _issuanceTime, 0, "", 0);//@audit-issue missing protection against change in the NAV rate
119:
120:         emit Buy(msg.sender, _stableCoinAmount, dsTokenAmount, currentNavRate, _investorWallet);
121:     }
122:
```
If the `navProvider.rate()` is changed during a specific timeframe by whatever reason, the investors do not have other ways but to accept the loss due to the rate change.

**Recommended Mitigation:** Add a parameter `_minDsTokenAmount` in the function so that the caller can specify the minimum expected amount.
It is also recommended to make the function `calculateDsTokenAmount()` public so that users can anticipate the receiving amounts beforehand.

**Securitize:** Fixed in commit [b09460](https://bitbucket.org/securitize_dev/securitize-swap/commits/b094604b341123a49c8abbd6e1c3d53d7c102f28).
We modified the definition of the buy function so that the `dsTokenAmount` is fixed, and the liquidity tokens vary according to the NAV rate.
We also added the parameter `_maxStableCoinAmount` to prevent price changes with sudden variations.

**Cyfrin:** Verified.
