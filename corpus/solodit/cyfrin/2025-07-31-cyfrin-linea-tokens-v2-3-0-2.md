---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-31-cyfrin-linea-tokens-v2-3-0-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-31T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-31-cyfrin-linea-tokens-v2.3.md
tags:
- firm:cyfrin
- report:2025-07-31-cyfrin-linea-tokens-v2-3
title: Prevent accidental ownership and admin renouncement
vuln_class: []
---

# Prevent accidental ownership and admin renouncement

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-31-cyfrin-linea-tokens-v2.3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-31-cyfrin-linea-tokens-v2.3.md)_

---

**Description:** The inherited `renounceOwnership()` and `AccessControlUpgradeable`’s `renounceRole(DEFAULT_ADMIN_ROLE, msg.sender)` both allow the last authority to remove themselves, potentially leaving the contract permanently ownerless or admin‑less—blocking critical functions like `withdraw()` or role‑protected operations.

Consider override `renounceOwnership()` in `TokenAirdrop` to always revert, and similarly override `renounceRole` to prevent `DEFAULT_ADMIN_ROLE` from being renounced.

**Linea:** Fixed in [PR#19](https://github.com/Consensys/linea-tokens/pull/19), commits [`babc8ca`](https://github.com/Consensys/linea-tokens/pull/19/commits/babc8ca99fe0ee7b69e53cbc0b48a3e31b9778e6) and [`a302e77`](https://github.com/Consensys/linea-tokens/pull/19/commits/a302e77baee0061f4d44b9805c751aea5fcd9098)

**Cyfrin:** Verified. `renounceOwnership` overriden and reverts.
