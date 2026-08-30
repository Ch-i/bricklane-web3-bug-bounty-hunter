---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-3-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Unnecessary Default Safe Math Usage - 2
vuln_class: []
---

# Unnecessary Default Safe Math Usage - 2

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: Informational

**Status**: Acknowledged

**Description**

GatewayRouterFacet.sol - In `recordWithdraw` function, the code snippet performs a subtraction operation on total and amount without the possibility of an underflow, as the preceding condition ensures total is greater than or equal to amount. The default safe math operation introduces unnecessary gas overhead, and the operation can be more gas-efficient by using the unchecked statement.
```solidity
   function recordWithdraw(ValidatorSet storage validators, address validator, uint256 amount) internal {
        uint256 total = validators.validators[validator].totalCollateral;
        if (total < amount) {
            revert WithdrawExceedingCollateral();
        }

        total -= amount;
        validators.validators[validator].totalCollateral = total;
    }
```
While the code snippet correctly ensures that the subtraction operation will not result in an underflow, the unnecessary default safe math usage can be optimized for gas efficiency. Wrapping the operation in an unchecked statement is a recommended practice for situations where the developer can guarantee that underflows will not occur. This enhancement contributes to more efficient gas utilization without compromising safety.

**Recommendation**

Wrap Operation in unchecked Statement, given that the condition preceding the operation ensures there is no risk of underflow.
