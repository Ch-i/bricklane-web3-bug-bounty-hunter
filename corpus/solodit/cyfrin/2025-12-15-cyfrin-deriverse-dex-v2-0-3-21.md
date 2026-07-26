---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-21
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: wrong error emitted from `spot-order-cancel`
vuln_class: []
---

# wrong error emitted from `spot-order-cancel`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** Inside [spot-order-cancel](https://github.com/deriverse/protocol-v1/blob/30b06d2da69e956c000120cdc15907b5f33088d7/src/program/processor/spot_order_cancel.rs#L51), wrong error is emitted when accounts length is more than expected length, which is wrong and inconsistent with rest of the places.
```rust
    if accounts.len() < SpotOrderCancelInstruction::MIN_ACCOUNTS {
        //@audit wrong, should have been InvalidAccountsNumber
        bail!(InvalidDataLength {
            expected: SpotOrderCancelInstruction::MIN_ACCOUNTS,
            actual: accounts.len(),
        });
    }
```

**Impact:** wrong errors cause confusions and give hard time debugging underlying issue.

**Recommended Mitigation:** Replace it with
```rust
        bail!(InvalidAccountsNumber {
            expected: SpotMassCancelInstruction::MIN_ACCOUNTS,
            actual: accounts.len(),
        });
```

**Deriverse:** Fixed in commit : [4b2e123](https://github.com/deriverse/protocol-v1/commit/4b2e1230342c2ef474803c50a10dd34d46276376)

**Cyfrin:** verified.
