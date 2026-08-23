---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-11
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: Tier indexing is confusing
vuln_class: []
---

# Tier indexing is confusing

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** Throughout `MembershipERC1155`, the [highest tier](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L169-L175) membership is referred to with the lowest tier index. To consider an example, for a DAO with `6` tiers, the lowest index `0` should be passed to mint the highest tier membership while the highest index `6` should be passed to mint the lowest tier membership.

This is very confusing and can cause issues for users or third-party integrations. Consider reversing this convention such that the highest tier index corresponds to the highest tier membership, and vice versa.

**One World Project:** Intentional. Tier 0 (Tier 1 in website) is at the highest level. Tier 6 (Tier 7 in website) is lowest.

**Cyfrin:** Acknowledged.
