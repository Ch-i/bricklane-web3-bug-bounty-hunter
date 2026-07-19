---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-2-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md
tags:
- firm:cyfrin
- report:2024-01-24-cyfrin-solidlyv3
title: Refactor hard-coded max pool fee into a constant as it is used in multiple
  places
vuln_class: []
---

# Refactor hard-coded max pool fee into a constant as it is used in multiple places

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** `100000` is the hard-coded max pool fee. There are two require statements enforcing this hard-coded value in `SolidlyV3Factory::enableFeeAmount` [L90](https://github.com/SolidlyV3/v3-core/blob/main/contracts/SolidlyV3Factory.sol#L90) and `SolidlyV3Pool::setFee` [L794](https://github.com/SolidlyV3/v3-core/blob/main/contracts/SolidlyV3Pool.sol#L794).

Using the same hard-coded value in multiple places throughout the code is error-prone as when making future code updates a developer can easily update one place but forget to update the others; recommend refactoring to use a constant which can be referenced instead of hard-coding.

**Solidly:**
Acknowledged.
