---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-06-01-protectorate-3-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-06-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-Protectorate.md
tags:
- firm:pashov-audit-group
- report:2023-06-01-protectorate
title: '[L-01] Strategy contract is incompatible with non-standard ERC20 tokens'
vuln_class: []
---

# [L-01] Strategy contract is incompatible with non-standard ERC20 tokens

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-06-01-Protectorate.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-Protectorate.md)_

---

Some tokens (for example `USDT`) do not follow the ERC20 standard correctly and do not revert a `bool` on `approve` call. Such tokens are incompatible with the `BendDaoLendingStrategy` contract as the `approve` calls in `deposit` & `withdraw` will always revert due to zero return data. Use `SafeERC20`'s `forceApprove` instead
