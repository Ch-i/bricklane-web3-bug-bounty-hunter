---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-0-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Deletion does not delete all values
vuln_class: []
---

# Deletion does not delete all values

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: High

**Status**: Resolved

**Description**

In LibQuorum.sol, the function `pruneQuorums()` can be problematic on line: 143 
```solidity
delete self.quorumSignatureSenders[h];
```
That's because `quorumSignatureSenders` is a mapping containing a struct which is containing a mapping. And deleting the outer mapping will not delete inner mapping contents. This could result in dangerous issues as it could lead to reuse of signatures or other undiscovered issues.

See: Openzeppelin EnumerableSet warning: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/structs/EnumerableSet.sol#L33

Crytic's Deletion bug: https://github.com/crytic/slither/wiki/Detector-Documentation#deletion-on-mapping-containing-a-structure

**Recommendation**: It is advised to clear the inner mappings properly to avoid any issues.

**Comments**: This issue was fixed in https://github.com/consensus-shipyard/ipc/pull/604
