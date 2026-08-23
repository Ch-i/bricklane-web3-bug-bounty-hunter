---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-2-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[M-04] Constraining approvals only partially limits the NFTs from being sold'
vuln_class: []
---

# [M-04] Constraining approvals only partially limits the NFTs from being sold

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

**Impact:**
High, as it can lead to scams and bugs when integrating with other games/protocols

**Likelihood:**
Low, as such sales or integrations are not currently expected to happen and because information about this is present in the docs

**Description**

Constraints on approvals (the `onlyApprovedContracts` modifier) were added so that the `Locked Lizards` NFTs can't be sold in marketplaces like OpenSea, Blur etc. This only partially limits selling the NFTs because users can always do OTC trades. Those trades will be scams though, since the original NFT owner can call `retractLockedLizard` anytime and re-gain ownership of the NFT. Not only sales will be problematic, but for example integrations with NFT games - the games are not expected to work properly with NFTs that can be retracted, as this opens up multiple attack-vectors.

**Recommendations**

Either remove the `onlyApprovedContracts` modifier and allow sales and integrations by removing the `retractLockedLizard` functionality, or just forbid the `approve` and `transfer` functionality altogether as otherwise they can result in problems.
