---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-15
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: EIP-712 name and project symbol are misaligned
vuln_class: []
---

# EIP-712 name and project symbol are misaligned

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** The [symbol](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L69) used for the `MembershipERC1155` token is `1WP`; however, `OWP` is used in the EIP-712 [name declaration](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/meta-transaction/NativeMetaTransaction.sol#L31).

This misalignment could be confusing for users signing messages thinking they are going to use `1WP` as the name. Consider using the same name as symbol, or vice versa.

**One World Project:** Made it OWP in [`ba3603a`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/ba3603ad8c4d976bdf1fa76ea3fb91e8ea1d4462).

**Cyfrin:** Verified. Token symbol is now `OWP`.
