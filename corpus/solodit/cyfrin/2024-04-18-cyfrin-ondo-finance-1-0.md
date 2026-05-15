---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: Consider implementing unlimited approvals for `rOUSG` token
vuln_class: []
---

# Consider implementing unlimited approvals for `rOUSG` token

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** ERC20 tokens commonly implement unlimited approvals by allowing users to approve spenders for `type(uint256).max`. Consider implementing this common feature; an [example](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol#L301-L311) from OpenZeppelin.

**Ondo:**
Acknowledged.
