---
affected_contracts: []
derives_from: []
id: solodit-hexens-2023-02-27-polygonzkevm-3-5
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
title: 16. REDUNDANT JUMPS
vuln_class: []
---

# 16. REDUNDANT JUMPS

_Section severity (from Solodit section header): Informational_  
_Audit firm: Hexens_  
_Source report: [2023-02-27-PolygonZkEvm.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md)_

---

**Severity:** Informational

**Path:** utils.zkasm

**Description:** 

In the utils.zkasm:readPush procedure some of the unconditional jumps are redundant as they jump to the very next operation and can be removed for clean code considerations.

*utils.zkasm:readPush*

```
...
   0 => B                      :JMP(readPushBlock)

readPushBlock:
...

   A*16777216 + C => C         :JMP(doRotate)

doRotate:
...
  B - 1 => A                  :JMP(doRotateLoop)

doRotateLoop:
...

```

**Remediation:** Consider removing the redundant jumps.

**Status:** Fixed

- - -
