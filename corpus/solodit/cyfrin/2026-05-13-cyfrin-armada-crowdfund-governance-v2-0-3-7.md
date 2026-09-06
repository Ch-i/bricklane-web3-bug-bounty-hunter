---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-3-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: Token-side mapping add-only asymmetry
vuln_class: []
---

# Token-side mapping add-only asymmetry

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ArmadaToken::authorizedDelegator`, `noDelegation`, and `transferWhitelist` are add-only with no removal path. Governance shipping a misbehaving entry has no on-chain revoke.

**Impact:** Structural risk only - a buggy or malicious entry cannot be revoked once added.

**Recommended Mitigation:** Consider adding timelock-gated removal paths for each of these mappings.

**Armada:** Acknowledged.
