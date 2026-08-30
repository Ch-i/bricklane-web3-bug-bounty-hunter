---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-15-cyfrin-veefriends-v2-0-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-15-cyfrin-veefriends-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-15-cyfrin-veefriends-v2-0
title: Unused internal functions should be removed to decrease bytecode size
vuln_class: []
---

# Unused internal functions should be removed to decrease bytecode size

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-15-cyfrin-veefriends-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-15-cyfrin-veefriends-v2.0.md)_

---

**Description:** The internal functions `_safeMint()`, `_safeMintBatch()`, `_airdrop()`, `_mintBatch()`, and `_burn()`, do not appear to be used and it is understood that there is not currently any requirement for additional functionality to be added to `VFTokenC`. The contracts are not upgradeable, so a separate deployment would be needed for any future upgrade, meaning that these functions should most likely be excluded from the current release to decrease the bytecode size.

**VeeFriends:** Fixed in commits [dc834fa](https://github.com/veefriends/smart-contracts-v2/commit/dc834fad574e9f7caf460ba5eae2983f8d0e4488) and [ed976c6](https://github.com/veefriends/smart-contracts-v2/commit/ed976c671033b145b9055337218196dfb2e642ae).

**Cyfrin:** Verified.

\clearpage
