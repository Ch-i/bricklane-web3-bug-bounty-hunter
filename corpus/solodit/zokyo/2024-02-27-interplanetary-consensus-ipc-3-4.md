---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-3-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Unnecessary Default Safe Math Usage - 3
vuln_class: []
---

# Unnecessary Default Safe Math Usage - 3

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: Informational

**Status**: Acknowledged

**Description**

SubnetActionManagerFacet.sol - In `preRelease` function, the code snippet performs a subtraction operation on `s.genesisbalance[msg.sender]` and amount without the possibility of an underflow, as the preceding condition ensures `s.genesisbalance[msg.sender]` is greater than or equal to amount. The default safe math operation introduces unnecessary gas overhead, and the operation can be more gas-efficient by using the unchecked statement.

```solidity
   function preRelease(uint256 amount) external nonReentrant {
        ...
        if (s.genesisBalance[msg.sender] < amount) {
            revert NotEnoughBalance();
        }

        s.genesisbalance[msg.sender] -= amount;
        ...
    }
```
While the code snippet correctly ensures that the subtraction operation will not result in an underflow, the unnecessary default safe math usage can be optimized for gas efficiency. Wrapping the operation in an unchecked statement is a recommended practice for situations where the developer can guarantee that underflows will not occur. This enhancement contributes to more efficient gas utilization without compromising safety.

**Recommendation**

Wrap Operation in unchecked Statement, given that the condition preceding the operation ensures there is no risk of underflow.
