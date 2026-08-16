---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-22
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: '`RegistryService::addWallet` should revert if the wallet being added has positive
  balance of `DSToken`'
vuln_class: []
---

# `RegistryService::addWallet` should revert if the wallet being added has positive balance of `DSToken`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `RegistryService::addWallet` doesn't update investor wallet or total balances if it is used to add a wallet that already has a positive `DSToken` balance.

Using it to add a wallet with a positive balance results in a number of incorrect states:

#### Compliance Validation Problems ####
* Investor might not be counted in total investors
* Won't trigger investor limit checks
* Could bypass US/EU investor limits

#### Transfer Validation Problems ####
* Compliance checks expect investor balance to match wallet balance
* Some checks compare investor balance to transfer amount
* Could trigger incorrect "new investor" logic
* Transfers could revert due to underflow when subtracting from existing internal wallet / investor balances resulting in the tokens being stuck

**Recommended Mitigation:** `RegistryService::addWallet` should revert if the wallet being added has positive balance of `DSToken`. The same applies to `addWalletByInvestor` but that function is being removed.

Alternatively another option is to register the existing tokens for the investor by calling `DSToken::updateInvestorBalance` and `addWalletToList` though these functions are currently private.

**Securitize:** Fixed in commit [3e9c754](https://github.com/securitize-io/dstoken/commit/3e9c754c6e11866884457cedfa46dd55d5b6bc2a) by preventing adding wallets with positive balance.

**Cyfrin:** Verified.

\clearpage
