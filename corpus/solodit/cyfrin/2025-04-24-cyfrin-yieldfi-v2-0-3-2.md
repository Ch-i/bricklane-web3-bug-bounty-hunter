---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-3-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: '`_receiverGas` check excludes minimum acceptable value'
vuln_class: []
---

# `_receiverGas` check excludes minimum acceptable value

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** In the LayerZero bridge contracts [`BridgeLR::send`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/BridgeLR.sol#L76) and [`BridgeMB::send`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/BridgeMB.sol#L66), there's a check to ensure the user has provided sufficient `_receiverGas`:

```solidity
require(_receiverGas > MIN_RECEIVER_GAS, "!gas");
```

The variable name `MIN_RECEIVER_GAS` suggests that the specified amount should be *inclusive*, meaning the minimum acceptable value is valid. However, the current `>` check excludes `MIN_RECEIVER_GAS` itself. To align with the semantic expectation, consider changing the comparison to `>=`:

```diff
- require(_receiverGas > MIN_RECEIVER_GAS, "!gas");
+ require(_receiverGas >= MIN_RECEIVER_GAS, "!gas");
```

Same applies to the call [`Bridge::setMIN_RECEIVER_GAS`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/Bridge.sol#L53) and the check in [`Bridge::quote`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/Bridge.sol#L85) as well.

**YieldFi:** Fixed in commit [`9aa242b`](https://github.com/YieldFiLabs/contracts/commit/9aa242b7351314fe07160e98699d8da14a1b9bc2)

**Cyfrin:** Verified.
