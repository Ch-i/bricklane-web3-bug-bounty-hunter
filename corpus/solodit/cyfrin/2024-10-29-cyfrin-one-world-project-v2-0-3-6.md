---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-6
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: Upgrading DAO tier emits same event as minting the same tier
vuln_class: []
---

# Upgrading DAO tier emits same event as minting the same tier

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** If a DAO is registered as SPONSORED, its members can upgrade their membership tier by burning two lower tier tokens for one higher tier token in a call to `MembershipFactory::upgradeTier`.

This will [emit](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L143) the `UserJoinedDAO` event which is the same as that emitted when joining a DAO for the first time, making it impossible to differentiate between these two actions.

**Recommended Mitigation:** Consider emitting a separate event when a DAO member upgrades their tier.

**One World Project:** Upgrading mints a new token in a new tier, so same event is kept to track events efficiently in backend.

**Cyfrin:** Acknowledged.
