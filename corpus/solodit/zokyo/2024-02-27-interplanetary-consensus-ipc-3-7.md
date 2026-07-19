---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-3-7
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
title: Potential for Gas Optimization through Tighter Packing of `SubnetActorStorage`
  Struct
vuln_class: []
---

# Potential for Gas Optimization through Tighter Packing of `SubnetActorStorage` Struct

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: Informational 

**Status**: Resolved 

**Instance 1**: 

Potential for Enhanced Gas Efficiency in ConstructorParams Struct through Variable Reordering
Overview: The ConstructorParams struct currently includes a mixture of data types that may not be optimally ordered for gas efficiency. Solidity's storage optimization mechanisms can be better leveraged by reordering the struct's variables, thus potentially reducing the gas cost associated with deploying and interacting with contracts using this struct.
Current Structure: The struct includes:
SubnetID parentId;
address ipcGatewayAddr;
ConsensusType consensus;
uint256 minActivationCollateral;
uint64 minValidators;
uint64 bottomUpCheckPeriod;
uint8 majorityPercentage;
uint16 activeValidatorsLimit;
uint256 minCrossMsgFee;
int8 powerScale;
Proposed Optimization: The struct can be reorganized to group variables of smaller sizes together, allowing Solidity to pack these into the same 32-byte storage slot.
Instance 2:
The SubnetActorStorage struct in the given contract can benefit from optimization through tighter packing of its variables. Solidity storage variables are laid out in 32-byte slots, and proper organization of these variables can lead to more efficient use of these slots, reducing the gas cost associated with storage operations.
Current Structure: The SubnetActorStorage struct contains a mix of variable types of different sizes (e.g., uint256, uint64, address, bool, int8, and mappings). The current arrangement does not fully utilize the potential for tight packing.
Proposed Optimization: Reorder the variables in SubnetActorStorage to group smaller-sized variables together. This reordering allows Solidity to pack these variables into the same 32-byte storage slots, thereby optimizing storage usage.
Rationale for Suggested Change:
Efficient Storage Slot Usage: Solidity can pack multiple smaller-sized variables (like uint64, uint16, uint8, int8) into a single 32-byte storage slot. Grouping these variables together can minimize the number of storage slots needed.
Gas Cost Reduction: Efficiently using storage slots can lead to reduced gas costs, especially in operations involving contract deployment and state updates.
Maintaining Logical Grouping: It's important to balance optimization with logical structuring of data. The reordering should not compromise the readability and logical grouping of related variables.

**Recommendation**:

Group smaller integer variables together (uint64, uint16, uint8, int8).
Place larger data types like uint256 and address next.
SubnetID and ConsensusType may be placed according to their respective sizes or at the end if they are complex types.
