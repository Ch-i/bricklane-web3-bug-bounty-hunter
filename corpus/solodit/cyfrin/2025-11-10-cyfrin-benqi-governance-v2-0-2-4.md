---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-2-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: Action count increment in `BenqiEcosystemModule::_buildActions` can be simplified
vuln_class: []
---

# Action count increment in `BenqiEcosystemModule::_buildActions` can be simplified

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** `BenqiEcosystemModule::_buildActions` increments the action count when processing indicates that the current gauge should not be skipped:

```solidity
if (!prgv.shouldSkip) {
    actions[actionCount] = Action(_target, 0, prgv.actionData);
    actionCount++;
}
```

However, this logic can be simplified to a single line:

```solidity
if (!prgv.shouldSkip) [actionCount++] = Action(_target, 0, prgv.actionData);
```

**BENQI:** Acknowledged.

**Cyfrin:** Acknowledged.

\clearpage
