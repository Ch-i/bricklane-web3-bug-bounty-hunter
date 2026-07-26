---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-28-cyfrin-yieldfi-pr19-v2-0-0-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-05-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-28-cyfrin-yieldfi_pr19-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-28-cyfrin-yieldfi-pr19-v2-0
title: Redundant `virtual` declaration in` YToken::_withdraw`
vuln_class: []
---

# Redundant `virtual` declaration in` YToken::_withdraw`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-28-cyfrin-yieldfi_pr19-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-28-cyfrin-yieldfi_pr19-v2.0.md)_

---

**Description:** In the [pull request](https://github.com/YieldFiLabs/contracts/pull/19), the function [`YToken::_withdraw`](https://github.com/YieldFiLabs/contracts/blob/702a931df3adb2f6e48807203cdc7a92604ea249/contracts/core/tokens/YToken.sol#L193) was updated to be declared `virtual`, allowing it to be overridden in derived contracts. However, it is never actually overridden in any of the `dYToken` implementations.

Consider removing the `virtual` modifier from both `YToken::_withdraw` and `YTokenL2::_withdraw` to clarify intent and avoid misleading extensibility.

**YieldFi:** Acknowledged.

\clearpage
