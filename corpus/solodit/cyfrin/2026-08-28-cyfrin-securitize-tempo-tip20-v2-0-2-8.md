---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-2-8
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-08-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-28-cyfrin-securitize-tempo-tip20-v2-0
title: '`deploy-full.ts` suppresses investor onboarding failures'
vuln_class: []
---

# `deploy-full.ts` suppresses investor onboarding failures

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** The deployment script appends an empty catch handler to investor registration and wallet addition. Any revert, including policy or authorization failure, is ignored and the script continues to print success.

**Impact:** A deployment can finish with the expected investor or wallet missing from the registry and TIP-403 policy.

**Recommended Mitigation:** Remove the blanket catch. Use read guards for expected already-completed states, propagate every other error, and verify the investor mapping and policy authorization before reporting success.

**Securitize:** Fixed in [PR 17](https://github.com/securitize-io/bc-tempo-sc/pull/17).

**Cyfrin:** Verified.
