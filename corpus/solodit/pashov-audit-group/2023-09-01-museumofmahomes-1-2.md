---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-09-01-museumofmahomes-1-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-09-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-09-01-MuseumOfMahomes.md
tags:
- firm:pashov-audit-group
- report:2023-09-01-museumofmahomes
title: '[L-03] A `treasury` account can mint all NFTs'
vuln_class: []
---

# [L-03] A `treasury` account can mint all NFTs

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-09-01-MuseumOfMahomes.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-09-01-MuseumOfMahomes.md)_

---

Currently an account that is in the `treasury` mapping can mint all NFTs for free. While it is desired that such an account does not pay for minting a token, consider adding a `MAX_TREASURY_MINTS` upper bound to limit the count of NFTs minted by `treasury` accounts. You can also make sure that when a `treasury` account is minting, the `msg.value` is 0.
