---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-10-13-thestandard-io-2-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-10-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md
tags:
- firm:zokyo
- report:2022-10-13-thestandard-io
title: Deployer responsibility for correct Oracle address in TokenManager.
vuln_class: []
---

# Deployer responsibility for correct Oracle address in TokenManager.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-10-13-TheStandard.io.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md)_

---

**Description**

TokenManager.sol
The deployer can put any address as the Oracle address. This address is used by other contracts in the project for making calculations. It is the responsibility of the deployer to put the correct oracle address.

**Recommendation**

Ensure a trusted and correct Oracle address is set during deployment, as this is critical for calculations in other project contracts.

**Re-audit comment**

Unresolved
