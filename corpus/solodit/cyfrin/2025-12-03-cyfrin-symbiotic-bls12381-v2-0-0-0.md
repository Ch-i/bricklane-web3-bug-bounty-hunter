---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-03-cyfrin-symbiotic-bls12381-v2-0-0-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-12-03T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-03-cyfrin-symbiotic-bls12381-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-03-cyfrin-symbiotic-bls12381-v2-0
title: '`BLS12381::findYFromX` returns `sqrt(-a)` instead of reverting when input
  is not a quadratic residue'
vuln_class: []
---

# `BLS12381::findYFromX` returns `sqrt(-a)` instead of reverting when input is not a quadratic residue

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-03-cyfrin-symbiotic-bls12381-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-03-cyfrin-symbiotic-bls12381-v2.0.md)_

---

**Description:** `BLS12381::findYFromX` computes the square root using the formula `y = (x^3+4)^((p+1)/4) mod p`. This formula only works correctly when `x^3+4` is a quadratic residue modulo p. When `x^3+4` is NOT a quadratic residue, the function returns `sqrt(-(x^3+4))` instead of reverting.

```solidity
function findYFromX(uint256 x_a, uint256 x_b) internal view returns (uint256 y_a, uint256 y_b) {
    // compute (x**3 + 4) mod p
    (y_a, y_b) = _xCubePlus4(x_a, x_b);

    // compute y = sqrt(x**3 + 4) mod p = (x**3 + 4)^(p+1)/4 mod p
    // ...
}
```

By Euler's criterion:
- If `a` is a quadratic residue: `a^((p-1)/2) = 1 (mod p)`
- If `a` is NOT a quadratic residue: `a^((p-1)/2) = -1 (mod p)`

So when `a` is not a quadratic residue:

```
(a^((p+1)/4))^2 = a^((p+1)/2) = a^((p-1)/2) * a = (-1) * a = -a (mod p)
```

The result `a^((p+1)/4)` gives `sqrt(-a)`, not `sqrt(a)`.

**Impact:** `findYFromX` is used in `KeyBlsBls12381::deserialize`, If an invalid x-coordinate is provided where `x^3+4` is not a quadratic residue, `deserialize` returns an invalid point that is NOT on the curve, rather than reverting.

The impact is limited in the current codebase because:
1. In `KeyRegistry::_setKey`, keys are validated via `fromBytes` -> `wrap` which checks `isOnCurve` and `isInSubgroup` before storing
2. `deserialize` only reads from trusted storage containing validated keys
3. BLS precompiles: BLS12_G1ADD, BLS12_G1MSM, BLS12_PAIRING_CHECK  would reject invalid points. https://github.com/ethereum/go-ethereum/blob/6f2cbb7a27ba7e62b0bdb2090755ef0d271714be/core/vm/contracts.go#L1211

However, if `findYFromX` or `deserialize` is used in another context without proper validation, it could return invalid curve points silently.

**Proof of Concept:** Example with p = 19 (where 19 = 3 (mod 4)):

| a | Is QR? | a^5 mod 19 | (a^5)^2 mod 19 | Expected |
|---|--------|------------|---------------|----------|
| 4 | Yes | 17 | 4 | a |
| 3 | No | 15 | 16 | -a = -3 = 16 |
| 2 | No | 13 | 17 | -a = -2 = 17 |
| 5 | Yes | 9 | 5 | a |

For non-quadratic residues, `a^((p+1)/4)` gives `sqrt(-a)` instead of `sqrt(a)`.

**Recommended Mitigation:** For future upgrades that do not enforce curve membership and subgroup validation, ensure proper handling of the edge case where x^3+4 fails to be a quadratic residue.

**Symbiotic:** Acknowledged, as the team aims to leave `BLS12381` behavior similar to `BN254`.
