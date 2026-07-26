---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-2-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-09-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-04-cyfrin-symbiotic-v2-0
title: Redundant manual access control checks
vuln_class: []
---

# Redundant manual access control checks

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-04-cyfrin-symbiotic-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md)_

---

**Description:** In both `BaseRewards` and `BaseSlashing` contracts, functions perform manual access control checks (`_checkRewarder` and `_checkSlasher`) instead of using the already-defined `onlyRewarder` and `onlySlasher` modifiers. Specifically:

* `distributeStakerRewards` and `distributeOperatorRewards` in `BaseRewards`

* `slashVault` and `executeSlashVault` in `BaseSlashing`

This inconsistency reduces code readability and increases the risk of missing or duplicating access control logic in the future.

**Recommended Mitigation:** Replace manual `_checkRewarder` and `_checkSlasher` calls with their corresponding modifiers for cleaner and more consistent access control enforcement:

```solidity
function distributeStakerRewards(...) public virtual onlyRewarder { ... }

function distributeOperatorRewards(...) public virtual onlyRewarder { ... }

function slashVault(...) public virtual onlySlasher returns (...) { ... }

function executeSlashVault(...) public virtual onlySlasher returns (...) { ... }
```

This ensures access checks are declarative, standardized, and easier to maintain.

**Symbiotic:** Acknowledged. Intended to decrease bytecode size.

**Cyfrin:** Acknowledged.
