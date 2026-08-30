---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-3
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
title: Entrypoint panics on empty `instruction_data`
vuln_class: []
---

# Entrypoint panics on empty `instruction_data`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The issue originates from a missing bounds check for the `instruction_data` array before accessing its first element during opcode dispatch.

```rust
entrypoint!(process_instruction);

pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    match instruction_data[0] {
        NewHolderInstruction::INSTRUCTION_NUMBER => new_holder_account(program_id, accounts)?,
        NewOperatorInstruction::INSTRUCTION_NUMBER => {
            new_operator(program_id, accounts, instruction_data)?
        }
```


**Impact:** This can result in an out-of-bounds read and program panic when `instruction_data` is empty instead of exiting gracefully with correct error message.

**Recommended Mitigation:** To mitigate this vulnerability, the program should validate the length of `instruction_data` before accessing entries, and handle the error gracefully instead of resorting to a crash.

**Deriverse:** Fixed in commit [8a2bd16](https://github.com/deriverse/protocol-v1/commit/8a2bd16db9fd84126fdf58c7f7eeb7b13410ba54).

**Cyfrin:** Verified.
