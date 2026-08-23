---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Eligible intruments may not be propagated
vuln_class: []
---

# Eligible intruments may not be propagated

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The function `dividends_allocation` currently throws error when encountering an instrument whose `distrib_time` has not yet passed the 1-hour threshold:
```rust
        } else {
            //@audit instead of returning we should have continued to another instr
            bail!(TooEarlyToDistribFunds {
                limit_time: instr_state.header.distrib_time,
                current_time: time,
            });
        }
```
This immediately terminates the entire dividends allocation process, even if subsequent instruments in the same transaction are eligible for distribution.
As a result, valid instruments are skipped.

**Impact:** Eligible instruments in the same batch are not processed.

**Recommended Mitigation:** Instead of bailing, we should continue to the next instrument in the loop:
```rust
if time > instr_state.header.distrib_time + HOUR {
    // distribute funds
} else {
    // skip this instrument, continue to next
    continue;
}
```
**Deriverse**
Fixed in commit [ca593e2](https://github.com/deriverse/protocol-v1/commit/ca593e2bc30b93a7a4a53c69ceb5b91a282c8955).

**Cyfrin:** Verified.
