---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-30-cyfrin-securitize-vault-registrarv2-v2-0-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-30-cyfrin-securitize-vault-registrarv2-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-30-cyfrin-securitize-vault-registrarv2-v2-0
title: '`VaultRegistrar::registerVault` uses `>=` for deadline check instead of `>`,
  deviating from EIP-2612 convention and design spec'
vuln_class: []
---

# `VaultRegistrar::registerVault` uses `>=` for deadline check instead of `>`, deviating from EIP-2612 convention and design spec

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-30-cyfrin-securitize-vault-registrarv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-30-cyfrin-securitize-vault-registrarv2-v2.0.md)_

---

**Description:** [`VaultRegistrar::registerVault`](https://github.com/securitize-io/bc-vault-registrar/blob/0867ad37a9f3479dc7c26d18e757fdb07d8620c5/VaultRegistrar/contracts/VaultRegistrar.sol#L83) checks `if (block.timestamp >= deadline)`, treating `block.timestamp == deadline` as expired. Both the EIP-2612 standard and OpenZeppelin's `ERC20Permit` use a strict `>` comparison. The project's own [design spec](https://github.com/securitize-io/bc-vault-registrar/blob/0867ad37a9f3479dc7c26d18e757fdb07d8620c5/VaultRegistrar/docs/phase1-design.md#L145) also specifies `if (block.timestamp > deadline)`.

**Impact:** The valid authorization window is one second shorter than intended. A transaction landing at exactly `block.timestamp == deadline` will revert unexpectedly. No funds at risk — only a failed transaction and minor operational inconvenience.

**Recommended Mitigation:**
```diff
- if (block.timestamp >= deadline) revert SignatureExpired();
+ if (block.timestamp > deadline) revert SignatureExpired();
```

**Securitize:** Fixed in commit [0cd08a3](https://github.com/securitize-io/bc-vault-registrar/commit/0cd08a3febe0f1905524306253ebb9715e69a9e6).

**Cyfrin:** Verified. Fixed by following the recommended mitigation.


\clearpage
