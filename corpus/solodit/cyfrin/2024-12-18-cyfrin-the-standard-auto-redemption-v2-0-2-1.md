---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: Additional validation should be performed on the Chainlink Functions response
vuln_class: []
---

# Additional validation should be performed on the Chainlink Functions response

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** When consuming a Chainlink Functions response, the following additional validation should be performed within `AutoRedemption::fulfillRequest`:
* Ensure the `_token` address is either a Hypervisor with valid data on the `SmartVaultYieldManager` contract (valid only for non-legacy vaults) or an accepted collateral token.
* Ensure the `_tokenID` has actually been minted such that `SmartVaultManagerV6::vaultData` will return a non-default `SmartVaultData` struct.

**The Standard DAO**
Fixed by commit [8ee0921](https://github.com/the-standard/smart-vault/commit/8ee0921026b5a56c0d441f3e87d5530506b7e445).

**Cyfrin:** Verified. `AutoRedemption::validData` has been added to verify that the vault address is non-zero and the token is a valid collateral token.

\clearpage
