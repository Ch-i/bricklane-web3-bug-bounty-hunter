---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-core-v2-0-2-6
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
title: '`FlashExerciseKeeper` is illustrative but is not explicitly marked unsafe
  for production use'
vuln_class: []
---

# `FlashExerciseKeeper` is illustrative but is not explicitly marked unsafe for production use

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md)_

---

**Description:** The `FlashExerciseKeeper` snippet is labeled illustrative, and the surrounding NatSpec warns users to grant `Perm.EXERCISE` only to audited contracts. However, the example omits production checks and does not explicitly say it must not be deployed as-is. This is a documentation-hardening issue; the protocol contracts behave as specified.

**Recommended Mitigation:** Add a prominent `NOT PRODUCTION READY` warning stating that the snippet is pseudocode and must not be used in live deployments.

**GreekFi:** Fixed in [PR44](https://github.com/greekfi/contracts/pull/44)

**Cyfrin:** Verified. The keeper example is now explicitly marked as pseudocode that is not production-ready and must not be deployed as written.
