---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Potential Inconsistency in Handling `powerScale` in `SubnetActorDiamond.sol`
  Constructor
vuln_class: []
---

# Potential Inconsistency in Handling `powerScale` in `SubnetActorDiamond.sol` Constructor

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: Low 

**Status**: Acknowledged 

**Location**: SubnetActorDiamond.sol contract, Constructor

**Description**

The constructor of the `SubnetActorDiamond.sol` contract allows for the setting of a `powerScale` parameter of type int8. There is a check in place to ensure that `powerScale` does not exceed 18. However, there is no corresponding check for the lower bound, particularly for negative values. Given that `powerScale` is of type int8, it can hold negative values, which might lead to unintended behavior or inconsistencies in the contract's logic if the contract allows a large negative value.
**Issue Details**:
Type of powerScale: The variable `powerScale` is of type int8, which allows for negative values.
Lack of Lower Bound Check: The current implementation only checks if powerScale is greater than 18 and does not account for negative values.
Potential Unintended Behavior: Without a lower bound check, large negative values of powerScale might lead to unexpected behavior, depending on how powerScale is used in the contract.

**Recommendation**: 

Implement Lower Bound Check: Add a validation check to ensure powerScale is within a reasonable range for negative values as well
