---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-3-10
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
title: Inconsistent Naming in `getAppliedTopDownNonce` Function of GatewayGetterFacet.sol
vuln_class: []
---

# Inconsistent Naming in `getAppliedTopDownNonce` Function of GatewayGetterFacet.sol

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: Informational 

**Status**: Resolved 

**Location**: GatewayGetterFacet.soo

**Description**

In the GatewayGetterFacet.sol contract, the function `getAppliedTopDownNonce` is misleadingly named as it returns the topDownNonce instead of the appliedTopDownNonce. This discrepancy between the function name and its actual behavior can lead to confusion and potential misuse in the context where the function is invoked.
**Issue Details**:
Naming Mismatch: The function name suggests that it returns an appliedTopDownNonce, but the implementation shows that it actually returns the topDownNonce.
Potential Misinterpretation: Users or developers interacting with this function might expect to receive the appliedTopDownNonce, leading to erroneous implementations or interpretations based on the function's output.

**Recommendation for Resolution**:

Rename Function: Consider renaming the function to accurately reflect its functionality, such as getTopDownNonce, to prevent confusion and ensure clarity in the contract's interface.
