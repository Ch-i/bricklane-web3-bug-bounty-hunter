---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-07-05-made-for-gamers-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2022-07-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-05-Made%20for%20gamers.md
tags:
- firm:zokyo
- report:2022-07-05-made-for-gamers
title: Owner is able to destroy the contract.
vuln_class: []
---

# Owner is able to destroy the contract.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-07-05-Made for gamers.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-05-Made%20for%20gamers.md)_

---

**Description**

Expo.sol: function destroySmartContract(). Owner has the ability to destroy the contract with the following function, destroying all users' balances as well. In case the owner key is compromised or stolen, the contract can be destroyed forever with all users' balances. Verify the necessity of this function. This issue is connected to crucial smart-contract logic, thus need to be mentioned in the report, and it needs to be verified by the team.

**Recommendation**

Verify the necessity of this function.

**Re-audit comment**

Resolved.

Post-audit:

The team has removed the selfdestruct functionality
