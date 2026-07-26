---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-0-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-07-18T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-18-cyfrin-securitize-redemptions-v2-0
title: Missing validation on the `msg.sender` in `SecuritizeSwap::buy` function
vuln_class: []
---

# Missing validation on the `msg.sender` in `SecuritizeSwap::buy` function

_Section severity (from Solodit section header): Critical_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-18-cyfrin-securitize-redemptions-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md)_

---

**Description:** The function `SecuritizeSwap::buy` is supposed to be used by investors to swap `stableCoinToken` for `dsToken` and the key difference from the function `SecuritizeSwap::swap` is that `buy` can be called by anyone while the `swap` function can only be called by `Issuer` or `Master`.
The problem is the function `buy()` does not validate if the caller is actually the investor of `_senderInvestorId`.
```solidity
SecuritizeSwap.sol
104:     function buy(//@audit-info public call that investors can directly call
105:         string memory _senderInvestorId,
106:         address _investorWallet,
107:         uint256 _stableCoinAmount,
108:         uint256 _blockLimit,
109:         uint256 _issuanceTime
110:     ) public override whenNotPaused {
111:         require(_blockLimit >= block.number, "Transaction too old");
112:         require(stableCoinToken.balanceOf(_investorWallet) >= _stableCoinAmount, "Not enough stable tokens balance");
113:         require(IDSRegistryService(dsToken.getDSService(DS_REGISTRY_SERVICE)).isInvestor(_senderInvestorId), "Investor not registered");
114:         require(navProvider.rate() > 0, "NAV Rate must be greater than 0");
115:         (uint256 dsTokenAmount, uint256 currentNavRate) = calculateDsTokenAmount(_stableCoinAmount);
116:         stableCoinToken.transferFrom(_investorWallet, issuerWallet, _stableCoinAmount);
117:
118:         dsToken.issueTokensCustom(_investorWallet, dsTokenAmount, _issuanceTime, 0, "", 0);
119:
120:         emit Buy(msg.sender, _stableCoinAmount, dsTokenAmount, currentNavRate, _investorWallet);
121:     }

```
As we can see in the implementation, the function only checks if the provided `_senderInvestorId` is actually registered and do not check if the `msg.sender` is an investor assigned to that ID.
This vulnerability allows anyone to force any investor to buy `dsToken` with `stableCoinToken` as long as the investor granted allowance to the `SecuritizeSwap` contract.

**Impact:** We evaluate the impact to be CRITICAL because anyone can change the investors economical status at the will.

**Recommended Mitigation:** Validate the `msg.sender` to be an actual investor utilizing the registry service.

**Securitize:** Fixed in commit [b09460](https://bitbucket.org/securitize_dev/securitize-swap/commits/b094604b341123a49c8abbd6e1c3d53d7c102f28)

**Cyfrin:** Verified.

\clearpage
