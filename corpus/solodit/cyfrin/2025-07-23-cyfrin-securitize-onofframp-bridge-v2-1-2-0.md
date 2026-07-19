---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-2-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Bridge gas limit parameter lacks lower bound validation leading to potential
  failed deliveries
vuln_class: []
---

# Bridge gas limit parameter lacks lower bound validation leading to potential failed deliveries

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** The `updateGasLimit` function in the `USDCBridge` contract allows an admin to set the `gasLimit` parameter to any arbitrary value. This parameter is used when quoting and sending cross-chain USDC transfers, specifically as the gas limit for the execution of the `receivePayloadAndUSDC` function on the target chain. If the admin sets this value too low, the cross-chain message delivery will not have enough gas to complete execution on the destination chain.

**Impact:** If the `gasLimit` is set below the required threshold, all cross-chain deliveries initiated by the bridge will consistently fail due to out-of-gas errors during the `receivePayloadAndUSDC` execution. This would prevent users from successfully transferring USDC across chains using the bridge, effectively halting the bridge's core functionality. Funds may become stuck or require manual intervention to resolve failed deliveries.

**Recommended Mitigation:** Implement a minimum gas limit check in the `updateGasLimit` function to prevent the admin from setting the `gasLimit` below a safe operational threshold. This threshold should be determined based on the maximum expected gas usage of the `receivePayloadAndUSDC` function, with an additional safety margin. Optionally, emit an event or revert the transaction if an attempt is made to set the gas limit below this minimum value.

**Securitize:** Acknowledged.

**Cyfrin:** Acknowledged.
