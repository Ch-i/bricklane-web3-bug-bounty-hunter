---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-04-cyfrin-solidly-v2-memecore-v2-2-2-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-05-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md
tags:
- firm:cyfrin
- report:2024-05-04-cyfrin-solidly-v2-memecore-v2-2
title: Lock creation can be front-run
vuln_class: []
---

# Lock creation can be front-run

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md)_

---

**Description:** `SolidlyV2ERC42069::lockToken` can be front-run with the transfer of a dust lock. This would cause the index at which the lock is created to be different from what the sender expected when sending the transaction.

In the worst case, this could cause the wrong lock to be withdrawn, extended, or split. If the sender is attentive, this can be easily remedied, but it could waste the gas cost for one TX.

**Impact:** The index at which a lock is created/split/transferred can be something other than expected.

**Recommended Mitigation:** Consider mentioning in the documentation that the user needs to use the events emitted to verify at which index their lock was created.

**Solidly Labs:** Acknowledged.

**Cyfrin:** Acknowledged.

\clearpage
