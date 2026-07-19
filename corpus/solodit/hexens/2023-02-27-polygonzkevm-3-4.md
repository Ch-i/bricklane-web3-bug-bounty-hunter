---
affected_contracts: []
derives_from: []
id: solodit-hexens-2023-02-27-polygonzkevm-3-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-02-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md
tags:
- firm:hexens
- report:2023-02-27-polygonzkevm
title: 15. CALL DEPTH CHECK MISSING
vuln_class: []
---

# 15. CALL DEPTH CHECK MISSING

_Section severity (from Solodit section header): Informational_  
_Audit firm: Hexens_  
_Source report: [2023-02-27-PolygonZkEvm.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md)_

---

**Severity:** Informational

**Path:** opcodes/create-terminate-context.zkasm

**Description:** 

The opcodes in the create-terminate-context.zkasm corresponds to the instructions that create new call contexts, such as opCALL, opDELEGATECALL, opSTATICCALL and etc. By the EVM specification, the call depth needs to have a limit of 1024. 
Refer to page 37 of the Yellow Paper:

https://ethereum.github.io/yellowpaper/paper.pdf

Although is does not have the check right now, there is no visible security impact at the moment of writing as the fact that the calls forward at max 63/64th of the remaining Gas makes it impractical to reach the 1024 level.

**Remediation:** Add the limit check in context creating opcodes.

**Status:** Fixed

- - -
