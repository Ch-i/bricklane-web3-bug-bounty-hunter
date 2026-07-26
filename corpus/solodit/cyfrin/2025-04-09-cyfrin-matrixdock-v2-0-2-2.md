---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-09-cyfrin-matrixdock-v2-0-2-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-04-09T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-09-cyfrin-matrixdock-v2-0
title: Cache amount and use Solady `SafeTransferLib::safeTransferETH` when refunding
  excess fee
vuln_class: []
---

# Cache amount and use Solady `SafeTransferLib::safeTransferETH` when refunding excess fee

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-09-cyfrin-matrixdock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md)_

---

**Description:** In `MTokenMessager::sendDataToChain` and `MTokenMessagerV2::sendDataToChain`, cache the amount and [use Solady](https://github.com/devdacian/solidity-gas-optimization?tab=readme-ov-file#10-use-safetransferlibsafetransfereth-instead-of-solidity-call-effective-035-cheaper) `SafeTransferLib::safeTransferETH` when refunding excess fee:
```diff
+ import {SafeTransferLib} from "@solady/utils/SafeTransferLib.sol";

-       if (msg.value - fee > 0) {
-           payable(msg.sender).sendValue(msg.value - fee);
-       }
+       uint256 excessFee = msg.value - fee;
+       if(excessFee > 0) {
+           SafeTransferLib.safeTransferETH(msg.sender, excessFee);
+       }
```

**Matrixdock:** Acknowledged.

\clearpage
