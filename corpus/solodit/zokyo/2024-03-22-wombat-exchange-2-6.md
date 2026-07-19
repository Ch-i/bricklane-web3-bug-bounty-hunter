---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-22-wombat-exchange-2-6
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-03-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md
tags:
- firm:zokyo
- report:2024-03-22-wombat-exchange
title: Unused constants
vuln_class: []
---

# Unused constants

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-03-22-Wombat Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**


In the library RepegHelper, the following constant is unused.

```solidity
   int256 private constant WAD_I = 10 ** 18;
```

**Recommendation**: 

Remove the unused constant.
