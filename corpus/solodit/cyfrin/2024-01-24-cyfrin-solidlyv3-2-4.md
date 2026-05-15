---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-2-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md
tags:
- firm:cyfrin
- report:2024-01-24-cyfrin-solidlyv3
title: Refactor `zeroRoot` declared in multiple functions into a private constant
vuln_class: []
---

# Refactor `zeroRoot` declared in multiple functions into a private constant

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** `zeroRoot` is declared and used in `RewardsDistributor::pauseClaimsGovernance` [L546](https://github.com/SolidlyV3/v3-rewards/blob/6dfb435392ffa64652c8f88c98698756ca80cf28/contracts/RewardsDistributor.sol#L546) and `pauseClaimsPublic` [L554](https://github.com/SolidlyV3/v3-rewards/blob/6dfb435392ffa64652c8f88c98698756ca80cf28/contracts/RewardsDistributor.sol#L554). Consider refactoring it into a private constant to avoid declaring it in multiple functions.

**Solidly:**
Fixed in commit [653c196](https://github.com/SolidlyV3/v3-rewards/commit/653c19659474c93ef0958479191d8103bc7b7e82).

**Cyfrin:**
Verified.
