---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-1-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-08-cyfrin-aztec-polynomial-v2-0
title: '`compute_linear_polynomial_product` is O(n^3) instead of O(n^2)'
vuln_class: []
---

# `compute_linear_polynomial_product` is O(n^3) instead of O(n^2)

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** In [`polynomial_arithmetic.cpp:213`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.cpp#L213), `compute_linear_polynomial_product` builds the polynomial `(X − r_0)(X − r_1)···(X − r_{n−1})` using a doubly-nested loop with a `compute_sum` call inside, giving total complexity **O(n^3)**:

```cpp
for (size_t i = 0; i < n - 1; ++i) {
    temp = 0;
    for (size_t j = 0; j < n - 1 - i; ++j) {
        scratch_space[j] = roots[j] * compute_sum(&scratch_space[j + 1], n - 1 - i - j);
        //                              compute_sum is O(n - 1 - i - j) → cubic total
        temp += scratch_space[j];
    }
    dest[n - 2 - i] = temp * constant;
    constant *= Fr::neg_one();
}
```

The same coefficients can be obtained in **O(n^2)** by the standard "multiply by `(X − r_i)` one root at a time" recurrence:

```cpp
dest[0] = -roots[0];
dest[1] = 1;
for (size_t i = 1; i < n; ++i) {
    const Fr r = roots[i];
    dest[i + 1] = dest[i];
    for (size_t k = i; k >= 1; --k) {
        dest[k] = dest[k - 1] - r * dest[k];
    }
    dest[0] = -r * dest[0];
}
```

Short trace with `n = 3`, `roots = [1, 2, 3]`, expected `(X−1)(X−2)(X−3) = X^3 − 6X^2 + 11X − 6` -> `dest = [−6, 11, −6, 1]`:

- Init (represents `X − 1`): `dest = [−1, 1, ?, ?]`.
- Iteration `i = 1` (multiply in `X − 2`, `r = 2`):
  - shift `dest[2] = dest[1] = 1`;
  - inner `k=1`: `dest[1] = dest[0] − r·dest[1] = −1 − 2 = −3`;
  - then `dest[0] = −r·dest[0] = 2`.
  - Result: `[2, −3, 1, ?]` = `(X−1)(X−2)`.
- Iteration `i = 2` (multiply in `X − 3`, `r = 3`):
  - shift `dest[3] = dest[2] = 1`;
  - inner `k=2`: `dest[2] = dest[1] − r·dest[2] = −3 − 3·1 = −6`;
  - inner `k=1`: `dest[1] = dest[0] − r·dest[1] = 2 − 3·(−3) = 11`;
  - then `dest[0] = −r·dest[0] = −3·2 = −6`.
  - Result: `[−6, 11, −6, 1]` = `(X−1)(X−2)(X−3)`.

The inner loop runs high → low so `dest[k−1]` still holds its previous-iteration value when read — the shift-then-combine trick that keeps the update in place without a scratch buffer. The current algorithm needs a scratch buffer because `dest[k]` stores the final coefficient `(-1)^(n-k) · e_{n-k}` while its inner loop aggregates partial sums of a different shape; the optimized version keeps the partial polynomial `(X − r_0)···(X − r_i)` directly in `dest[0..i+1]`, so `dest[]` already has the right layout.

As a side benefit, `compute_linear_polynomial_product` is the only caller of `get_scratch_space<Fr>` ([`polynomial_arithmetic.cpp:21`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.cpp#L21)) — the static thread-shared buffer at the root of [issue-8](https://github.com/AztecProtocol/aztec-packages/issues/8). After this fix, `get_scratch_space` can be deleted outright, so one change delivers O(n^3) → O(n^2) cost, zero per-call allocation, and concurrency safety.

**Impact:** Informational (performance). Production callers via `compute_efficient_interpolation`:

| Caller | n |
|--------|---|
| `zk_sumcheck_data.hpp:230` (Libra interpolation, non-BN254 path) | Grumpkin SUBGROUP_SIZE = **87** |
| `small_subgroup_ipa.cpp:226` (ECCVM challenge polynomial, Grumpkin) | 87 |
| `small_subgroup_ipa.cpp:436` (monomial coefficients, Grumpkin) | 87 |
| Generic interpolation constructor (any future caller) | up to BN254 SUBGROUP_SIZE = **256** |

(BN254 ZK-Sumcheck takes the IFFT path, not this one.)

**Proof of Concept:** Integrated benchmark [`AuditPoC.P36_LinearPolyProductCubicVsQuadratic`](https://github.com/AztecProtocol/aztec-packages/blob/audit/qpzm/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.test.cpp#L775) in `polynomials/polynomial_arithmetic.test.cpp`. The test generates random roots, runs both implementations, verifies coefficient-by-coefficient equality and that `evaluate(dest, z) == \prod(z − r_i)`, then times 50 runs of each and reports the speedup.

Measured on an M-series Mac, release build:

```
P-36 n=87  (Grumpkin):   current = 307 μs    optimized = 35 μs    speedup = 8.7×
P-36 n=256 (BN254 subgroup): current = 7.1 ms   optimized = 0.30 ms  speedup = 23.4×
```

The speedup grows linearly with `n` as expected from O(n³) → O(n²).

Removing the scratch buffer also makes `compute_efficient_interpolation` reentrant, so today-sequential call sites become independently parallelizable:

| Site | Currently | After fix | Wall-time savings |
|------|-----------|-----------|-------------------|
| [`small_subgroup_ipa.cpp:336-357`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/commitment_schemes/small_subgroup_ipa/small_subgroup_ipa.cpp#L336) — `compute_lagrange_first_and_last` does 2 independent `compute_monomial_coefficients` calls (L_1 and L_{\|H\|}) | sequential | trivially parallel | ~50% of this function (~30 μs at n=87) |
| Batched proof generation (e.g., Chonk / folding pipelines) — multiple `SmallSubgroupIPAProver::prove()` instances across circuits | must run sequentially or risk corruption | each prover thread-safe | scales linearly with #circuits |

The mutex inside `get_scratch_space` also gives reviewers a false signal of thread safety, so the fix removes a long-term tripwire.

**Recommended Mitigation:** Replace the implementation with the incremental "multiply by `(X − r_i)`" loop (shown above). Same output, ~9× faster on production-sized inputs. Then delete `get_scratch_space<Fr>` from `polynomial_arithmetic.cpp` — it has no other callers.

**Aztec:**
Fixed in [044b745](https://github.com/AztecProtocol/aztec-packages/commit/044b745f678d854b1d446f1bfb53c58b8942b815).

**Cyfrin:** Verified.
