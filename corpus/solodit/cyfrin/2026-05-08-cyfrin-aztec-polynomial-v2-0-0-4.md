---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-0-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-05-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-08-cyfrin-aztec-polynomial-v2-0
title: '`get_scratch_space` shared buffer unsafe under concurrent FFTs'
vuln_class: []
---

# `get_scratch_space` shared buffer unsafe under concurrent FFTs

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** In [`polynomial_arithmetic.cpp:21`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.cpp#L21), `get_scratch_space` returns a `shared_ptr` to a **single static buffer** reused across sequential calls to avoid repeated allocation. The mutex protects allocation but does **not** prevent two concurrent threads from receiving the same buffer and writing to it simultaneously.

```cpp
template <typename Fr> std::shared_ptr<Fr[]> get_scratch_space(const size_t num_elements)
{
    static std::mutex scratch_mutex;
    std::lock_guard lock(scratch_mutex);          // only protects allocation
    static std::shared_ptr<Fr[]> working_memory = nullptr;
    static size_t current_size = 0;
    if (num_elements > current_size) {
        working_memory = std::make_shared<Fr[]>(num_elements);
        current_size = num_elements;
    }
    return working_memory;                        // returns same pointer to all callers
}
```

The lock serializes the allocation but not the **usage**. Both threads get a `shared_ptr` to the same underlying array and write butterfly results into overlapping indices, corrupting each other's output.

Note: [PR22306](https://github.com/AztecProtocol/aztec-packages/pull/22306) (`20392b77aa`) added this `std::mutex` to `get_scratch_space` to protect the allocation logic. However, this only serializes the check-and-allocate step — the **concurrent usage** issue (two callers receiving the same buffer) remains unfixed.

**Impact:** Low. This is a reproducible data corruption with PoC (50/50 trials corrupted). In barretenberg's current architecture, FFTs are not called concurrently — `parallel_for` parallelizes within a single FFT. The shared scratch buffer is safe under this assumption, but the code does not enforce it and the mutex gives a false sense of thread safety.

**Proof of Concept:** [`AuditPoC_P30_ScratchSpaceConcurrentCorruption`](https://github.com/AztecProtocol/aztec-packages/blob/audit/qpzm/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.test.cpp#L528) in `polynomial_arithmetic.test.cpp`:

```cpp
TEST(AuditPoC, P30_ScratchSpaceConcurrentCorruption)
{
    using FF = bb::fr;
    constexpr size_t n = 256;

    std::vector<FF> roots_a(n), roots_b(n);
    for (size_t i = 0; i < n; i++) {
        roots_a[i] = FF(i + 1);
        roots_b[i] = FF(i + 1000);
    }
    std::vector<FF> dest_a(n + 1), dest_b(n + 1);
    std::vector<FF> ref_a(n + 1), ref_b(n + 1);
    polynomial_arithmetic::compute_linear_polynomial_product(roots_a.data(), ref_a.data(), n);
    polynomial_arithmetic::compute_linear_polynomial_product(roots_b.data(), ref_b.data(), n);

    constexpr size_t num_trials = 50;
    size_t corruption_count = 0;
    for (size_t trial = 0; trial < num_trials; trial++) {
        std::atomic<bool> go{ false };
        std::thread thread_a([&]() { while (!go.load()) {} polynomial_arithmetic::compute_linear_polynomial_product(roots_a.data(), dest_a.data(), n); });
        std::thread thread_b([&]() { while (!go.load()) {} polynomial_arithmetic::compute_linear_polynomial_product(roots_b.data(), dest_b.data(), n); });
        go.store(true);
        thread_a.join();
        thread_b.join();
        bool ok = true;
        for (size_t i = 0; i <= n; i++) { if (dest_a[i] != ref_a[i] || dest_b[i] != ref_b[i]) ok = false; }
        if (!ok) corruption_count++;
    }
    // corruption_count == 50/50
}
```

```bash
cd barretenberg/cpp/build && ninja polynomials_tests
./bin/polynomials_tests --gtest_filter="*P30*"
```

```
P-30: 50/50 trials had corrupted results
P-30 CONFIRMED: concurrent scratch space usage causes data corruption
```

**Parallelization Opportunities Currently Blocked**

`get_scratch_space` is reachable only via the call chain:

```
get_scratch_space
  └── compute_linear_polynomial_product       (only caller)
        └── compute_efficient_interpolation   (only caller)
              ├── Polynomial(span, span, vsize) interpolation constructor
              ├── SmallSubgroupIPAProver::compute_eccvm_challenge_polynomial    (small_subgroup_ipa.cpp:226)
              ├── SmallSubgroupIPAProver::compute_monomial_coefficients         (small_subgroup_ipa.cpp:436)
              └── ZKSumcheckData::compute_concatenated_libra_polynomial         (zk_sumcheck_data.hpp:230)
```

All four reachable sites currently run sequentially because the shared scratch buffer makes concurrent invocation unsafe. Once this finding is fixed, the following call sites become legally parallelizable:

| Site | Current | After fix | Estimated savings |
|------|---------|-----------|-------------------|
| [`small_subgroup_ipa.cpp:336-357`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/commitment_schemes/small_subgroup_ipa/small_subgroup_ipa.cpp#L336) — `compute_lagrange_first_and_last` makes two independent `compute_monomial_coefficients` calls (L_1 and L_{\|H\|}) | sequential | trivially parallel | ~50% of this function (~30 μs at n=87) |
| `SmallSubgroupIPAProver::prove()` over multiple proofs (Chonk / folding pipelines, batched circuits) | one prover at a time | concurrent provers | scales linearly with #circuits |
| Future Lagrange-batched routines (e.g., constructing several `Polynomial(points, evals_i, vsize)` inside a `parallel_for`) | unsafe — silently corrupts | safe | depends on caller |

Sites NOT blocked (for completeness):
- Gemini's `compute_fold_polynomials` (`gemini_impl.hpp:124-157`) — has a hard data dependency across folds (A_{l+1} depends on A_l). Already uses `parallel_for_heuristic` *within* each fold, which is the only parallelism that algorithm admits.
- Shplonk's per-claim quotient batching (`shplonk.hpp:75-117`) — uses `factor_roots`, not `compute_efficient_interpolation`. Independent per claim and could be parallelized as a separate optimization, but isn't blocked by this finding.

The largest practical payoff is the second row above: enabling Chonk/folding pipelines to safely invoke independent `SmallSubgroupIPAProver` instances concurrently. The mutex inside `get_scratch_space` even gives reviewers a *false signal* of thread safety, so the fix also removes a long-term tripwire — the natural "wrap a `compute_efficient_interpolation` loop in `parallel_for`" refactor would silently corrupt proofs today.

**Recommended Mitigation:** Give each thread its own buffer with `thread_local`:

```cpp
template <typename Fr> std::shared_ptr<Fr[]> get_scratch_space(const size_t num_elements)
{
    thread_local std::shared_ptr<Fr[]> working_memory = nullptr;
    thread_local size_t current_size = 0;
    if (num_elements > current_size) {
        working_memory = std::make_shared<Fr[]>(num_elements);
        current_size = num_elements;
    }
    return working_memory;
}
```

Note: a deeper fix that removes `get_scratch_space` entirely — by rewriting `compute_linear_polynomial_product` in place — is tracked separately as [issue-21](https://github.com/AztecProtocol/aztec-packages/issues/21). That rewrite would also close the concurrency concern here as a side effect.

**Aztec:**
Fixed in [044b745](https://github.com/AztecProtocol/aztec-packages/commit/044b745f678d854b1d446f1bfb53c58b8942b815).

**Cyfrin:** Verified.
