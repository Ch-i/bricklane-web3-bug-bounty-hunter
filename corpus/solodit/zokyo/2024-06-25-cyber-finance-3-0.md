---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-06-25-cyber-finance-3-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-06-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-25-Cyber%20Finance.md
tags:
- firm:zokyo
- report:2024-06-25-cyber-finance
title: Front Running Vulnerability in `decreaseClaimable` Function
vuln_class: []
---

# Front Running Vulnerability in `decreaseClaimable` Function

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-06-25-Cyber Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-25-Cyber%20Finance.md)_

---

**Severity**: Informational

**Status**: Acknowledged

The `decreaseClaimable` function, which can only be called by an admin, is vulnerable to front running by users who call the claim function. This allows the users to drain the claimable balance before it is decreased by the `decreaseClaimable` function. This behavior can potentially lead to unexpected fund depletion or malicious draining of resources.

**Recommendation**: 

To mitigate this vulnerability, consider implementing a two-step claim process. Introduce a `commitClaim` function where the user commits to a planned claim as the first step. The user would then finalize the claim after a certain number of blocks have passed and before a specified deadline block. This mechanism would significantly hinder opportunistic claims based on admin actions, thereby reducing the risk of front-running exploits.
