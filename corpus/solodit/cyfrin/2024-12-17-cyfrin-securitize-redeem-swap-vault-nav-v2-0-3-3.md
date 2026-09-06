---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0-3-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0
title: Unused state variable in BaseSecuritizeSwap contract
vuln_class: []
---

# Unused state variable in BaseSecuritizeSwap contract

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md)_

---

**Description:** The `BaseSecuritizeSwap` contract contains an unused state variable `dsToken`. This variable is declared but never referenced in any function throughout the contract or its inheriting contracts. While this doesn't pose any security risks, it unnecessarily increases gas costs during deployment and may cause confusion for developers maintaining the codebase.

**Securitize:** Fixed in commit [ab46d0](https://bitbucket.org/securitize_dev/securitize-swap/commits/ab46d0e9be5184b0a4980a975f2afd68b33fa66b).

**Cyfrin:** Verified.


\clearpage
