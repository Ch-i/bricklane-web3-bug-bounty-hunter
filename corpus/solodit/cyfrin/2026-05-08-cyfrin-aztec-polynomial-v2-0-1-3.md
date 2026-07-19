---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-1-3
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
title: '`fft_inner_parallel` unsafe when `coeffs == target`'
vuln_class: []
---

# `fft_inner_parallel` unsafe when `coeffs == target`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** In [`polynomial_arithmetic.cpp:86-93`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.cpp#L86), phase 1 of `fft_inner_parallel` reads from `coeffs[swap_index]` (bit-reversed) and writes to `target[i]` (sequential):

```cpp
Fr::__copy(coeffs[swap_index_1], temp_1);   // read from bit-reversed index
Fr::__copy(coeffs[swap_index_2], temp_2);
target[i + 1] = temp_1 - temp_2;            // write to sequential index
target[i] = temp_1 + temp_2;
```

If `coeffs == target` (same pointer), the bit-reversed read at `swap_index` could access an element that was already overwritten by a previous iteration's sequential write. For example with `n=8`:

```
i=0: writes target[0], target[1]
i=2: reads coeffs[reverse(2)] = coeffs[2] ← OK (not yet written)
     reads coeffs[reverse(3)] = coeffs[6] ← OK
     writes target[2], target[3]
i=4: reads coeffs[reverse(4)] = coeffs[1] ← ALREADY OVERWRITTEN at i=0!
```

The function signature accepts separate `Fr* coeffs` and `Fr* target` pointers but does not assert they are different.

**Impact:** Informational. In UltraHonk, `ifft` is only called in ZK sumcheck Libra ([`zk_sumcheck_data.hpp:233`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/sumcheck/zk_sumcheck_data.hpp#L233)) and small subgroup IPA ([`small_subgroup_ipa.cpp:439`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/commitment_schemes/small_subgroup_ipa/small_subgroup_ipa.cpp#L439)), both on `SUBGROUP_SIZE = 256` with separate input/output buffers. The function signature permits aliasing, and a future caller passing the same buffer would get silently wrong results.

**Proof of Concept:** [`AuditPoC_P32_FftInPlaceAliasing`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.test.cpp#L620) in `polynomial_arithmetic.test.cpp`:

```cpp
TEST(AuditPoC, P32_FftInPlaceAliasing)
{
    using FF = bb::fr;
    constexpr size_t n = 16;

    auto domain = bb::EvaluationDomain<FF>(n);
    domain.compute_lookup_table();

    std::array<FF, n> coeffs;
    for (size_t i = 0; i < n; i++) {
        coeffs[i] = FF::random_element();
    }

    // Correct: separate input/output buffers
    std::array<FF, n> correct_output;
    std::array<FF, n> coeffs_copy;
    std::copy(coeffs.begin(), coeffs.end(), coeffs_copy.begin());
    polynomial_arithmetic::fft_inner_parallel(
        coeffs_copy.data(), correct_output.data(), domain, domain.root, domain.get_round_roots());

    // Buggy: in-place (coeffs == target)
    std::array<FF, n> aliased;
    std::copy(coeffs.begin(), coeffs.end(), aliased.begin());
    polynomial_arithmetic::fft_inner_parallel(
        aliased.data(), aliased.data(), domain, domain.root, domain.get_round_roots());

    // In-place produces different (wrong) results
    bool mismatch = false;
    for (size_t i = 0; i < n; i++) {
        if (correct_output[i] != aliased[i]) {
            mismatch = true;
            break;
        }
    }
    EXPECT_TRUE(mismatch);
}
```

**Recommended Mitigation:** In [`polynomial_arithmetic.cpp:74`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.cpp#L74):

```diff
 void fft_inner_parallel(
     Fr* coeffs, Fr* target, const EvaluationDomain<Fr>& domain, const Fr&, const std::vector<Fr*>& root_table)
 {
+    BB_ASSERT(coeffs != target, "fft_inner_parallel does not support in-place operation");
```

**Aztec:**
Fixed in [80131f6](https://github.com/AztecProtocol/aztec-packages/commit/80131f6906d0c5e0ac9f55f2d40a00757899c7c4).

**Cyfrin:** Verified.
