---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-2-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Gas Optimization
vuln_class: []
---

# Gas Optimization

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Informational

**Status**: Unresolved

Under the hood of solidity, Booleans (bool) are uint8, which means they use 8 bits of storage. A Boolean can only have two values: True or False. This means that you can store a boolean in only a single bit.
https://github.com/zokyo-sec/audit-struct-finance-1/blob/audit/zokyo-feb-2023/contracts/protocol/common/GACManaged.sol#L30

**Recommendation** : 

Change the uint8 to uint256 to save gas
