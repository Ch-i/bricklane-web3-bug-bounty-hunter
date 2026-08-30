---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: typo error in variables
vuln_class: []
---

# typo error in variables

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The variable `mint_token_prgoram_version` contains a typo: "prgoram" should be "program". This typo is repeated in the error message.

```rust

    let data = NewInstrumentData::new(instruction_data, root_state.tokens_count)?;
    let mint_token_prgoram_version = TokenProgram::new(asset_mint.owner)?;

    let token_program_version = TokenProgram::new(token_program.key)?;

    if token_program_version != mint_token_prgoram_version {
        bail!(DeriverseErrorKind::InvalidMintProgramId {
            expected: token_program_version,
            actual: mint_token_prgoram_version,
            mint_address: *asset_mint.key,
        });
    }
```



**Impact:** This does not affect functionality, it reduces code readability and consistency.

**Recommended Mitigation:** Rename the variable to mint_token_program_version:
```rust
-    let mint_token_prgoram_version = TokenProgram::new(asset_mint.owner)?;
+    let mint_token_program_version = TokenProgram::new(asset_mint.owner)?;

    let token_program_version = TokenProgram::new(token_program.key)?;

-    if token_program_version != mint_token_prgoram_version {
+    if token_program_version != mint_token_program_version {
        bail!(DeriverseErrorKind::InvalidMintProgramId {
            expected: token_program_version,
-            actual: mint_token_prgoram_version,
+            actual: mint_token_program_version,
            mint_address: *asset_mint.key,
        });
    }
```
**Deriverse:** Fixed in commit [a3c75ae8](https://github.com/deriverse/protocol-v1/commit/a3c75ae87eb1f7122b7be778223950aae3cd91b5).

**Cyfrin:** Verified.
