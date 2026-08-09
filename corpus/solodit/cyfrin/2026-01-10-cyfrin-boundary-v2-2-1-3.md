---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-3
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
title: Smart-account benefactors cannot use ERC-1271 signature validation and delegated
  signers at the same time
vuln_class: []
---

# Smart-account benefactors cannot use ERC-1271 signature validation and delegated signers at the same time

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-10-cyfrin-boundary-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md)_

---

**Description:** In `USBDMinting::_verifySignature`, a smart-account benefactor cannot use its own ERC-1271 signature logic and delegated signers simultaneously. As soon as any delegate is added to `_delegatesPerBenefactor[benefactor]`, signature verification for that benefactor switches to the ECDSA path and ERC-1271 validation is no longer used. This makes ERC-1271–based validation mutually exclusive with delegated signing for smart-account benefactors.

Consider allowing smart-account benefactors to keep ERC-1271 validation active even when delegates exist, or explicitly document this limitation as an intentional design constraint.


**Boundary:**
Resolved. Intentional - contract benefactors choose one signature mode. Documentation clarified in [PR#167](https://github.com/boundary-labs/boundary-protocol-ethereum/pull/167).

**Cyfrin:** Verified.
