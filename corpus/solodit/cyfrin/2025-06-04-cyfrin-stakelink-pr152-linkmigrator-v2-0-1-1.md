---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2-0-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-06-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2-0
title: Lack of events emitted on important state changes
vuln_class: []
---

# Lack of events emitted on important state changes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md)_

---

**Description:** [`LINKMigrator::setQueueDepositMin`](https://github.com/stakedotlink/contracts/blob/0bd5e1eecd866b2077d6887e922c4c5940a6b452/contracts/linkStaking/LINKMigrator.sol#L119-L125) and [`PriorityPool::setQueueBypassController`](https://github.com/stakedotlink/contracts/blob/0bd5e1eecd866b2077d6887e922c4c5940a6b452/contracts/core/priorityPool/PriorityPool.sol#L678-L685) change internal state without emitting events. Events are important for off-chain tracking and transparency. Consider emitting events from these functions.

**stake.link:**
Acknowledged.
