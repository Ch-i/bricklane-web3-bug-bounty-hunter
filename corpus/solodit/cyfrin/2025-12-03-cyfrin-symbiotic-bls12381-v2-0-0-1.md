---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-03-cyfrin-symbiotic-bls12381-v2-0-0-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-12-03T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-03-cyfrin-symbiotic-bls12381-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-03-cyfrin-symbiotic-bls12381-v2-0
title: Inconsistent handling of point at infinity between `isOnCurve` and `isInSubgroup`
vuln_class: []
---

# Inconsistent handling of point at infinity between `isOnCurve` and `isInSubgroup`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-03-cyfrin-symbiotic-bls12381-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-03-cyfrin-symbiotic-bls12381-v2.0.md)_

---

**Description:** The `BLS12381::isOnCurve` function returns `false` for the point at infinity `(0, 0, 0, 0)`, while `isInSubgroup` returns `true` for the same point. This creates an inconsistency in how the identity element is validated.

In `isOnCurve`, the function checks if $y^2 \equiv x^3 + 4 \pmod{p}$:
- For `(0, 0, 0, 0)`: $y^2 = 0$ but $x^3 + 4 = 4$
- Since $0 \neq 4$, the function returns `false`

However, in `isInSubgroup`:
```solidity
function isInSubgroup(G1Point memory point) internal view returns (bool) {
    G1Point memory result = scalar_mul(point, G1_SUBGROUP_ORDER);
    return result.x_a == 0 && result.x_b == 0 && result.y_a == 0 && result.y_b == 0;
}
```

The point at infinity correctly returns `true` since `0 * order = 0` (identity multiplied by any scalar is identity).

Mathematically, the point at infinity is a valid group element (the identity) but does not have affine coordinates satisfying the Weierstrass curve equation.

Note that other functions in the library handle the point at infinity correctly:
- `add`, `scalar_mul`, `pairing`: Handled by EIP-2537 precompiles
- `negate`: Explicit check returns `(0, 0, 0, 0)` unchanged
- `isInSubgroup`: Returns `true` correctly

This makes `isOnCurve` the sole outlier in its handling of the identity element.

**Impact:**
- If `isOnCurve` is used to validate G1 points before cryptographic operations, the identity element would be incorrectly rejected

**Proof of Concept:**
```solidity
G1Point memory infinity = G1Point(0, 0, 0, 0);

bool onCurve = BLS12381.isOnCurve(infinity);      // returns false
bool inSubgroup = BLS12381.isInSubgroup(infinity); // returns true

// Inconsistent: valid subgroup element fails curve check
```

**Recommended Mitigation:** Add a special case check for the point at infinity in `isOnCurve`:

```solidity
function isOnCurve(G1Point memory point) internal view returns (bool) {
    // Point at infinity is a valid curve point (identity element)
    if (point.x_a == 0 && point.x_b == 0 && point.y_a == 0 && point.y_b == 0) {
        return true;
    }
    // ... rest of the function
}
```

**Symbiotic:** Fixed in [bedb2ea](https://github.com/symbioticfi/relay-contracts/commit/bedb2ea253950f978c07cf80f71ae72ddf313e5a).

**Cyfrin:** Verified.

\clearpage
