---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-08-25-cyfrin-stake-link-1-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-08-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-08-25-cyfrin-stake-link.md
tags:
- firm:cyfrin
- report:2023-08-25-cyfrin-stake-link
title: Do not use deprecated library functions
vuln_class: []
---

# Do not use deprecated library functions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-08-25-cyfrin-stake-link.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-08-25-cyfrin-stake-link.md)_

---

```solidity
File: PriorityPool.sol

103:         token.safeApprove(_stakingPool, type(uint256).max);

```
**Client:**
Fixed in this [PR](https://github.com/stakedotlink/contracts/pull/32).

**Cyfrin:** Verified.
