---
affected_contracts: []
derives_from: []
id: solodit-hexens-2023-02-27-polygonzkevm-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-02-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md
tags:
- firm:hexens
- report:2023-02-27-polygonzkevm
title: 9. RECOMMENDATION TO CHANGE A CONDITIONAL JUMP
vuln_class: []
---

# 9. RECOMMENDATION TO CHANGE A CONDITIONAL JUMP

_Section severity (from Solodit section header): Low_  
_Audit firm: Hexens_  
_Source report: [2023-02-27-PolygonZkEvm.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md)_

---

**Severity:** Low

**Path:** /main/opcodes/block.zkasm

**Description:**  

While analysing the zkEVM ROM opcodes and the appropriate PIL representation in the state machines it has been noticed that some of the conditional jumps differ in their operational register size:
-   *JMPN (jump negative)*

```
pol jmpnCondValue = JMPN*(isNeg*2**32 + op0);
```
-   *JMPZ (jump zero) and JMPNZ (jump not zero)*
```
/// op0 check zero
pol commit op0Inv;
pol op0IsZero = 1 - op0*op0Inv;
op0IsZero*op0 = 0;
...
pol doJMP = JMPN*isNeg + JMP + JMPC*carry + JMPZ*op0IsZero + return + call;
```
It can be seen that the JMPN/Z/NZ opcodes consider the op0 register only, unlike other conditional jumps such as JMPC,JMPNC, which use binary state machine carry latch, which operates on 256-bit values.

As a result, these type of jumps will consider only the lower part of the registers that have 8-slot (A,B,C,...):
```
A   :JMPZ(someLabel)
```
The jump will happen as long as A0 = 0, even for A = [A0 = 0, A1 != 0 ,...,A7 != 0], for example if A = 2^32. This holds true as op0=A0,op1=A1,...op7=A7 and only the op0 will be used in the jump condition.

We have iteratively looked through all of the JMPN,JMPZ,JMPNZ calls done throughout all of the zkEVM ROM in order to find the ones that use 8-slot registers and don't have other limitations of the register's value (e.g., to be smaller than 2^32).

After multiple iterations, the only case found where the register can hold values bigger than 2^32 is in the opBLOCKHASH:
```
opBLOCKHASH:
...
   ; Get last tx count
   $ => B          :MLOAD(txCount)
   $ => A          :MLOAD(SP) ; [blockNumber => A]
   ; Check batch block is lt current block number, else return 0
   B - A - 1       :JMPN(opBLOCKHASHzero)
   ```
Here the JMPN can be incorrectly triggered in the scenario where the txCount is greater than 2^32; this is probable to happen, although not in the near future, as the blocks in zkEVM network actually represent transactions (hence the reason why txCount is being used), and with an average expectation of 75 TPS it will overlap 32-bit values after 1.5-2 years. As this is a very prolonged scenario, the severity of the issue is lowered.

Nonetheless, if this happens, the BLOCKHASH instruction for older blockNumbers will start returning 0 instead of their actual values.

**Remediation:** Consider using LT opcode and JMPC conditional jump instead of JMPN; in that case, the txCount should be incremented with ADD opcode.

**Status:** Fixed

- - -
