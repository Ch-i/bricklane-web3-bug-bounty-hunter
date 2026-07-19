---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2-0-2-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-06-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2-0
title: Unchanged state variables can be immutable
vuln_class: []
---

# Unchanged state variables can be immutable

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md)_

---

**Description:** None of:
* [`LINKMigrator.linkToken`](https://github.com/stakedotlink/contracts/blob/0bd5e1eecd866b2077d6887e922c4c5940a6b452/contracts/linkStaking/LINKMigrator.sol#L22)
* [`LINKMigrator.communityPool`](https://github.com/stakedotlink/contracts/blob/0bd5e1eecd866b2077d6887e922c4c5940a6b452/contracts/linkStaking/LINKMigrator.sol#L24)
* [`LINKMigrator.priorityPool`](https://github.com/stakedotlink/contracts/blob/0bd5e1eecd866b2077d6887e922c4c5940a6b452/contracts/linkStaking/LINKMigrator.sol#L27)

Are changed outside of the constructor. Consider making them `immutable` to save on gas when accessing them.

**stake.link:**
Fixed in [`6f9d9b7`](https://github.com/stakedotlink/contracts/commit/6f9d9b77201184d2dfc8f4c06f3430f2d360db24)

**Cyfrin:** Verified.
