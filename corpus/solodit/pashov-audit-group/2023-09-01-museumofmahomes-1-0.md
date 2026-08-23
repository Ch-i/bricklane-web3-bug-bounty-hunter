---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-09-01-museumofmahomes-1-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-09-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-09-01-MuseumOfMahomes.md
tags:
- firm:pashov-audit-group
- report:2023-09-01-museumofmahomes
title: '[L-01] Reveal and Redeem should only be set to `true`'
vuln_class: []
---

# [L-01] Reveal and Redeem should only be set to `true`

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-09-01-MuseumOfMahomes.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-09-01-MuseumOfMahomes.md)_

---

Currently the `setRevealOpen` and `setRedeemOpen` methods allow setting the values to both `true` and `false` as many times as the `metadataOwner` decides to. This shouldn't be the case, as both should only be available to set to `true` just once, and never to `false` after this. Change the setters to methods that only set the values to `true`, removing the parameters from the methods.
