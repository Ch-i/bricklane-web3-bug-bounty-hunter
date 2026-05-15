---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-ethcf-swapboard-v2-0-2-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-ethcf-swapboard-v2-0
title: When sending ETH, use `SafeTransferLib::safeTransferETH` instead Of Solidity
  `call`
vuln_class: []
---

# When sending ETH, use `SafeTransferLib::safeTransferETH` instead Of Solidity `call`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-ethcf-swapboard-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md)_

---

**Description:** When sending ETH, use [SafeTransferLib::safeTransferETH](https://github.com/Vectorized/solady/blob/main/src/utils/SafeTransferLib.sol#L95-L103) instead Of Solidity `call` which is more [gas efficient](https://github.com/devdacian/solidity-gas-optimization?tab=readme-ov-file#10-use-safetransferlibsafetransfereth-instead-of-solidity-call-effective-035-cheaper):
```solidity
Swapboard.sol
205:        (bool success,) = payable(order.maker).call{value: order.amountA}("");
227:        (bool success,) = payable(msg.sender).call{value: order.amountA}("");
```

Another alternative "stand-alone" pattern which is also more efficient and prevents "return-bomb" style attacks is for example in `cancelOrderUnwrap`:
```solidity
-       (bool success,) = payable(maker).call{value: amountA}("");
+       bool success;
+       assembly {
+           success := call(gas(), maker, amountA, 0, 0, 0, 0)
+       }
        if (!success) revert ETHTransferFailed(maker);
```

**ETHCF:** Fixed in commit [3a9e06e](https://github.com/ETHCF/swapboard/commit/3a9e06eb2493b0c501b484c05e3d1033d7e56ba2) using the alternative "stand-alone" pattern.

**Cyfrin:** Verified.
