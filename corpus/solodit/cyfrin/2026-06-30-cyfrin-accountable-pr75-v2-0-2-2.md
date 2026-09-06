---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-2-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`AccountableYield::onMint` entry path is permanently dead once a deposit gateway
  is wired because the gateway only calls `vault.deposit`'
vuln_class: []
---

# `AccountableYield::onMint` entry path is permanently dead once a deposit gateway is wired because the gateway only calls `vault.deposit`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** PR75 adds `_requireFromGateway(controller)` to both `AccountableYield::onDeposit, onMint`, so once a deposit gateway is wired, every deposit/mint hook must originate from the wired gateway (a direct user is rejected with `DepositNotFromGateway`). `DepositGateway::settle` is the only path that drives escrowed requests into the vault, and it calls `IAccountableVault(vault).deposit(assets, req.user, address(this))` exclusively - it never calls a mint path. The consequence is that with a gateway set, `onMint` is unreachable for all actors: direct users are rejected by `_requireFromGateway`, and the gateway never invokes the mint route. The exact-shares (mint-by-shares) subscription entry that `onMint` implements therefore has no live caller and no replacement, so that entry mode is effectively removed for the gated configuration. This is a structural dead-path / capability-loss observation, not an exploit: no funds are at risk, but a reader expecting `onMint` to remain a usable entry will be surprised, and a future change that begins routing settlement through a mint path would re-activate code that currently receives no test coverage in the gated flow.

**Recommended Mitigation:** Decide whether mint-by-shares entry is intended to survive the gateway wiring. If it is not, document on `onMint` that the gated configuration disables it and consider removing or explicitly reverting the unused path to avoid future re-activation of untested code. If it is intended, give the gateway a settle variant that routes through the mint hook (mint-by-shares) so the exact-shares entry remains reachable, and cover it with tests.

**Accountable:** Fixed in commit [`aea937c`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/aea937ccb0d39600236526c1dbcfe78fadbb3865)

**Cyfrin:** Verified.
