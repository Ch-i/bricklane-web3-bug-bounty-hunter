---
affected_contracts: []
derives_from: []
id: solodit-hexens-2023-02-27-polygonzkevm-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-02-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md
tags:
- firm:hexens
- report:2023-02-27-polygonzkevm
title: 6. INCORRECT LIMIT CHECK IN ZKASM ECRECOVER IMPLEMENTATION
vuln_class: []
---

# 6. INCORRECT LIMIT CHECK IN ZKASM ECRECOVER IMPLEMENTATION

_Section severity (from Solodit section header): Medium_  
_Audit firm: Hexens_  
_Source report: [2023-02-27-PolygonZkEvm.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md)_

---

**Severity:** Medium

**Path:** [StakeableVestingFactory.sol:deployStakeableVesting#L39-L71](https://github.com/0xPolygonHermez/zkevm-rom/blob/develop/main/ecrecover/ecrecover.zkasm#L61C8-L67)

**Description:** 

In the zkASM implementation of the ecrecover function, there must be a check against ECDSA signature malleability. The check should be done when the transaction’s signature is verified and is omitted when the precompiled ecrecover is called. For ECDSA signature not to be malleable, the S value should not be greater than Fp/2 (S <= Fp/2); Fp/2 = 57896044618658097711785492504343953926418782139537452191302581570759080747168 This check is implemented in EVM (Go-ethereum) https://github.com/ethereum/go-ethereum/blob/f53ff0ff4a68ffc56004ab1d5cc244bcb64d3277/crypto/crypto.go#L268-L270

Although in case of zkASM the ecrecover checks againt Fp/2 + 1 (57896044618658097711785492504343953926418782139537452191302581570759080747169), instead of Fp/2, thus the allowed range of S values also includes Fp/2 + 1. This discrepancy can be abused to generate proof for transactions which do not comply with EVM.

```
CONSTL %FNEC_DIV_TWO = 57896044618658097711785492504343953926418782139537452191302581570759080747169n
...
ecrecover_tx:
       %FNEC_DIV_TWO   :MSTORE(ecrecover_s_upperlimit)
...

       ; s in [1, ecrecover_s_upperlimit]
       $ => A      :MLOAD(ecrecover_s_upperlimit)
       $ => B      :MLOAD(ecrecover_s)
       $           :LT,JMPC(ecrecover_s_is_too_big)
       0n => A
       $           :EQ,JMPC(ecrecover_s_is_zero)
```

**Remediation:** The FNEC_DIV_TWO should be equal to 57896044618658097711785492504343953926418782139537452191302581570759080747168 (Fp/2).

**Status:** Fixed

- - -
