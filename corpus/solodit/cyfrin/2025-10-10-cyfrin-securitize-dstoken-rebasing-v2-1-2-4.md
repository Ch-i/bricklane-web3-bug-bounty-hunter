---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Missing `checkWalletsForList` in `issueTokensWithNoCompliance`
vuln_class: []
---

# Missing `checkWalletsForList` in `issueTokensWithNoCompliance`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** The `issueTokensWithNoCompliance` function in `DSToken.sol` fails to call `checkWalletsForList(address(0), _to)` after token issuance, unlike all other issuance functions. This prevents wallets from being added to the contract's internal enumeration list used for administrative operations.

**Impact:** * `walletCount()` returns incorrect values and `getWalletAt()` cannot retrieve wallets that received tokens via no-compliance issuance
* Failed Bulk Operations: Any administrative function relying on wallet enumeration will miss these token holders


**Recommended Mitigation:** Add the `checkWalletsForList`  in ` issueTokensWithNoCompliance`

**Securitize:** `DSToken:: issueTokensWithNoCompliance` was removed.

**Cyfrin:** Verified.
