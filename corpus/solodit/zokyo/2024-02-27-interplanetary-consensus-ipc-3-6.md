---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-3-6
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Incorrect Description in pop Function Comments of `LibMaxPQ`
vuln_class: []
---

# Incorrect Description in pop Function Comments of `LibMaxPQ`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: Informational

**Status**: Resolved 

**Location**: LibMaxPQ

In the LibMaxPQ library, the In the LibMaxPQ library, the comments above the pop function inaccurately describe its functionality. The comment states that the function pops the "minimal value" from the priority queue, but the function's logic suggests that it actually pops the "maximum value." This discrepancy can lead to confusion about the function's behavior.
**Location of Issue**:
**File**: LibMaxPQ
**Function**: pop
Functionality Check:
Based on the provided code snippet and typical implementations of Max Priority Queues, it seems that the largest value in a Max Priority Queue is stored at the root (slot 1). The pop function appears to remove the top element, which would be the largest value in the queue, not the smallest.
**Issue Details**:
Misleading Information: The comment incorrectly indicates that the function pops the minimal value.
Potential for Misinterpretation: Developers or maintainers reading the code could be misled by the comment, potentially leading to incorrect assumptions or use of the function. 
**Fix**: Issue addressed and resolved in commit 632e710 .
**Recommendation for Resolution**:
Correct the Comment: Update the comment to accurately reflect the function's behavior of removing the maximum value from the priority queue.
 above the pop function inaccurately describe its functionality. The comment states that the function pops the "minimal value" from the priority queue, but the function's logic suggests that it actually pops the "maximum value." This discrepancy can lead to confusion about the function's behavior.
**Location of Issue:**
**File**: LibMaxPQ
**Function**: pop
**Functionality Check**:
Based on the provided code snippet and typical implementations of Max Priority Queues, it seems that the largest value in a Max Priority Queue is stored at the root (slot 1). The pop function appears to remove the top element, which would be the largest value in the queue, not the smallest.
**Issue Details**:
**Misleading Information**: The comment incorrectly indicates that the function pops the minimal value.
Potential for Misinterpretation: Developers or maintainers reading the code could be misled by the comment, potentially leading to incorrect assumptions or use of the function.
**Recommendation for Resolution**:
Correct the Comment: Update the comment to accurately reflect the function's behavior of removing the maximum value from the priority queue.
