---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-01-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md
tags:
- firm:cyfrin
- report:2026-01-10-cyfrin-boundary-v2-2
title: Incorrect information in redeem-documentation
vuln_class: []
---

# Incorrect information in redeem-documentation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-10-cyfrin-boundary-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md)_

---

**Description:** Currently, the protocol documentation file `03-Fund-Flows` section `B.Redeeming` states that in order to execute `redeem`, `benefactor` must send USDB to the `USDBMinting` contract. However, this is not implemented in the code. The code calls the `USDB::burnFrom` function during the `redeem` process, which means that USDB must be held by the `benefactor`, but an `allowance` must be issued to the `USDBMinting` address.

**Boundary:**
Resolved. Documentation corrected in [PR#162](https://github.com/boundary-labs/boundary-protocol-ethereum/pull/162).

**Cyfrin:** Verified.
