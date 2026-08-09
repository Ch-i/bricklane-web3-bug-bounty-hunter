---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-31-cyfrin-linea-tokens-v2-3-0-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-31T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-31-cyfrin-linea-tokens-v2.3.md
tags:
- firm:cyfrin
- report:2025-07-31-cyfrin-linea-tokens-v2-3
title: Parameter name mismatch between L2LineaToken interface and implementation
vuln_class: []
---

# Parameter name mismatch between L2LineaToken interface and implementation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-31-cyfrin-linea-tokens-v2.3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-31-cyfrin-linea-tokens-v2.3.md)_

---

**Description:** There is a discrepancy in parameter naming between the [`IL2LineaToken::syncTotalSupplyFromL1`](https://github.com/Consensys/audit-2025-07-linea-tokens/blob/44640f0965a5c7465b99769a5d241a9a1cb3a2ef/src/L2/interfaces/IL2LineaToken.sol#L38) interface and its implementation, [`L2LineaToken::syncTotalSupplyFromL1`](https://github.com/Consensys/audit-2025-07-linea-tokens/blob/44640f0965a5c7465b99769a5d241a9a1cb3a2ef/src/L2/L2LineaToken.sol#L104). The interface uses the names (`_l1BlockTimestamp`, `_l1TotalSupply`), whereas the implementation employs more verbose names (`_l1LineaTokenTotalSupplySyncTime`, `_l1LineaTokenSupply`) that mirror the contract’s state variables. This mismatch in wording can lead to confusion when reading documentation or generating bindings, even though the ABI remains compatible.

Consider using `_l1LineaTokenTotalSupplySyncTime` and `_l1LineaTokenSupply` in both the interface and its NatSpec comments so they align with the implementation’s state fields and maintain clear, consistent documentation.


**Linea:** Fixed in [PR#17](https://github.com/Consensys/linea-tokens/pull/17), commit [`1296069`](https://github.com/Consensys/linea-tokens/pull/17/commits/1296069ed398e72d9a57f71a02b2ee93fbbc5e47)

**Cyfrin:** Verified. Parameters now renamed in interface and corresponding nat-spec.
