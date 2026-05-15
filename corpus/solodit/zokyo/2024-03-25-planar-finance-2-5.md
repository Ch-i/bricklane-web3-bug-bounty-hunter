---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-2-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: Lack of Ownership Check in `addRewards` Function Contradicts Documentation
vuln_class: []
---

# Lack of Ownership Check in `addRewards` Function Contradicts Documentation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Severity**: Informational

**Status**:  Resolved

**Location**: Hyperpool.sol, line  402

**Description**:

The `addRewards` function, as per the provided code snippet, is intended for exclusive use by the owner of a Hyper Pool to add reward tokens to the pool. This functionality is crucial for managing the pool's reward distribution and aligns with the governance model outlined in the project documentation. The documentation explicitly states that "Only the owner of a Hyper Pool can fill it with reward tokens," emphasizing the need for ownership verification within the function to adhere to the specified access control policy.

However, the current implementation of the `addRewards` function lacks any form of ownership check or validation.

**Expected Behavior**:
The `addRewards` function should incorporate an ownership check to ensure that only the owner of the Hyper Pool can invoke it. This is critical for maintaining the integrity and security of the pool's reward distribution mechanism, as outlined in the project's documentation.

**Observed Misbehavior:**

The function currently allows any external entity to add rewards to the pool, disregarding the ownership requirement detailed in the documentation.


**Note** The `addRewards` function is meant to be an external function without access restriction, irrespective of the documentation (which was an error). Anybody can add Reward Tokens specified by the Owner. The protocol can charge a fee (Maximum 1%) for non-Owner deposits. You may find this exemption logic in `HyperPoolFactory.sol`
