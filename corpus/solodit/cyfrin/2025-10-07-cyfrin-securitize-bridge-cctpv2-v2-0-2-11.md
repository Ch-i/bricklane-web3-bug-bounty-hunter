---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-2-11
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: '`USDCBridgeV2` can''t bridge to non-EVM chains even though Wormhole and Circle
  CCTP support this'
vuln_class: []
---

# `USDCBridgeV2` can't bridge to non-EVM chains even though Wormhole and Circle CCTP support this

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** Both Wormhole and Circle CCTP support bridging between EVM and non-EVM chains, however `USCBridgeV2` prevents bridging to non-EVM chains since:

1) `_sendUSDCWithPayloadToEvm` always calls `wormholeRelayer.sendToEvm`
2) `bridgeAddresses[_targetChain]` stores the target bridges using `address`, but this is not compatible with target bridges on non-EVM chains such as Solana

**Impact:** Bridging to non-EVM chains is not supported.

**Recommended Mitigation:** If bridging to non-EVM chains should be supported:
* use `wormholeRelayer.send` instead of `sendToEvm`
* `bridgeAddresses[_targetChain]` should store target bridges as `bytes32` then cast them to `address` when bridging to EVM chains
* generally addresses for remote chains should be passed as input, stored and used using `bytes32` not `address`

**Securitize:** Acknowledged; by design for now.
