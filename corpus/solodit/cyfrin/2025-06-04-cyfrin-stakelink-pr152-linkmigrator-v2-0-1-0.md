---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2-0-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-06-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2-0
title: Unused error
vuln_class: []
---

# Unused error

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md)_

---

**Description:** In [`LINKMigrator.sol#L47`](https://github.com/stakedotlink/contracts/blob/0bd5e1eecd866b2077d6887e922c4c5940a6b452/contracts/linkStaking/LINKMigrator.sol#L47) the error `InvalidPPState` is unused, consider using or removing it.

**stake.link:**
Fixed in [`6827d9d`](https://github.com/stakedotlink/contracts/commit/6827d9df664de5132d81570f03b55ed4a482dff5)

**Cyfrin:** Verified.
