---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-3-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[L-02] Implementation is not making use of ERC721''s `burn` method'
vuln_class: []
---

# [L-02] Implementation is not making use of ERC721's `burn` method

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

The current implementation stores the LLZ NFT after a user withdraws his stake and it transfers it back to him on a subsequent deposit. It would be better if you burn the LLZ NFT on a withdraw and then re-mint it on subsequent deposit as this follows the usual best-practice pattern related to ERC721 NFTs, while the currently used one is error-prone.
