---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-1-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: Swaps will revert when `A = B + Xhat - x = 0`
vuln_class: []
---

# Swaps will revert when `A = B + Xhat - x = 0`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** `CompensationPriceFinder::_zeroForOneGetFinalCompensationPrice` implements two branches depending on the sign of `A`. The following logic executes when it is positive, but note that `A` will equal zero when `sumX` is exactly equal to `rangeVirtualReserves0`, i.e. $$A = B + \hat X - x = 0$$:

```solidity
    if (sumX >= rangeVirtualReserves0) {
        // `A` is positive, compute `D = y * (Xhat + B) + A * Yhat`, `p* = (-L + sqrt(D)) / A`.
@>      uint256 a = sumX - rangeVirtualReserves0;
        {
            (uint256 ay1, uint256 ay0) = Math512Lib.fullMul(a, sumUpToThisRange1);
            (d1, d0) = Math512Lib.checkedAdd(d1, d0, ay1, ay0);
        }
        // Compute `sqrtDX96 := sqrt(D) * 2^96 <> sqrt(D * 2^192)`
        (d1, d0) = Math512Lib.checkedMul2Pow192(d1, d0);
        // Reuse `d1, d0` to store numerator `-L + sqrt(D)`.
        (d1, d0) =
            Math512Lib.checkedSub(0, Math512Lib.sqrt512(d1, d0), 0, uint256(liquidity) << 96);
@>      (uint256 upperBits, uint256 p1) = Math512Lib.div512by256(d1, d0, a);
        assert(upperBits == 0);

        return p1.toUint160();
    } else {
```

In this case, execution will revert in `Math512Lib::div512by256` with `DivisorZero()` due to division by zero; however, the actual solution should be $$p_\star = (\hat Y+y) / 2L$$ since the quadratic term in $$A \cdot(\sqrt{p_\star})^2 + 2L\cdot\sqrt{p_\star} - (\hat Y+y) = 0$$ disappears and the equation becomes linear in $$\sqrt{p_\star}$$.

**Impact:** Swaps will revert when $$A = B + \hat X - x = 0$$.

**Recommended Mitigation:** Handle this edge case separately.

**Sorella Labs:** Fixed in commit [500ef96](https://github.com/SorellaLabs/l2-angstrom/commit/500ef9660a20bab0187a9db73078fdbf8a1bebf8).

**Cyfrin:** Verified. The $$A = 0$$ case is now handled separately.

\clearpage
