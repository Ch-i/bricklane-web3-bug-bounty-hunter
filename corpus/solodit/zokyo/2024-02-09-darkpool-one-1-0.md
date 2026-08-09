---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-09-darkpool-one-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-02-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-09-Darkpool%20One.md
tags:
- firm:zokyo
- report:2024-02-09-darkpool-one
title: Validate array lengths
vuln_class: []
---

# Validate array lengths

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-02-09-Darkpool One.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-09-Darkpool%20One.md)_

---

**Severity** - Low

**Status** - Resolved

**Description**

In the contract Vesting.sol’s constructor array of vestedPlans , receivers , amounts and timestamps is passed but there are not sufficient checks to verify the lengths of these arrays.
It should be made sure that these arrays are of equal lengths otherwise it might result in erroneous assignment.

**Recommendation**:

Ensure all these arrays are of equal lengths.
