---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-4-11
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: No helper functions for `maxDeposit`, `maxMint`, `maxRedeem`, `maxWithdraw`
  for `sUSDe`
vuln_class: []
---

# No helper functions for `maxDeposit`, `maxMint`, `maxRedeem`, `maxWithdraw` for `sUSDe`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** The Tranches allow deposits using `USDe` or `sUSDe`, but there aren't helper functions to calculate how much `sUSDe` an operation can be made with. The implemented functions only work for `USDe` amounts.

Specifically for withdrawing/redeeming `sUSDe`, it is not a straightforward process for a user to determine how much `sUSDe` they can request to be withdrawn.

The fact that the withdrawal flows for `USDe` or `sUSDe` vary considerably is mainly due to the unstaking time window for withdrawing USDe.

**Recommended Mitigation:** Consider adding helper functions to allow users to calculate max values when operating using `sUSDe`.
- Note: These functions don't need to be called anywhere in the code per se; they should just be available for a user to call them off-chain.

**Strata:**
Acknowledged; the user can use the `Strategy::convertToTokens`. To get "maxWithdraw" for sUSDe, the user calls the basic `maxWithdraw` to get amount in `USDe` and converts the value into `sUSDe` with `convertToTokens`. Later on we will extract those helper functions into additional "Lens" contract.

\clearpage
