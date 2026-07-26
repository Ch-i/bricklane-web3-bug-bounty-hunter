---
affected_contracts: []
derives_from: []
id: solodit-hexens-2023-02-27-polygonzkevm-3-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-02-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md
tags:
- firm:hexens
- report:2023-02-27-polygonzkevm
title: 13. PLOOKUP AND PERMUTATION SELECTOR POLYNOMIAL DISCREPANCY BETWEEN VERIFYPIL
  TOOLING AND STARK GENERATION
vuln_class: []
---

# 13. PLOOKUP AND PERMUTATION SELECTOR POLYNOMIAL DISCREPANCY BETWEEN VERIFYPIL TOOLING AND STARK GENERATION

_Section severity (from Solodit section header): Informational_  
_Audit firm: Hexens_  
_Source report: [2023-02-27-PolygonZkEvm.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md)_

---

**Severity:** Informational

**Path:**  [PolygonZkEVM.sol](https://github.com/0xPolygonHermez/pilcom/blob/107765f18d78a865c12517c9c84cbdfbad1d99d0/src/pil_verifier.js#L194-L222)

**Description:** 

In PIL language there is a selector polynomial for choosing specific lines to meet the constraints.

But there is differences how verifyPIL method and STARK verifier uses 
that selector. For verifyPIL polynomial trace’s lines are being chosen in case of the selectors are not 0 and can be not equal.

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
and corresponding polynomials:
```
const b1 = [0,5,0,0];
const b2 = [6,0,0,0];

const a1 = [4,2,3,21];
const a2 = [2,6,19,7];
```
verifyPil method will work in this case, but STARK generator throws an exception as the z polynomial: the grand product will not be equal to 1.

The difference arises as the verifyPil method doesn’t check whether two selectors are, only checks not zero case (https://github.com/0xPolygonHermez/pilcom/blob/107765f18d78a865c12517c9c84cbdfbad1d99d0/src/pil_verifier.js#L194-L222) , but in the STARK generation selector polynomials are being interpolated and used in grand product’s calculations, so our example will fail on STARK generation phase.

The same issues arises also for plookup identities.
*PermutationIdentities code:*
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
*PlookupIdentities code:*
```
let t = {};
       for (let j=0; j<N; j++) {
           if ((pi.selT==null) || (!F.isZero(pols.exps[pi.selT].v_n[j]))) {
               const vals = []
               for (let k=0; k<pi.t.length; k++) {
                   vals.push(F.toString(pols.exps[pi.t[k]].v_n[j]));
               }
               t[vals.join(",")] = true;
           }
       }


       for (let j=0; j<N; j++) {
           if ((pi.selF==null) || (!F.isZero(pols.exps[pi.selF].v_n[j]))) {
               const vals = []
               for (let k=0; k<pi.f.length; k++) {
                   vals.push(F.toString(pols.exps[pi.f[k]].v_n[j]));
               }
               const v = vals.join(",");
               if (!t[v]) {
                   res.push(`${pil.plookupIdentities[i].fileName}:${pil.plookupIdentities[i].line}:  plookup not found w=${j} values: ${v}`);
                   console.log(res[res.length-1]);
                   if (!config.continueOnError) j=N;  // Do not continue checking
               }
           }
       }
```

**Remediation:**  VerifyPil method must check whether two selectors are equal.

**Status:** Fixed

- - -
