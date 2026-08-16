---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Incorrect Price Validation When Creating `NewInstrumentData` Struct during
  `NewInstrumentInstruction` instruction
vuln_class: []
---

# Incorrect Price Validation When Creating `NewInstrumentData` Struct during `NewInstrumentInstruction` instruction

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The current validation logic when creating `NewInstrumentData` using `new` method during `NewInstrumentInstruction` instruction uses an exclusive upper bound when checking the price field. As a result, a price equal to MAX_PRICE is incorrectly rejected even though it should be considered valid.

```rust
    fn new(instruction_data: &[u8], tokens_count: u32) -> Result<&Self, DeriverseError> {
        let data = bytemuck::try_from_bytes::<Self>(instruction_data)
            .map_err(|_| drv_err!(InvalidClientDataFormat))?;

        if data.crncy_token_id >= tokens_count {
            bail!(InvalidTokenId {
                id: data.crncy_token_id,
            })
        }

        if !(MIN_PRICE..MAX_PRICE).contains(&data.price) {                  //<- HERE
            bail!(InvalidPrice {
                price: data.price,
                min_price: MIN_PRICE,
                max_price: MAX_PRICE,
            })
        }

        return Ok(data);
    }
```

In Rust, the syntax a..b defines a range that excludes the upper bound(b), whereas a..=b defines an inclusive range that allows b as a valid value.


**Impact:** This bug prevents legitimate instruments with a price equal to MAX_PRICE from being created.

**Recommended Mitigation:** To fix this issue, the validation should use an inclusive range (a..=b) so that prices equal to MAX_PRICE pass the check.
```rust
    fn new(instruction_data: &[u8], tokens_count: u32) -> Result<&Self, DeriverseError> {
        let data = bytemuck::try_from_bytes::<Self>(instruction_data)
            .map_err(|_| drv_err!(InvalidClientDataFormat))?;

        if data.crncy_token_id >= tokens_count {
            bail!(InvalidTokenId {
                id: data.crncy_token_id,
            })
        }

        if !(MIN_PRICE..=MAX_PRICE).contains(&data.price) {                  //<- HERE
            bail!(InvalidPrice {
                price: data.price,
                min_price: MIN_PRICE,
                max_price: MAX_PRICE,
            })
        }

        return Ok(data);
    }
```


**Deriverse:** Fixed in commit [aa6136](https://github.com/deriverse/protocol-v1/commit/aa613649a9dcd3394890a03e964a6d2b6b6570ad).

**Cyfrin:** Verified.
