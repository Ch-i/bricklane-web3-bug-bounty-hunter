---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-1-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: DAO members have no option to leave
vuln_class: []
---

# DAO members have no option to leave

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** `MembershipFactory` exposes methods to join a DAO and upgrade tiers within a `SPONSORED` type DAO; however, there is no logic directly exposed to DAO members to burn their membership token(s) if they decide to leave the DAO. The only role with permissions to execute this is `EXTERNAL_CALLER` who can do so on behalf of the user, presumably at their request.

**Impact:** DAO members cannot leave without the cooperation of `EXTERNAL_CALLER`.

**Recommended Mitigation:** Consider exposing burn logic directly to DAO members so they have the option to leave.

**One World Project:** There is intentionally no process in place for a member to exit the DAO as per business logic. They can be removed by burning their Membership NFTs through off-chain process by the `EXTERNAL_CALLER`.

**Cyfrin:** Acknowledged. This dependency introduces additional risks, and we recommend ensuring the off-chain service meets stringent security standards.

\clearpage
