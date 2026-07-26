---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-2-8
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`DepositGateway` wraps vault `IAccess` reads in redundant `try/catch` guards
  that cannot fail for a valid vault'
vuln_class: []
---

# `DepositGateway` wraps vault `IAccess` reads in redundant `try/catch` guards that cannot fail for a valid vault

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** The gateway binds its `vault` once at construction (`immutable`) and the constructor already calls `IAccess(vault_).permissionLevel()` unwrapped (`src/modules/DepositGateway.sol:71`), so any deployed gateway is guaranteed to sit on a vault that implements `IAccess`. Yet three helpers still wrap their vault reads in `try/catch`: `_requireWhitelistIfConfigured` (`src/modules/DepositGateway.sol:319-335`), `_bothAllowed` (`src/modules/DepositGateway.sol:304-316`), and `_refundable` (`src/modules/DepositGateway.sol:291-296`). `permissionLevel` and `allowed` are plain storage and mapping getters; a `permissionLevel` call cannot fail against a valid vault, and `allowed` is a simple `mapping(address => bool)` lookup that likewise cannot revert, so every catch arm is unreachable code that only obscures the control flow.

The catch directions are also inconsistent: `_requireWhitelistIfConfigured`'s `permissionLevel` catch does a bare `return` (fail-open - silently skipping whitelist enforcement) while the `allowed` catches return `false` (fail-closed). None of this affects fund safety, since the vault's settle-time `onlyAuth` / `_areVerified` is the authoritative permission gate and these are only early-rejection checks, so it is a readability simplification with the bonus of removing the lone fail-open arm.

**Files:**

- `DepositGateway::_requireWhitelistIfConfigured` (`src/modules/DepositGateway.sol`)
- `DepositGateway::_bothAllowed` (`src/modules/DepositGateway.sol`)
- `DepositGateway::_refundable` (`src/modules/DepositGateway.sol`)

**Recommended Mitigation:** Call `permissionLevel` and `allowed` directly in all three helpers and drop the `try/catch` wrappers. A vault that cannot answer these getters is not a valid deployment target, so a clean revert is safer and simpler than silently skipping the check or special-casing it.

**Accountable:** FIxed in commit [`aea937c`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/aea937ccb0d39600236526c1dbcfe78fadbb3865)

**Cyfrin:** Verified.
