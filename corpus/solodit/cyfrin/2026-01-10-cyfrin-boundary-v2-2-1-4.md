---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-01-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md
tags:
- firm:cyfrin
- report:2026-01-10-cyfrin-boundary-v2-2
title: Residual permissions after benefactor removal
vuln_class: []
---

# Residual permissions after benefactor removal

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-10-cyfrin-boundary-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md)_

---

**Description:** When a benefactor is removed via `removeBenefactor`, previously configured beneficiaries and delegated signers for that benefactor are not cleared. If the same address is later re-added as a benefactor, all previously approved beneficiaries and delegates automatically become active again. This behavior may be unexpected, as removing a benefactor does not fully revoke prior trust relationships.

Consider clearing all beneficiaries and delegated signer data when a benefactor is removed, or explicitly document that removing a benefactor only disables mint/redeem temporarily and that prior approvals persist if the benefactor is re-added.

**Boundary:**
Resolved. Intentional design - benefactors manage their own configuration which persists independently of approval status. Documentation clarified in [PR#169](https://github.com/boundary-labs/boundary-protocol-ethereum/pull/169).

**Cyfrin:** Verified.
