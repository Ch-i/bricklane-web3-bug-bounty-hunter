---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-core-v2-0-2-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-08-cyfrin-greekfi-core-v2-0
title: Public mapping accessors omit key and value names
vuln_class: []
---

# Public mapping accessors omit key and value names

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md)_

---

**Description:** The public `Factory::receipts, optionFor, permissions` and `Receipt::feeAccrued` mappings omit named key and value parameters. Their generated getters therefore expose less descriptive ABI metadata than the surrounding public interface.

**Recommended Mitigation:** Add descriptive key and value names to each mapping declaration, including both key levels of `permissions`.

**GreekFi:** Fixed in [PR35](https://github.com/greekfi/contracts/pull/35)

**Cyfrin:** Verified. The public mapping declarations now name their keys and return values, including both levels of permissions.
