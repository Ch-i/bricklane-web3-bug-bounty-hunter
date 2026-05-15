---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-2-15
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: '`get_by_tag` tries to access out of bound index'
vuln_class: []
---

# `get_by_tag` tries to access out of bound index

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The [get_by_tag](https://github.com/deriverse/protocol-v1/blob/30b06d2da69e956c000120cdc15907b5f33088d7/src/program/constants.rs#L4) contains an off-by-one error in its loop condition. The function iterates using [while i <= continer.candles.len()](https://github.com/deriverse/protocol-v1/blob/30b06d2da69e956c000120cdc15907b5f33088d7/src/program/constants.rs#L9) instead of the correct [while i < continer.candles.len()](), causing an out-of-bounds array access when iterating past the last valid index.
```rust
pub const fn get_by_tag<const TAG: u32>(
    continer: CandleRegister,
) -> Result<CandleParams, DeriverseError> {
    let mut i = 0;

    while i <= continer.candles.len() {  // BUG: should be `<` not `<=`
        if continer.candles[i].tag == TAG {  // Out-of-bounds when i == len
            return Ok(continer.candles[i]);
        }
        i += 1;
    }
    // ...
}
```
This function is called throughout the codebase in different candle-related operations & all paths are affected.  The bug may not manifest during normal operations if the TAG is found early in the array, It will panic when i == len() due to out-of-bounds indexing rather than returning normal error
```rust
    Err(DeriverseError {
        error: DeriverseErrorKind::CandleWasNotFound { tag: TAG },
        location: ErrorLocation {
            file: file!(),
            line: line!(),
        },
    })
```

**Impact:** When the requested TAG is not found before the loop exhausts, or when i reaches [continer.candles.len()](), the code attempts to access memory beyond the array bounds and hence will cause program to panic rather than throwing proper error.

**Recommended Mitigation:**
```rust
pub const fn get_by_tag<const TAG: u32>(
    continer: CandleRegister,
) -> Result<CandleParams, DeriverseError> {
    let mut i = 0;

    while i < continer.candles.len() {  // Fixed: use `<` instead of `<=`
        if continer.candles[i].tag == TAG {
            return Ok(continer.candles[i]);
        }
        i += 1;
    }

    Err(DeriverseError {
        error: DeriverseErrorKind::CandleWasNotFound { tag: TAG },
        location: ErrorLocation {
            file: file!(),
            line: line!(),
        },
    })
}
```
**Deriverse:** Fixed in commit: [4e88698](https://github.com/deriverse/protocol-v1/commit/4e8869833c3de69ad84ed5b9f32fff3b560c5b93)

**Cyfrin:** Verified.
