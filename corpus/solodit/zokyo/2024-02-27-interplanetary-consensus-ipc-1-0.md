---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-1-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Potential Gas Limitation Issue with `.transfer()` Method in LibStaking.sol
vuln_class: []
---

# Potential Gas Limitation Issue with `.transfer()` Method in LibStaking.sol

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: Medium

**Status**: Resolved 

**Location**: LibStaking.sol contract, Lines 90 and 443

**Description**

The `.transfer()` method is used in two instances within the LibStaking.sol contract (specifically on lines 90 and 443) to send Ether. However, using `.transfer()` poses a risk due to its 2300 gas stipend limitation, which may not be sufficient for all recipient contracts and could lead to failed transactions. T

**Issue Details**:

Gas Stipend Limitation: The `.transfer()` method forwards exactly 2300 gas to the recipient, which is only enough for basic operations like logging an event. This can be insufficient if the recipient contract performs more complex operations in its fallback function.
Risk of Transaction Failure: If the recipient contract's fallback function requires more than 2300 gas (e.g., performing state changes, emitting events, or calling other functions), the transaction will fail.

**Recommendation**: 

It’s better to use the `sendValue` method
