---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-3-11
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Gas Optimization in LibMaxPQ Contract Using Bitwise Shift Operations
vuln_class: []
---

# Gas Optimization in LibMaxPQ Contract Using Bitwise Shift Operations

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: informational

**Status**: Resolved 

**Description**

The LibMaxPQ contract currently employs multiplication and division by 2 in its logic (specifically at lines 158, 133, and 119). This informational finding suggests the replacement of these operations with bitwise shift operations as a means to enhance gas efficiency in the contract's execution.
Details of Current Implementation:
Multiplication by 2:
Line 158: x * 2
Line 133: y * 2
Division by 2:
Line 119: z / 2
**Recommendation and Rationale for Suggested Change**:
Gas Efficiency with Bitwise Operations:
Multiplication and Division by 2: These are relatively more expensive in terms of gas usage because they are interpreted as arithmetic operations.
Bitwise Shifts: Replacing these with bitwise left shift (<<) for multiplication and right shift (>>) for division is more efficient. This is because bitwise shifts are simpler operations at the binary level and typically consume less gas.
Left Shift (<<): A single left bitwise shift (x << 1) is equivalent to multiplying by 2 (x * 2).
Right Shift (>>): A single right bitwise shift (z >> 1) is equivalent to dividing by 2 (z / 2).
Solidity and EVM Optimization:
In Solidity, optimizing for gas usage is crucial. Bitwise operations are generally more efficient in the Ethereum Virtual Machine (EVM), leading to lower transaction costs.
No Functional Impact:
Switching to bitwise operations in the mentioned scenarios should not impact the contract's logic. The primary purpose of these operations is to manipulate numerical values for algorithmic logic, and bitwise shifts accomplish the same with better efficiency.

**Recommendation**:

These are the following recommendations:
Replace the multiplication by 2 operations (x * 2, y * 2) with left bitwise shifts (x << 1, y << 1) on lines 158 and 133.
Replace the division by 2 operation (z / 2) with a right bitwise shift (z >> 1) on line 119.
Expected Outcome:
The change is anticipated to yield gas savings per transaction involving these operations. The savings, while potentially modest per transaction, can accumulate to significant amounts over many transactions, contributing to overall contract efficiency.
