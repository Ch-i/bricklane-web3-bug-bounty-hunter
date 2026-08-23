---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Use the `transient` keyword instead of low-level assembly
vuln_class: []
---

# Use the `transient` keyword instead of low-level assembly

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** As of Solidity v0.8.30, transient storage is accessible via the [transient](https://www.aarc-xyz.io/glossary/storage-solidity) keyword for value types (e.g., uint256, bool).

Hence declare variables using the `transient` keyword where required instead of using low-level assembly. Affected contracts:
* `IBTCY::IS_FORCE_TRANSFERRING_SLOT`

**Aarc:** Fixed in commit [529ff75](https://github.com/aarc-xyz/btcy-contracts-main/commit/529ff7513dbc147340534dbf4677373a1ee2ac70).

**Cyfrin:** Verified.
