---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-1-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-12-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-19-cyfrin-lido-earn-v2-0
title: '`EmergencyVault::activateRecovery` NatSpec references wrong event name'
vuln_class: []
---

# `EmergencyVault::activateRecovery` NatSpec references wrong event name

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-19-cyfrin-lido-earn-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md)_

---

**Description:** The NatSpec for  `EmergencyVault::activateRecovery` states that it emits `RecoveryActivated`:
```solidity
*      Emits RecoveryActivated(actualBalance, totalSupply, protocolBalance, implicitLoss)
```
While it actually emits: `RecoveryModeActivated`
```solidity
emit RecoveryModeActivated(actualBalance, supply, protocolBalance, implicitLoss);
```
Consider changing the NatSpec to refer the correct event name.

**Lido:** Fixed in commit [`3d89267`](https://github.com/lidofinance/defi-interface/commit/3d89267ee409eb0857abb9302dcc42337429e4f9)

**Cyfrin:** Verified.
