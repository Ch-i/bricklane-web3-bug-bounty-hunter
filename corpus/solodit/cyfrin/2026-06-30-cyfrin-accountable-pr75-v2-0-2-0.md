---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`DepositGateway::requestDeposit` omits the constructor''s KYC rejection on
  a later Whitelist-to-KYC flip'
vuln_class: []
---

# `DepositGateway::requestDeposit` omits the constructor's KYC rejection on a later Whitelist-to-KYC flip

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** The `DepositGateway` constructor (`src/modules/DepositGateway.sol:64-81`) reverts `SigAuthNotSupported` if the vault's `permissionLevel` is KYC at deploy time, because the gateway cannot supply the per-account EIP-712 signature a KYC vault requires. But `permissionLevel` is mutable on the vault. After a flip from Whitelist (or other) to KYC, `requestDeposit` (`src/modules/DepositGateway.sol:84-110`) keeps accepting escrow: its `_requireWhitelistIfConfigured` gate (`src/modules/DepositGateway.sol:319-335`) only enforces anything when the level is Whitelist and is a no-op for KYC. Settlement, however, is impossible - `IAccountableVault::deposit` under KYC needs a signature the gateway never carries. Open-epoch requests escrowed after the flip remain cancellable, but once their epoch passes they can never settle.

**Files:**

- `DepositGateway::requestDeposit` (`src/modules/DepositGateway.sol`)
- `DepositGateway::_requireWhitelistIfConfigured` (`src/modules/DepositGateway.sol`)

**Impact:** After a vault permission flip to KYC, the gateway continues to accept deposits it cannot ever settle. A request escrowed post-flip that reaches a Passed epoch is stuck against settlement; `_refundable` (`src/modules/DepositGateway.sol:280-302`) does return `true` on its KYC branch, so refund remains available as a recovery path, but the deposit flow itself is broken for that gateway from the moment of the flip. The trigger is an admin-driven permission change rather than an attacker; the impact is a silently broken deposit path that keeps accepting funds.

**Recommended Mitigation:** Mirror the constructor's KYC rejection at request time: have `requestDeposit` revert when the vault's current `permissionLevel` is KYC, so the gateway stops accepting escrow it cannot settle the instant the vault flips. This surfaces the misconfiguration to depositors immediately instead of accepting deposits into a dead-end settlement path.

**Accountable:** Fixed in commit [`aea937c`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/aea937ccb0d39600236526c1dbcfe78fadbb3865)

**Cyfrin:** Verified.
