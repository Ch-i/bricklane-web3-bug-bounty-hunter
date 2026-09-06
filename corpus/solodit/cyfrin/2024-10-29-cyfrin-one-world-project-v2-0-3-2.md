---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: Mixed use of `uint` and `uint256` in `MembershipERC1155`
vuln_class: []
---

# Mixed use of `uint` and `uint256` in `MembershipERC1155`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** The state declarations in `MembershipERC1155` use both `uint` and `uint256`:

```solidity
mapping(address => uint256) public totalProfit;
mapping(address => mapping(address => uint)) internal lastProfit;
mapping(address => mapping(address => uint)) internal savedProfit;

uint256 internal constant ACCURACY = 1e30;

event Claim(address indexed account, uint amount);
event Profit(uint amount);
```

This is inconsistent and confusing. Consider using `uint256` everywhere as this is more expressive.

**One World Project:** Updated in [`09b6f0f`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/09b6f0f978d2a8d2952a6938bf5756bec8a0170d).

**Cyfrin:** Verified. `uint256` is now used.
