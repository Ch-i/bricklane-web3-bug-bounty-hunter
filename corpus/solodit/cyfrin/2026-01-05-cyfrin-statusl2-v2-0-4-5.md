---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-4-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: '`DeployProtocol.s.sol` doesn''t deploy RLN contracts'
vuln_class: []
---

# `DeployProtocol.s.sol` doesn't deploy RLN contracts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** `DeployProtocol.s.sol` is supposed to automatically deploy all contracts and configure them. However it forgets to invoke script `RLN.s.sol` which deploys contracts `RLN.sol` and `PoseidonHasher.sol`

**Recommended Mitigation:** Invoke the script `RLN.s.sol` and add contract `RLN.sol` as Slasher to Karma.

**StatusL2:** Acknowledged, the team stated that the contracts can be deployed separately.
