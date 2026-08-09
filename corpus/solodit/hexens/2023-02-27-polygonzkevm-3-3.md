---
affected_contracts: []
derives_from: []
id: solodit-hexens-2023-02-27-polygonzkevm-3-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-02-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md
tags:
- firm:hexens
- report:2023-02-27-polygonzkevm
title: 14. PERMUTATION CONSTRAINT DISCREPANCY BETWEEN VERIFYPIL TOOLING AND STARK
  GENERATION
vuln_class: []
---

# 14. PERMUTATION CONSTRAINT DISCREPANCY BETWEEN VERIFYPIL TOOLING AND STARK GENERATION

_Section severity (from Solodit section header): Informational_  
_Audit firm: Hexens_  
_Source report: [2023-02-27-PolygonZkEvm.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md)_

---

**Severity:** Informational

**Path:** pilcom/src/pil_verifier.js

**Description:** 

In PIL language there is a selector polynomial for choosing specific lines to meet the constraints.

But there is differences how verifyPIL method and STARK generator uses that selector. 
In case of permutation constraint, 2 sequences must have the same length. We can make 2 different length sequences to be checked via selectors.

For example we have a PIL:
```
constant %N = 4;

namespace Global(%N);
   pol constant L1;

namespace PermutationExample(%N);

   pol constant b1, b2; // selector polynomials
   pol commit a1, a2;
   b1{a1} is b2{a2};
```
*and corresponding polynomials:*
```
const b1 = [1,1,1,0];
const b2 = [1,1,1,1];

const a1 = [1,2,3,4];
const a2 = [4,3,2,1];

```
In that case verifyPIL check will pass but the STARK generator will throw an exception while counting the z polynomial.
```
for (let j=0; j<N; j++) {
   if ((pi.selT==null) || (!F.isZero(pols.exps[pi.selT].v_n[j]))) {
       const vals = []
       for (let k=0; k<pi.t.length; k++) {
           vals.push(F.toString(pols.exps[pi.t[k]].v_n[j]));
       }
       const v = vals.join(",");
       t[v] = (t[v] || 0) + 1;
   }
}

for (let j=0; j<N; j++) {
   if ((pi.selF==null) || (!F.isZero(pols.exps[pi.selF].v_n[j]))) {
       const vals = []
       for (let k=0; k<pi.f.length; k++) {
           vals.push(F.toString(pols.exps[pi.f[k]].v_n[j]));
       }
       const v = vals.join(",");
       const found = t[v] ?? false;
       if (!t[v]) {
           res.push(`${pi.fileName}:${pi.line}:  permutation not `+(found === 0 ? 'enought ':'')+`found w=${j} values: ${v}`);
           console.log(res[res.length-1]);
           if (!config.continueOnError) j=N;  // Do not continue checking
       }
       else {
           t[v] -= 1;
       }
   }
}
```

**Remediation:** Make sure that 2 sequences have the same length when there is used a selector in permutation constraint.

**Status:** Fixed

- - -
