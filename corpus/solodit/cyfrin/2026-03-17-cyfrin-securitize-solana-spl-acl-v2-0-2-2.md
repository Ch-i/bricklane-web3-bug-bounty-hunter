---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0-2-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0
title: Several error variants are defined but currently unused
vuln_class: []
---

# Several error variants are defined but currently unused

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md)_

---

**Description:** The error enum currently contains several variants that appear unused across the program logic and tests, including `SameAuthority`, `InvalidProgram`, `InvalidMint`, `InsufficientBalance`, `MissingMintConfig`, `MissingTokenAcl`, and `InvalidMintConfig`.

The clearest example is `SameAuthority`: `set_authority` does not use it to reject no-op transfers where the new authority equals the current authority. The other variants look like dead-code placeholders or validation branches that were planned but never wired into instruction handlers.

**Recommended Mitigation:** Either wire these variants into real validation paths or remove them so the error surface matches actual program behavior.

**Securitize:** Fixed in [29df9ca](https://github.com/securitize-io/bc-solana-spl-acl-sc/commit/29df9cafd0cbe0e47890814f43c6863bb00316d4).

**Cyfrin:** Verified.
