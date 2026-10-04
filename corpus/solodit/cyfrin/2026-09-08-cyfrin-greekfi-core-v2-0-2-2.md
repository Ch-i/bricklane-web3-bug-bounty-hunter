---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-core-v2-0-2-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-08-cyfrin-greekfi-core-v2-0
title: Unused declarations remain in `Factory` and `Option`
vuln_class: []
---

# Unused declarations remain in `Factory` and `Option`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md)_

---

**Description:** `Factory::createOption` declares the named return variable `option_` but returns the result of `createOption2` directly without assigning that variable. Separately, `Option` imports `IERC20` without using the symbol. These declarations add noise without affecting the compiled behavior.

**Recommended Mitigation:** Make the `Factory::createOption` return value unnamed and remove the unused `IERC20` import from `Option`.

**GreekFi:** Fixed in [PR33](https://github.com/greekfi/contracts/pull/33)

**Cyfrin:** Verified. The unused createOption return name and unused IERC20 import have been removed.
