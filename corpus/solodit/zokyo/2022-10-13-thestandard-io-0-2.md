---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-10-13-thestandard-io-0-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2022-10-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md
tags:
- firm:zokyo
- report:2022-10-13-thestandard-io
title: Unsafe ERC20 transfer in SEuroOffering `transferCollateral`.
vuln_class: []
---

# Unsafe ERC20 transfer in SEuroOffering `transferCollateral`.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2022-10-13-TheStandard.io.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md)_

---

**Description**

SEuroOffering.sol transferCollateral - function is transferring assets (i.e. tokens) without safeguarding that transfer and not validating return.

**Recommendation**

It is preferred to use safeTransfer while transferring ERC20.

**Re-audit comment**

Unresolved
