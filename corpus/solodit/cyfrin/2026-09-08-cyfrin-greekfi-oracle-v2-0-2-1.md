---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-oracle-v2-0-2-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-oracle-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-08-cyfrin-greekfi-oracle-v2-0
title: '`OracleReceipt` retains an unused commented-out `SCALE` declaration'
vuln_class: []
---

# `OracleReceipt` retains an unused commented-out `SCALE` declaration

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-oracle-v2.0.md)_

---

**Description:** `OracleReceipt` contains a commented-out `SCALE` constant declaration that is not part of the compiled pricing implementation. Retaining dead code beside active scale documentation can make it less clear which scaling factor the implementation actually uses.

**Recommended Mitigation:** Delete the commented-out declaration while retaining the explanatory comment about why the Morpho scale collapses to `1e18`.

**GreekFi:** Fixed in [PR38](https://github.com/greekfi/contracts/pull/38)

**Cyfrin:** Verified. The unused commented SCALE declaration has been removed from OracleReceipt.
