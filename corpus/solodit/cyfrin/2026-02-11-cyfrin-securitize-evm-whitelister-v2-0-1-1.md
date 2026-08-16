---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-11-cyfrin-securitize-evm-whitelister-v2-0-1-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-02-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-11-cyfrin-securitize-evm-whitelister-v2-0
title: '`Whitelister::whitelist` duplicates checks already performed in `RegistryService::addWallet`'
vuln_class: []
---

# `Whitelister::whitelist` duplicates checks already performed in `RegistryService::addWallet`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md)_

---

**Description:** `Whitelister::whitelist`  checks that the investor has a valid investor id, and that the given `vaultAddress` is not already a registered wallet.

However the function it calls `RegistryService::addWallet` already [performs](https://github.com/securitize-io/bc-vault-whitelister/blob/main/3-dstoken-reference/contracts/registry/RegistryService.sol#L163) these checks via the modifiers `investorExists(_id) newWallet(_address)`.

**Recommended Mitigation:** The modifier checks return the older-style text message errors while the new checks return typed errors. If the textual errors are sufficient, consider removing the duplicate checks. Otherwise if the typed errors are desired the existing code can be kept, it will just have slightly higher gas costs.

**Securitize:** Acknowledged; the duplicate checks are intentional and were kept for readability and explicitness at the call site.

\clearpage
