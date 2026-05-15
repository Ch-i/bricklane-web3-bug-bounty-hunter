---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-18-cyfrin-securitize-solana-whitelister-v2-0-2-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-03-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-18-cyfrin-securitize-solana-whitelister-v2-0
title: Insufficient validation on vaults
vuln_class: []
---

# Insufficient validation on vaults

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md)_

---

**Description:** The Solana implementation lacks the validation checks present in the EVM `VaultRegistrar` designed to verify if a vault has already been registered. In the EVM version, before a vault wallet is added, the protocol queries if the vault is already associated with an identity. If it is linked to a different investor, it purposefully reverts with `VaultBelongsToDifferentInvestor`; if it is linked to the same investor, it reverts with `VaultAlreadyRegistered`.

Currently, the Solana contract calls `rwa_rbac::cpi::attach_wallet_to_identity` directly. Our Solana flow calls the CPI directly without this pre-check., which breaks parity with the EVM architecture and sacrifices granular error handling.

**Recommended Mitigation:** Implement proper checks just like its evm equivalent.

**Securitize:** Fixed in [8e3b5f8](https://github.com/securitize-io/bc-solana-whitelister/commit/8e3b5f8753b86afc984ad5620e1865ed2db63106).

**Cyfrin:** Verified.
