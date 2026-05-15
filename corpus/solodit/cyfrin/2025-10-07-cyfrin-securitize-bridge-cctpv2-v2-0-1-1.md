---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-1-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: No way to retrieve ETH sent with call to `SecuritizeBridge::receiveWormholeMessages`
vuln_class: []
---

# No way to retrieve ETH sent with call to `SecuritizeBridge::receiveWormholeMessages`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** `SecuritizeBridge::receiveWormholeMessages` is marked as `payable` however:
* it does nothing with `msg.value`
* there is no function in `SecuritizeBridge` to withdraw ETH

**Impact:** If ETH should be sent along with the call to `SecuritizeBridge::receiveWormholeMessages`, it will be stuck in the contract unable to be retrieved.

**Recommended Mitigation:** Add a function `withdrawETH` that allows the contract owner to withdraw the contract's ETH balance.

**Securitize:** Fixed in commits [923e50e](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/923e50e41dc859fa9516dd370988d01d685759e6), [2b18646](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/2b18646e6344fcebe4f32107cd56812877ddadea#diff-3f58493270011157ff7c863627332c733405a46f8b6524660d25b33ef16f9f74R171) by adding a `withdrawETH` function the owner can call.

**Cyfrin:** Verified.
