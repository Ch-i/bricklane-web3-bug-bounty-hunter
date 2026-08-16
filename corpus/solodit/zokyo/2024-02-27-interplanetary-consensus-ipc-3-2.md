---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-3-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Unnecessary Default Safe Math Usage
vuln_class: []
---

# Unnecessary Default Safe Math Usage

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: Informational

**Status**: Acknowledged

**Description**

GatewayRouterFacet.sol - In `execBottomUpMsgBatch` function, the code snippet performs a subtraction operation on `subnet.circSupply` and `totalAmount` without the possibility of an underflow, as the preceding condition ensures subnet.circSupply is greater than or equal to `totalAmount`. The default safe math operation introduces unnecessary gas overhead, and the operation can be more gas-efficient by using the unchecked statement.
```solidity
       if (subnet.circSupply < totalAmount) {
            revert NotEnoughSubnetCircSupply();
        }

        subnet.circSupply -= totalAmount;
```
While the code snippet correctly ensures that the subtraction operation will not result in an underflow, the unnecessary default safe math usage can be optimized for gas efficiency. Wrapping the operation in an unchecked statement is a recommended practice for situations where the developer can guarantee that underflows will not occur. This enhancement contributes to more efficient gas utilization without compromising safety.

**Recommendation** 

Wrap Operation in unchecked Statement, given that the condition preceding the operation ensures there is no risk of underflow.
