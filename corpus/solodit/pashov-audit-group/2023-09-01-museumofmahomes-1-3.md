---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-09-01-museumofmahomes-1-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-09-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-09-01-MuseumOfMahomes.md
tags:
- firm:pashov-audit-group
- report:2023-09-01-museumofmahomes
title: '[L-04] Contract is not working as a state machine'
vuln_class: []
---

# [L-04] Contract is not working as a state machine

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-09-01-MuseumOfMahomes.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-09-01-MuseumOfMahomes.md)_

---

Currently it is possible for the `metadataOwner` to set the `redeemOpen` value to `true` while the `revealOpen` hasn't been set to `true` yet. There should be a sequence/flow of how the contract works - first minting, then revealing, then redeem (or redeem right after reveal). Allow setting `redeemOpen` to `true` only if `revealOpen == true`, and also allow setting `revealOpen` to `true` only when mint is completed (`totalSupply == MAX_SUPPLY`).
