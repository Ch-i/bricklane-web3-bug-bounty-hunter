---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-0-5
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-08-cyfrin-aztec-polynomial-v2-0
title: '`parse_size_string` does not check for overflow in `value * multiplier`'
vuln_class: []
---

# `parse_size_string` does not check for overflow in `value * multiplier`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** `parse_size_string()` in `backing_memory.cpp` parses a human-readable size string (e.g., `"500m"`, `"2g"`) into a byte count. After extracting the numeric value via `std::stoull` and selecting the appropriate multiplier based on the suffix, it returns the product `value * multiplier` without checking whether that multiplication overflows `size_t`. On a 64-bit system, `size_t` is 8 bytes, and `value * multiplier` silently wraps modulo 2^64.

```cpp
// backing_memory.cpp, lines 33-73
size_t parse_size_string(const std::string& size_str)
{
    if (size_str.empty()) {
        return std::numeric_limits<size_t>::max();
    }

    try {
        std::string str = size_str;
        char suffix = static_cast<char>(std::tolower(static_cast<unsigned char>(str.back())));
        size_t multiplier = 1;

        if (suffix == 'k') {
            multiplier = 1024ULL;
            str.pop_back();
        } else if (suffix == 'm') {
            multiplier = 1024ULL * 1024ULL;
            str.pop_back();
        } else if (suffix == 'g') {
            multiplier = 1024ULL * 1024ULL * 1024ULL;
            str.pop_back();
        } else if (std::isdigit(static_cast<unsigned char>(suffix)) == 0) {
            throw_or_abort("Invalid storage size format: ...");
        }

        if (str.empty()) {
            throw_or_abort("Invalid storage size format: ...");
        }

        size_t value = std::stoull(str);
        return value * multiplier;   // <--- unchecked overflow
    } catch (...) { ... }
}
```

For example, `"18014398509481984k"` parses as `value = 2^54` and `multiplier = 1024 = 2^10`. The product is `2^64`, which wraps to `0`. The storage budget is then set to `0`, causing all subsequent file-backed allocations to fail the budget check and silently fall back to RAM.

**Impact:** An operator specifying a large `BB_STORAGE_BUDGET` env var value gets a silently tiny budget. All file-backed allocations fail, falling back to RAM. There is no memory safety issue; the consequence is unexpected performance behavior (RAM instead of mmap), not corruption. The env var is set by trusted operators, not attacker-controlled.

This is operator-controlled configuration. It is suitable as a Low severity reliability issue, not an externally exploitable security issue.

**Proof of Concept:** At the shell level:

```bash
# Operator intends to set a very large budget:
BB_SLOW_LOW_MEMORY=1 BB_STORAGE_BUDGET="18014398509481984k" ./bb prove ...
# Internally: 18014398509481984 * 1024 = 2^64, wraps to 0. storage_budget = 0
# In low-memory mode, any required_bytes > 0 causes the file-backed admission
# check to fail, silently falling back to aligned heap memory.
```

```cpp
TEST(LowFindings, ECA_04_ParseSizeStringOverflow)
{
    // Sanity: well-formed inputs parse correctly.
    EXPECT_EQ(parse_size_string("1k"), 1024u);
    EXPECT_EQ(parse_size_string("2g"), 2ULL * 1024 * 1024 * 1024);

    // 2^54 * 1024 == 2^64 → wraps to 0 silently. An operator who set
    // BB_SLOW_LOW_MEMORY=1 BB_STORAGE_BUDGET=18014398509481984k would actually
    // get a budget of 0 bytes, disabling all file-backed allocation.
    EXPECT_EQ(parse_size_string("18014398509481984k"), 0u);
}
```

**Recommended Mitigation:** Add an overflow guard before the multiplication:

```cpp
size_t value = std::stoull(str);
if (value > std::numeric_limits<size_t>::max() / multiplier) {
    throw_or_abort("Storage size overflows: '" + size_str + "'");
}
return value * multiplier;
```

**Aztec:**
Fixed in [87513f8](https://github.com/AztecProtocol/aztec-packages/commit/87513f8bffb880276c560bea2d8c540a8fa94945).

**Cyfrin:** Verified.
