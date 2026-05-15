---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: '`MIN_SPEED` and `DEFAULT_MIN_SPEED` should be merged into a shared constants
  library'
vuln_class: []
---

# `MIN_SPEED` and `DEFAULT_MIN_SPEED` should be merged into a shared constants library

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** The `DistributionManager`, `BenqiCoreModule`, and `BenqiEcosystemModule` contracts each independently define a constant for the minimum reward speed, `DEFAULT_MIN_SPEED` and `MIN_SPEED` respectively. Although they currently share the same value of 1 wei purpose, to ensure a minimal reward flow when gauge votes drop to zero, they are not linked.

The `DistributionManager` uses its `DEFAULT_MIN_SPEED` to calculate the maximum permissible budget overrun. In contrast, the modules use their own private `MIN_SPEED` constants to determine the actual budget required, which includes applying this minimum speed floor.

**Impact:** This duplication adds additional overheads introduces the risk of the values becoming inconsistent during future development. If `MIN_SPEED` in a module is changed to a value that differs from `DEFAULT_MIN_SPEED` in the `DistributionManager`, the values will no longer be equal.

**Recommended Mitigation:** To ensure consistency and simplify maintenance, the minimum speed constant should be defined in a single location:

1.  Create a new library (e.g., `Constants.sol`) to hold shared constants.

2.  Define a single `MIN_SPEED` constant in this new library.

3.  Remove the separate `DEFAULT_MIN_SPEED` and `MIN_SPEED` definitions from `DistributionManager`, `BenqiCoreModule`, and `BenqiEcosystemModule`.

4.  Have all three contracts import the new constants library and reference the single `MIN_SPEED` value. This ensures that all components of the system are always operating with the same parameter, preventing potential inconsistencies.

**BENQI:** Fixed in PR [\#29](https://github.com/aragon/benqi-governance/pull/29).

**Cyfrin:** Verified.
