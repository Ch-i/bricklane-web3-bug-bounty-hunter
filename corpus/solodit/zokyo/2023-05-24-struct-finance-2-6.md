---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-2-6
ingested_at: '2026-08-16T05:02:10Z'
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

Change the order of external contract call in _gacPausable function in GACManaged.sol
By swapping the order of the require statements, the local pause check will be performed first, which does not require an external contract call. If it fails, the function will revert immediately, saving the gas cost of the external contract call. Only if the local pause check passes, the global pause check will be executed.
https://github.com/zokyo-sec/audit-struct-finance-1/blob/audit/zokyo-feb-2023/contracts/protocol/common/GACManaged.sol#L85

**Recommendation** :

Change to this :
```solidity
function _gacPausable() private view {
    require(!paused(), Errors.ACE_LOCAL_PAUSED);
    require(!gac.paused(), Errors.ACE_GLOBAL_PAUSED);
}
```
This way, the local pause check will be performed first, and if it fails, the function will revert immediately without incurring the gas cost of the external contract call. If the local pause check passes, only then the global pause check will be executed
