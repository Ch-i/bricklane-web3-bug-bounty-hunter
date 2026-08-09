---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-1-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: Round up fees in `OUSGInstantManager::_getInstantMintFees` and `_getInstantRedemptionFees`
  to favor the protocol
vuln_class: []
---

# Round up fees in `OUSGInstantManager::_getInstantMintFees` and `_getInstantRedemptionFees` to favor the protocol

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** Solidity rounds down by default so consider explicitly rounding up fees in `OUSGInstantManager::_getInstantMintFees` and `_getInstantRedemptionFees` to favor the protocol.

**Ondo:**
Acknowledged.
