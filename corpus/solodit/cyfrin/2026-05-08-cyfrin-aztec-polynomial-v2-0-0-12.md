---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-0-12
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-08-cyfrin-aztec-polynomial-v2-0
title: '`EvaluationDomain` move constructor leaves inconsistent state'
vuln_class: []
---

# `EvaluationDomain` move constructor leaves inconsistent state

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** The [move constructor](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/evaluation_domain.cpp#L125-L145) nullifies `other.roots` and moves the `round_roots` / `inverse_round_roots` vectors, but leaves `other.size`, `other.root`, `other.domain`, and the other scalar fields at their original nonzero values.

After move, the moved-from domain has `size > 0` (appears valid) but `roots == nullptr` and `round_roots` empty. Any subsequent FFT operation on the moved-from object dereferences null or accesses empty vectors.

Same issue in the [move assignment operator](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/evaluation_domain.cpp#L147-L172).

**Impact:** Low. In C++ move semantics, using a moved-from object is generally discouraged. But the partial invalidation (`size` still > 0) makes accidental reuse more dangerous than a fully-zeroed state — the object looks valid but crashes on use.

**Proof of Concept:** Integrated test [`AuditPoC_P18_EvalDomainMoveInconsistent`](https://github.com/AztecProtocol/aztec-packages/blob/7b19ca3983/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.test.cpp#L662) in `polynomials/polynomial_arithmetic.test.cpp`:

```cpp
TEST(polynomials, AuditPoC_P18_EvalDomainMoveInconsistent)
{
    using FF = bb::fr;

    constexpr size_t n = 16;
    auto domain = EvaluationDomain<FF>(n);
    domain.compute_lookup_table();

    // Save original values
    FF original_root = domain.root;

    // Move-construct a new domain
    auto moved = EvaluationDomain<FF>(std::move(domain));

    // moved should have the data
    EXPECT_EQ(moved.size, n);
    EXPECT_EQ(moved.root, original_root);
    EXPECT_NE(moved.get_round_roots().size(), 0UL);

    // Source domain: roots were moved out (nullptr), but size and root are NOT zeroed
    // This is inconsistent — size > 0 suggests a valid domain, but roots == nullptr
    std::cout << "P-18: After move, source domain.size = " << domain.size << std::endl;
    std::cout << "P-18: After move, source domain.root = " << domain.root << std::endl;
    std::cout << "P-18: After move, source domain round_roots count = "
              << domain.get_round_roots().size() << std::endl;

    bool inconsistent = (domain.size > 0) && (domain.get_round_roots().empty());
    if (inconsistent) {
        std::cout << "P-18 CONFIRMED: moved-from domain has size=" << domain.size
                  << " but empty round_roots" << std::endl;
    }
    EXPECT_TRUE(inconsistent);
}
```

```bash
cd barretenberg/cpp/build && ninja polynomials_tests
./bin/polynomials_tests --gtest_filter="*AuditPoC_P18*"
```

```
P-18: After move, source domain.size = 16
P-18: After move, source domain.root = ...
P-18: After move, source domain round_roots count = 0
P-18 CONFIRMED: moved-from domain has size=16 but empty round_roots
```

**Recommended Mitigation:** Make the moved-from object match the **default-constructed empty state** — i.e., restore the invariant `size > 0 → roots != nullptr`. Use `std::exchange` to both steal the field's value and zero the source in one expression:

```diff
 EvaluationDomain<Fr>::EvaluationDomain(EvaluationDomain&& other)
-    : size(other.size)
-    , num_threads(compute_num_threads(other.size))
-    , thread_size(other.size / num_threads)
-    , log2_size(static_cast<size_t>(numeric::get_msb(size)))
-    , log2_thread_size(static_cast<size_t>(numeric::get_msb(thread_size)))
-    , log2_num_threads(static_cast<size_t>(numeric::get_msb(num_threads)))
-    , generator_size(other.generator_size)
+    : size(std::exchange(other.size, 0))
+    , num_threads(std::exchange(other.num_threads, 0))
+    , thread_size(std::exchange(other.thread_size, 0))
+    , log2_size(std::exchange(other.log2_size, 0))
+    , log2_thread_size(std::exchange(other.log2_thread_size, 0))
+    , log2_num_threads(std::exchange(other.log2_num_threads, 0))
+    , generator_size(std::exchange(other.generator_size, 0))
     , root(other.root)
     , root_inverse(other.root_inverse)
-    , domain(Fr{ size, 0, 0, 0 }.to_montgomery_form())
-    , domain_inverse(domain.invert())
+    , domain(other.domain)
+    , domain_inverse(other.domain_inverse)
     , generator(other.generator)
     , generator_inverse(other.generator_inverse)
+    , roots(std::move(other.roots))            // shared_ptr move → other.roots = nullptr
+    , round_roots(std::move(other.round_roots))
+    , inverse_round_roots(std::move(other.inverse_round_roots))
 {
-    roots = other.roots;
-    round_roots = std::move(other.round_roots);
-    inverse_round_roots = std::move(other.inverse_round_roots);
-    // @audit move must not destruct the source
-    other.roots = nullptr;
 }
```

Apply the same pattern to the move assignment operator.

Reference pattern: [`BackingMemory::operator=(BackingMemory&&)`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/backing_memory.hpp#L78) already does this correctly — it nulls `other.raw_data` after stealing its target to preserve the invariant that `raw_data` mirrors the owning pointer. `EvaluationDomain` should mirror this discipline.

Why `std::exchange` is applied to these specific fields — two tiers:

- Must zero (`size`) — this is the only invariant-gating field. All validity checks on an `EvaluationDomain` gate on `size > 0`; zeroing it on move makes the source visibly empty and prevents any downstream code from treating the moved-from object as usable.
- Should zero for internal consistency (`num_threads`, `thread_size`, `log2_size`, `log2_thread_size`, `log2_num_threads`, `generator_size`) — these are derived from `size`. Setting `size = 0` but leaving `log2_size = 4` would be internally incoherent even though no code reads them without first checking `size`. Cheap to fix, keeps the moved-from state coherent.

The field elements (`root`, `domain`, `generator`, etc.) are not invariant-gating, so plain `other.root` is fine — zeroing them is defensive but adds noise. The `shared_ptr` and `vector` members use `std::move`, not `std::exchange`, because moving a `shared_ptr` already nulls the source and moving a `vector` already empties it.

**Aztec:**
Fixed in [cf988ed](https://github.com/AztecProtocol/aztec-packages/commit/cf988ed6f4801af41adab1e98d7d0ff771adb227).

**Cyfrin:** Verified.
