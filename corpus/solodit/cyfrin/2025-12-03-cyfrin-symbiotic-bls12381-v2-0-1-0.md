---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-03-cyfrin-symbiotic-bls12381-v2-0-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-12-03T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-03-cyfrin-symbiotic-bls12381-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-03-cyfrin-symbiotic-bls12381-v2-0
title: '`BLS12381::hashToG1` can use constants for DST'
vuln_class: []
---

# `BLS12381::hashToG1` can use constants for DST

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-03-cyfrin-symbiotic-bls12381-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-03-cyfrin-symbiotic-bls12381-v2.0.md)_

---

**Description:** In `BLS12381::hashToG1`, the Domain Separation Tag (DST) string is passed as an inline string literal to `expandMsg`, causing unnecessary memory allocation on every call.

```solidity
function hashToG1(bytes memory message) internal view returns (G1Point memory result) {
    bytes memory uniform_bytes = expandMsg("BLS_SIG_BLS12381G1_XMD:SHA-256_SSWU_RO_NUL_", message, 0x80);
```
https://github.com/symbioticfi/relay-contracts/blob/main/src/libraries/utils/BLS12381.sol#L287

At runtime, this:
1. Allocates 43 bytes in memory for the string
2. Copies the string literal from bytecode to memory
3. Incurs memory expansion costs
4. Passes a memory pointer to `expandMsg`

**Impact:** Gas is wasted on every `hashToG1` call. Since BLS signature verification is a common operation, this adds up.

| Test | Before | After | Savings |
|------|--------|-------|---------|
| `test_VerifyValidSignature` | 401,631 | 400,494 | 1,137 gas |
| `test_HashToG1_OnCurveAndNonZero` | 20,672 | 20,298 | 374 gas |

**Recommended Mitigation:** Define the DST as constants and create a specialized `expandMsgBLS` function:

```solidity
bytes32 private constant DST_PART1 = "BLS_SIG_BLS12381G1_XMD:SHA-256_S";
bytes11 private constant DST_PART2 = "SWU_RO_NUL_";
uint8 private constant DST_LEN = 43;

function hashToG1(bytes memory message) internal view returns (G1Point memory result) {
    bytes memory uniform_bytes = expandMsgBLS(message, 0x80);
    // ...
}

function expandMsgBLS(bytes memory message, uint8 n_bytes) internal pure returns (bytes memory) {
    bytes memory zpad = new bytes(0x40);
    bytes memory b_0 = abi.encodePacked(zpad, message, uint8(0x00), n_bytes, uint8(0x00), DST_PART1, DST_PART2, DST_LEN);
    // ... rest of expandMsg logic using DST_PART1, DST_PART2, DST_LEN
}
```

This embeds the DST directly in bytecode, avoiding runtime memory allocation.

**Symbiotic:** Acknowledged, as the team prefers to not perform changes on the `expandMsg`.


\clearpage
