---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-2-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-09-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-25-cyfrin-button-basis-trade-v2-0
title: Missing minimum deposit enforcement
vuln_class: []
---

# Missing minimum deposit enforcement

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-25-cyfrin-button-basis-trade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md)_

---

**Description:** The `BasisTradeVault::deposit` function does not enforce a minimum deposit amount. Allowing dust deposits can lead to several undesirable situations:

1.  **Economic Unviability:** A user might deposit an amount so small that the gas fees for the transaction are significantly higher than the value of the deposit itself.

2.  **Potential for Nuisance:** It could enable scenarios where an attacker spams the vault with many tiny deposits, which, while not a direct security threat, can be a nuisance.

Although the contract is protected from the most severe issues by the base ERC4626 implementation, enforcing a sensible minimum deposit amount is a good practice for user protection and contract robustness.

**Recommended Mitigation:** Introduce a new state variable, `minDepositAmount`, which can be set by an admin. Modify the `deposit` function to require that the deposited `assets` are greater than or equal to this minimum amount.

**Button:** Fixed in commit [`9cde24c`](https://github.com/buttonxyz/button-protocol/commit/9cde24caa4b3f5f37a059bb2fde172cfa374d3a9).

**Cyfrin:** Verified. A minimum deposit configurable by admin is now enforced
