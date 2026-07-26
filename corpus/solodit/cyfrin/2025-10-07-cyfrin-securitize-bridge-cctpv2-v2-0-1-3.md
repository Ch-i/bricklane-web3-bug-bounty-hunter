---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-1-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Inconsistent usage of `whenNotPaused` modifier for bridging fulfillment in
  `SecuritizeBridge` and `USDCBridgeV2`
vuln_class: []
---

# Inconsistent usage of `whenNotPaused` modifier for bridging fulfillment in `SecuritizeBridge` and `USDCBridgeV2`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** `USDCBridgeV2` inherits pause functionality from `BaseRBACContract`. Currently `USDCBridgeV2::receiveWormholeMessages` does not apply the `whenNotPaused` modifier allowing receipt of tokens to occur on a paused destination chain contract.

In contrast `SecuritizeBridge::receiveWormholeMessages` does have the `whenNotPaused` preventing receipt of tokens on a paused destination chain contract.

**Recommended Mitigation:** There is an inconsistent usage of `whenNotPaused` modifier for bridging fulfillment; if there is no good reason for this difference then it should be made consistent. Either:
* don't allow bridging fulfillment when destination contracts are paused
* allow bridging fulfillment when destination contracts are paused but don't allow new bridging requests when paused

**Securitize:** Acknowledged; for now we prefer to leave the modifiers unchanged. We can prevent issuances on flying bridges for dsTokens, as we control them and we can issue, burn, etc. We do not want to pause USDC flying bridges, as we do not have control over usdc circle stable coin.

\clearpage
