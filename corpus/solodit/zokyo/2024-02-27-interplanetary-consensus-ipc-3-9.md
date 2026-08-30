---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-3-9
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
title: Missing Getter Function for `appliedBottomUpNonce` in GatewayGetterFacet.sol
vuln_class: []
---

# Missing Getter Function for `appliedBottomUpNonce` in GatewayGetterFacet.sol

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: Informational 

**Status**: Resolved 

**Location**: GatewayGetterFacet.sol

**Description**

The Subnet struct in the GatewayGetterFacet.sol contract includes an `appliedBottomUpNonce` field, but there is no corresponding getter function to retrieve this value. The absence of a getter for appliedBottomUpNonce presents an inconsistency in the contract's interface, potentially hindering the ability to access important contract state information.

**Issue Details**:

**Missing Functionality**: The lack of a getter function for appliedBottomUpNonce limits external visibility into this particular state variable.
Inconsistent Access Patterns: While other fields in the Subnet struct are accessible through getter functions, appliedBottomUpNonce is not, leading to an inconsistent interface.

**Recommendation for Resolution**:

Implement Getter Function: Add a new function to the GatewayGetterFacet.sol contract that allows users to retrieve the appliedBottomUpNonce value for a given subnet. This enhances transparency and usability of the contract.
