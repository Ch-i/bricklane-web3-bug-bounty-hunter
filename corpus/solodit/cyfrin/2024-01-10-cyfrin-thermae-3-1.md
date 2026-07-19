---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-10-cyfrin-thermae-3-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-01-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md
tags:
- firm:cyfrin
- report:2024-01-10-cyfrin-thermae
title: Move payable `receive()` function from `PorticoBase` into `PorticoFinish`
vuln_class: []
---

# Move payable `receive()` function from `PorticoBase` into `PorticoFinish`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-10-cyfrin-thermae.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md)_

---

**Description:** Move payable `receive()` function from `PorticoBase` into `PorticoFinish` since `PorticoFinish` is the only contract which needs to receive eth when it calls `WETH.withdraw()`.

`PorticoStart` which also inherits from `PorticoBase` never needs to receive eth apart from the payable `start` function, so does not need to have or inherit a payable `receive()` function.

**Wormhole:**
Fixed in commit 6208dd1.

**Cyfrin:** Verified.
