---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-07-18T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-18-cyfrin-securitize-redemptions-v2-0
title: No validation check of `_investorWallet` when buying `dsToken`.
vuln_class: []
---

# No validation check of `_investorWallet` when buying `dsToken`.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-18-cyfrin-securitize-redemptions-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md)_

---

**Description:** In the `SecuritizeSwap.buy()` function, there is no validation check to verify if `_investorWallet` has already been added to the wallet list of `_senderInvestorId`, unlike in the `swap()` function. Consequently, users can purchase `dsToken` using wallets that have not been added.

The following code snippet demonstrates the wallet validation part within the `swap()` function. It first verifies if the wallet has already been added. If the wallet hasn't been added, it adds the wallet. If the wallet has already been added, it verifies if the wallet belongs to the investor. However, the `buy()` function does not include these steps.

```solidity
    File: securitize_dev-securitize-swap-47704357c2da\contracts\swap\SecuritizeSwap.sol

88:         //Check if new wallet should be added
89:         string memory investorWithNewWallet = IDSRegistryService(dsToken.getDSService(DS_REGISTRY_SERVICE)).getInvestor(_newInvestorWallet);
90:         if(CommonUtils.isEmptyString(investorWithNewWallet)) {
91:             IDSRegistryService(dsToken.getDSService(DS_REGISTRY_SERVICE)).addWallet(_newInvestorWallet, _senderInvestorId);
92:         } else {
93:             require(CommonUtils.isEqualString(_senderInvestorId, investorWithNewWallet), "Wallet does not belong to investor");
94:         }
```

**Impact:** Users can buy `dsToken` using wallets that have not been added.

**Recommended Mitigation:** A validation check for the wallet should be included in the `buy()` function.

**Securitize:** Fixed in commit [b09460](https://bitbucket.org/securitize_dev/securitize-swap/commits/b094604b341123a49c8abbd6e1c3d53d7c102f28)

**Cyfrin:** Verified.
