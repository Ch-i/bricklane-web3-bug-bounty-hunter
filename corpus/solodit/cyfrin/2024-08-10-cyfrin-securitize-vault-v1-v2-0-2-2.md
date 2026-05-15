---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-10-cyfrin-securitize-vault-v1-v2-0-2-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-08-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-10-cyfrin-securitize-vault-v1-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-10-cyfrin-securitize-vault-v1-v2-0
title: Avoid emitting unnecessary events
vuln_class: []
---

# Avoid emitting unnecessary events

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-10-cyfrin-securitize-vault-v1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-10-cyfrin-securitize-vault-v1-v2.0.md)_

---

**Description:** The function `setLiquidationOpenToPublic` is used to set the state `liquidationOpenToPublic` and it is set to the provided parameter regardless of the current status. If the provided parameter is the same to the current value, a redundant event `LiquidationOpenToPublic` will be emitted.

**Securitize:** Fixed in [a2bae86](https://bitbucket.org/securitize_dev/bc-securitize-vault-sc/commits/a2bae865466a79c9a079a0957efa05ea0d6f68a6).

**Cyfrin:** Verified.
