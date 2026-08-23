---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-09-brightpool-finance-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-02-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-09-Brightpool%20Finance.md
tags:
- firm:zokyo
- report:2024-02-09-brightpool-finance
title: Unreachable Branch
vuln_class: []
---

# Unreachable Branch

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-02-09-Brightpool Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-09-Brightpool%20Finance.md)_

---

**Description**

In the function_internalDeposit in the contract Vesting.sol the condition if (receiver_ == address(0)) revert ZeroAddress() is unnecessary since at L114 ERC20's mint is called which reverts on 0 address mint, therefore checking the condition again is not needed.

**Recommendation**

The check can be removed.

**Re-audit comment**

Resolved
