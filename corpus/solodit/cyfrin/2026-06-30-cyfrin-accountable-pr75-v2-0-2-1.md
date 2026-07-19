---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`DepositGatewayFactory::createDepositGateway` is permissionless and registry-less,
  creating a poisoned-gateway social-engineering surface'
vuln_class: []
---

# `DepositGatewayFactory::createDepositGateway` is permissionless and registry-less, creating a poisoned-gateway social-engineering surface

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** `createDepositGateway(strategy_)` deploys a new `DepositGateway` bound to the caller-supplied `strategy_` and emits `DepositGatewayCreated(gateway, strategy_)` with no validation of `strategy_` at the factory layer and no registry of legitimate gateways. The deployed `DepositGateway` constructor backstops the obvious cases (it reverts on a zero or non-conforming strategy and rejects KYC vaults), and a gateway can only be activated when `AccountableYield::setDepositGateway` confirms `gateway.strategy() == address(this)` under `onlyManager`. So a gateway built around a garbage strategy can never be wired into the protocol path, and there is no direct on-chain fund-loss vector here. The residual concern is observational: because the factory is permissionless and emits the same `DepositGatewayCreated` event for any caller, an attacker can deploy a gateway bound to the *real* strategy address - which will pass the later `gateway.strategy() == this` check - and any off-chain tooling or operator that selects a gateway to wire by scanning `DepositGatewayCreated` events, rather than by their own deployment record, could be steered onto an attacker-deployed gateway. The on-chain wiring step is manager-gated and validated, so this is a social-engineering / operational-hygiene surface, not a contract bug.

**Recommended Mitigation:** Treat `createDepositGateway` output as untrusted: operators must wire only gateways they deployed and whose address they recorded out-of-band, never a gateway discovered by scanning `DepositGatewayCreated`. If on-chain provenance is desired, have the factory maintain a `mapping(address strategy => address[] gateways)` registry and/or restrict `createDepositGateway` to a known deployer role, so the event stream is not the trust anchor.

**Accountable:** Fixed in commit [`aea937c`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/aea937ccb0d39600236526c1dbcfe78fadbb3865)

**Cyfrin:** Verified.
