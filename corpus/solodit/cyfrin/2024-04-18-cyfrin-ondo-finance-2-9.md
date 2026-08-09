---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-2-9
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: Change `ROUSG::unwrap` to return amount of `OUSG` output tokens then use that
  as input when calling `_redeem` in `OUSGInstantManager::redeemRebasingOUSG`
vuln_class: []
---

# Change `ROUSG::unwrap` to return amount of `OUSG` output tokens then use that as input when calling `_redeem` in `OUSGInstantManager::redeemRebasingOUSG`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** Change `ROUSG::unwrap` to return amount of `OUSG` output tokens then use that as input when calling `_redeem` in `OUSGInstantManager::redeemRebasingOUSG`:
```solidity
uint256 ousgAmountIn = rousg.unwrap(rousgAmountIn);

usdcAmountOut = _redeem(ousgAmountIn);
```

**Ondo:**
Acknowledged.

\clearpage
