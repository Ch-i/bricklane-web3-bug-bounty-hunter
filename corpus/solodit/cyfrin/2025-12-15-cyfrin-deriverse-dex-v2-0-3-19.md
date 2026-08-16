---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-19
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
title: Incorrect Token Program Error Message in Airdrop Flow
vuln_class: []
---

# Incorrect Token Program Error Message in Airdrop Flow

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The airdrop instruction correctly enforces that DRVS tokens must use the `Token‑2022` program, but the error message suggests the opposite. This inconsistency can mislead operators when diagnosing configuration mistakes.

```rust
if check_spl_token(...) ? {
    let token_program_version = TokenProgram::new(token_program.key)?;
    bail!(InvalidTokenProgramId {
        expected: TokenProgram::Original,
        actual: token_program_version,
    });
}
```

The bailout is correct: the code later calls `spl_token_2022::instruction::transfer_checked`, so Token‑2022 is required. However, the error message reports `expected: TokenProgram::Original`, which is the *rejected* option.

**Impact:** Operators who misconfigure the mint/program pair will see an error stating that “Original” was expected even though the instruction actually expects Token‑2022.


**Recommended Mitigation:** Update the `InvalidTokenProgramId` message to reflect the real expectation.

**Deriverse:** Fixed in commit [40043ae](https://github.com/deriverse/protocol-v1/commit/40043aeec9d5e731544e6c0b36b766690e7b9c55).

**Cyfrin:** Verified.
