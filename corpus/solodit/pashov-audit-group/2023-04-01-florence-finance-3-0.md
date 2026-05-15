---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-04-01-florence-finance-3-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-04-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md
tags:
- firm:pashov-audit-group
- report:2023-04-01-florence-finance
title: '[L-01] If too many funding tokens are whitelisted then removal might become
  impossible'
vuln_class: []
---

# [L-01] If too many funding tokens are whitelisted then removal might become impossible

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-04-01-Florence Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md)_

---

The `setFundingToken` method in `LoanVault` allows the owner to whitelist as many funding tokens as he wants, pushing them to an unbounded array. The problem is that if he whitelists too many tokens, then the array will grow too big and removing a value (for example the last one) from the array might cost too much gas, even more than the block gas limit, resulting in impossibility of removing some funding tokens from the whitelist. To fix this you should put an upper limit on the `_fundingTokens` array size, for example 50.
