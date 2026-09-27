---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-3-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-08-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-05-cyfrin-securitize-evm-async-vault-v2-0
title: '`AsyncFundVault::initialize` accepts non-contract NAV providers'
vuln_class: []
---

# `AsyncFundVault::initialize` accepts non-contract NAV providers

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** `AsyncFundVault::initialize` forwards `navProvider_` to the base initializer at `contracts/AsyncFundVault.sol:104-109`. That initializer rejects only the zero address before storing the provider at `contracts/base/AsyncFundVaultAdmin.sol:109-128`, so a nonzero externally owned account can be configured. `_checkNavPrice` subsequently invokes `navProvider.rate()` at `contracts/AsyncFundVault.sol:960-969`; the call to a codeless address returns empty returndata, and the ABI decoder reverts on the missing `uint256` return value before `live` can be assigned or the `live == 0` skip can be reached. Both settlement flows call this check before changing generation state at `contracts/AsyncFundVault.sol:438-445` and `contracts/AsyncFundVault.sol:633-640`, so the invalid configuration prevents deposit and redemption generations from being fulfilled.

**Impact:** A deployment-time provider-address error leaves submitted requests unfulfillable until an administrator deploys and executes a recovery upgrade that replaces the provider.

**Recommended Mitigation:** In `AsyncFundVaultAdmin::__AsyncFundVaultAdmin_init`, reject a `navProvider_` whose `code.length` is zero before assigning it. Also validate the dependency's expected response during initialization by requiring a successful `rate` call with a well-formed return value.

**Securitize:** Acknowledged.
