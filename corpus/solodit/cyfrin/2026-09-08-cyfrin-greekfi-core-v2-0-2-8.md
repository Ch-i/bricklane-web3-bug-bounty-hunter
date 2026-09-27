---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-core-v2-0-2-8
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
title: Index key fields in Exercise, Expire, and Swept events
vuln_class: []
---

# Index key fields in Exercise, Expire, and Swept events

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md)_

---

**Description:** `Exercise` and `Expire` do not index either account, while `Swept` indexes only `caller`. Indexers cannot filter these logs by holder, keeper, token, or recipient without fetching and decoding every event from each clone.

**Impact:** No contract behavior or funds are affected. Monitoring and accounting are less efficient.

**Recommended Mitigation:** Index `caller` and `holder` in `Exercise`; index either account field in `Expire`, since both are always equal; and index `token` and `recipient` in `Swept`.

**GreekFi:** Fixed in [PR43](https://github.com/greekfi/contracts/pull/43)

**Cyfrin:** Verified. Exercise, Expire, and Swept now index the relevant caller, holder, recipient, and token fields.

\clearpage
