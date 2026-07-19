---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-4-7
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: Typos and Bad NATSPEC
vuln_class: []
---

# Typos and Bad NATSPEC

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** We have identified the following typos/NATSPEC problems:

```
AccessControlled.sol
29: `NewAccessControlManager` should be `NewAccessControllManager`

Accounting.sol:
66: `InvalidNavSpit` should be `InvalidNavSplit`

ERC20Cooldown.sol:
10: `allows to store` should be `allows storing`

StrataCDO.sol:
42: `Sinior` should be `Senior`
62: `@notice` is empty

UnstakeCooldown.sol:
144: `for a tokens` should be `for tokens`
```

**Strata:**
Fix in commit [506c4c](https://github.com/Strata-Money/contracts-tranches/commit/506c4c744dc6dea538bb8b69dade114bee1aeb5e) by correcting Typos and updating Natspec.

**Cyfrin:** Verified.
