---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-2-6
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
title: '`DepositGatewayFactory::createDepositGateway` has a dead `gateway == address(0)`
  check after `new`'
vuln_class: []
---

# `DepositGatewayFactory::createDepositGateway` has a dead `gateway == address(0)` check after `new`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** `DepositGatewayFactory::createDepositGateway` checks `if (gateway == address(0)) revert FailedDeployment(...)` immediately after `gateway = address(new DepositGateway(...))`. The `new` operator reverts the whole transaction if creation fails (out-of-gas, constructor revert, etc.) - it can never return `address(0)`. The branch is unreachable dead code; the `FailedDeployment` error and its string argument can never fire from this site.

```solidity
factory/DepositGatewayFactory.sol
18:        gateway = address(new DepositGateway(strategy_));
19:        if (gateway == address(0)) revert FailedDeployment("zero gateway address");
```

**Recommended Mitigation:** Remove the unreachable check, and remove the `FailedDeployment` import if it is no longer used. Note that the sibling V1 factories use the same dead pattern against `new`-created addresses; those are out of scope here but share the root cause.

**Accountable:** Fixed in commit [`aea937c`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/aea937ccb0d39600236526c1dbcfe78fadbb3865)

**Cyfrin:** Verified.
