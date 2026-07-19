---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-09-01-museumofmahomes-1-1
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
title: '[L-02] All state-changing methods should emit events'
vuln_class: []
---

# [L-02] All state-changing methods should emit events

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-09-01-MuseumOfMahomes.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-09-01-MuseumOfMahomes.md)_

---

Currently most of the state-changing methods in the `MuseumOfMahomes` contract do not emit an event. An example is the `setPrice` method, which might be important for users or front-end/UI clients that wish to monitor and track the current price of the NFTs. Add proper event emissions in all state-changing methods.
