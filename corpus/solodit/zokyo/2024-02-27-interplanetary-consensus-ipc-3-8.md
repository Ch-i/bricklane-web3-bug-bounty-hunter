---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-3-8
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
title: Enhancing Gas Efficiency in `createSubnetId` Through Caching `subnet.route.length`
vuln_class: []
---

# Enhancing Gas Efficiency in `createSubnetId` Through Caching `subnet.route.length`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: Informational 

**Status**: Resolved

**Location**: subnetIdHelper.sol

**Description**

In the `subnetIdHelper` smart contract, specifically within the `createSubnetId` function, there is an opportunity to optimize gas usage by caching the value of subnet.route.length. The current implementation retrieves this value multiple times, which can be more gas-intensive than necessary.
Rationale for Suggested Change:
Gas Efficiency Through Caching:
Accessing the length of a dynamic array (subnet.route.length) multiple times in a function incurs a small but repeated gas cost.

**Recommendation**:

By caching this length in a local variable (`routeLength`), and using it throughout the function, we reduce the number of times the contract has to fetch this property, saving gas.Each access to subnet.route.length can be considered a read operation from the contract's state. Reducing state access where possible is a good practice in smart contract optimization.
