---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-23-cyfrin-strata-shares-cooldown-v2-0-2-9
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-01-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-23-cyfrin-strata-shares-cooldown-v2-0
title: Misleading owner field in OnMetaWithdraw event
vuln_class: []
---

# Misleading owner field in OnMetaWithdraw event

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md)_

---

**Description:** `OnMetaWithdraw` event emit receiver as the first argument, while the parameter is named owner. Since owner, caller, and receiver can differ, this semantic mismatch may mislead off-chain indexers

**Recommended Mitigation:** Rename the event parameter to receiver, or include both owner and receiver explicitly

**Strata:** Fixed in commit [1021020](https://github.com/Strata-Money/contracts-tranches/commit/1021020ab866177f8570aa28494f0f7a03a1b091).

**Cyfrin:** Verified.

\clearpage
