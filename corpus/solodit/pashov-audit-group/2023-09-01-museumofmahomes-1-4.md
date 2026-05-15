---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-09-01-museumofmahomes-1-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-09-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-09-01-MuseumOfMahomes.md
tags:
- firm:pashov-audit-group
- report:2023-09-01-museumofmahomes
title: '[L-05] Use a two-step access control transfer pattern'
vuln_class: []
---

# [L-05] Use a two-step access control transfer pattern

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-09-01-MuseumOfMahomes.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-09-01-MuseumOfMahomes.md)_

---

The `MuseumOfMahomes` contract uses a single-step access control transfer pattern in `setOwner` and `setMetadataOwner`. This means that if the current `owner` or `metadataOwner` accounts call the methods with an incorrect address, then those roles will be lost forever along with all the functionality that depends on them. Follow the pattern from OpenZeppelin's [Ownable2Step](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable2Step.sol) and implement a two-step transfer pattern for the actions.
