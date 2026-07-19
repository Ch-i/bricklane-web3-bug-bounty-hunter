---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-2-7
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: '`PublicBridge::lockTokens` allows zero-amount bridge operations when bridge
  fee is zero'
vuln_class: []
---

# `PublicBridge::lockTokens` allows zero-amount bridge operations when bridge fee is zero

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** When `bridgeFee == 0`, calling `lockTokens` with `amount = 0` succeeds because the fee check is skipped entirely:

```solidity
uint256 bridgeAmount = amount; // 0
if (bridgeFee > 0) { // false, skipped
    // ...
}
require(token.transferFrom(msg.sender, address(vault), bridgeAmount), "Transfer to vault failed");
// transferFrom with 0 amount succeeds on this Token
```

This emits a `TokensLocked` event with zero amount and increments `_nonce`, which could create misleading events for relayer nodes that monitor lock events.

**Recommended Mitigation:** Add a minimum amount check:

```solidity
require(amount > 0, "Amount required");
```

**BridgeX:**
Fixed in commit [a460520](https://github.com/NerdUnited-NodeGovernance/audit-2026-03-bridgex/commit/a4605205cabafdec3fd9f30147c87d1c4b4dd612).

**Cyfrin:** Verified.
