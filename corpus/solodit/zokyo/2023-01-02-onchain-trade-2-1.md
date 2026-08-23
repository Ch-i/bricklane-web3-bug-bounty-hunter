---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-01-02-onchain-trade-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-01-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md
tags:
- firm:zokyo
- report:2023-01-02-onchain-trade
title: Remove hardhat console imports from the code
vuln_class: []
---

# Remove hardhat console imports from the code

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-01-02-Onchain Trade.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md)_

---

**Severity**: Informational

**Status**: Unresolved

**Description**

In contracts Swap.sol and VariableBorrow.sol the hardhat/console.sol library is imported and never used. 

**Recommendation**: 

Remove all occurrences of hardhat/console.sol imports from production code
