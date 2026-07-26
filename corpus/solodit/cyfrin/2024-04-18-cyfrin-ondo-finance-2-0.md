---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-2-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: Cache array length outside of loops and consider unchecked loop incrementing
vuln_class: []
---

# Cache array length outside of loops and consider unchecked loop incrementing

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** Cache array length outside of loops and consider using `unchecked {++i;}` if not compiling with `solc --ir-optimized --optimize`:
```solidity
File: contracts/ousg/InvestorBasedRateLimiter.sol

253:     for (uint256 i = 0; i < addresses.length; ++i) {
```

```solidity
File: contracts/ousg/ousgInstantManager.sol

881:     for (uint256 i = 0; i < exCallData.length; ++i) {
```

**Ondo:**
Acknowledged.
