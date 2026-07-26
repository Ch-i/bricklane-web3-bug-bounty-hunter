---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: Use low-level call to send ETH if return data is unimportant to avoid return
  bomb DoS and for gas efficiency
vuln_class: []
---

# Use low-level call to send ETH if return data is unimportant to avoid return bomb DoS and for gas efficiency

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** Use low-level call to send ETH if return data is unimportant, for example in `PublicBridge::payReleaseFee`:
```diff
-               (bool success, ) = payable(releasers[i]).call{value: feePerReleaser}("");
+               bool success;
+               address feeReceiver = releasers[i];

+               assembly {
+                   success := call(gas(), feeReceiver, feePerReleaser, 0, 0, 0, 0)
+               }
```

This avoids the "return-bomb" DoS attack and is also more gas efficient. All affected places:
```solidity
PublicBridge.sol
392:                (bool success, ) = payable(releasers[i]).call{value: feePerReleaser}("");
402:            (bool success, ) = payable(releasers[0]).call{value: remainingWei}("");
414:            (bool success, ) = payable(msg.sender).call{value: refundAmount}("");

PrivateChainBridge.sol
390:                (bool success, ) = payable(releasers[i]).call{value: feePerReleaser}("");
400:            (bool success, ) = payable(releasers[0]).call{value: remainingWei}("");
412:            (bool success, ) = payable(msg.sender).call{value: refundAmount}("");
```

**BridgeX:**
Fixed in commit [efb6843](https://github.com/NerdUnited-NodeGovernance/audit-2026-03-bridgex/commit/efb6843d02d675cb869aa916bcfceceae24a831b).

**Cyfrin:** Verified.
