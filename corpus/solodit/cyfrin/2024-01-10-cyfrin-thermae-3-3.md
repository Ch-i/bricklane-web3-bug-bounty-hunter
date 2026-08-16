---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-10-cyfrin-thermae-3-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-01-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md
tags:
- firm:cyfrin
- report:2024-01-10-cyfrin-thermae
title: '`TokenBridge::isDeployed` could be declared pure'
vuln_class: []
---

# `TokenBridge::isDeployed` could be declared pure

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-10-cyfrin-thermae.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md)_

---

**Description:** `TokenBridge::isDeployed` could be declared pure. Also not sure what the point of this contract is; if it is used for testing perhaps move it into a `mocks` directory.

**Wormhole:**
Removed this contract.

**Cyfrin:** Verified.
