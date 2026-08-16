---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-10-cyfrin-thermae-3-0
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
title: Missing sanity check for address validity in `PorticoBase::unpadAddress`
vuln_class: []
---

# Missing sanity check for address validity in `PorticoBase::unpadAddress`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-10-cyfrin-thermae.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md)_

---

**Description:** `PorticoBase::unpadAddress` is a re-implementation of [`Utils::fromWormholeFormat`](https://github.com/wormhole-foundation/wormhole-solidity-sdk/blob/main/src/Utils.sol#L10-L15) from the Wormhole Solidity SDK, but is missing a sanity check for address validity which is in the SDK implementation.

**Recommended Mitigation:** Consider adding the address validity sanity check to `PorticoBase::unpadAddress`.

**Wormhole:**
Fixed in commit 6208dd1.

**Cyfrin:** Verified.
