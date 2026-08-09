---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-3-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Performance Concerns with Nested For Loop
vuln_class: []
---

# Performance Concerns with Nested For Loop

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: Informational

**Status**: Acknowledged

**Description**

LibQuorum.sol - In pruneQuorums function:
The smart contract includes a nested for loop structure, which, depending on the size of the data being processed, may result in increased gas costs. Nested loops can lead to a denial of service if the loops are large enough to hit the limit.
```solidity
   function pruneQuorums(QuorumMap storage self, uint256 newRetentionHeight) internal {
        ...
        for (uint256 h = oldRetentionHeight; h < newRetentionHeight; ) {
            ...
            for (uint256 i; i < n; ) {
                delete self.quorumSignatures[h][validators[i]];
                unchecked {
                    ++i;
                }
            }
            unchecked {
                ++h;
            }
        }
        self.retentionHeight = newRetentionHeight;
    }
```
**Recommendation**

To optimize performance and reduce gas consumption, it is recommended to review and refactor Loop Logic: Evaluate the necessity of the nested for loop structure and consider refactoring the logic to minimize computational complexity.
