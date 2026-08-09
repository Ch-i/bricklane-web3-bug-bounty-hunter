---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-14
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: DAO creators cannot freely update membership configuration
vuln_class: []
---

# DAO creators cannot freely update membership configuration

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** While `MembershipFactory::updateDAOMembership` is intended to update the tier configurations for a specific DAO, this function can only be called by the [permissioned](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L95) `EXTERNAL_CALLER` role. As such, DAO creators cannot freely update membership configuration without coordination of the `EXTERNAL_CALLER` role.

**Recommended Mitigation:** Allow DAO creators to freely update the membership configuration for their DAOs.

**One World Project:** DAO creators are not supposed to have that access directly.

**Cyfrin:** Acknowledged.
