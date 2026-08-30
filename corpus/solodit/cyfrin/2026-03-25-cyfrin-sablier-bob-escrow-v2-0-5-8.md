---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-5-8
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Use `SafeTransferLib::safeTransferETH` instead of Solidity `call` to send ETH
  in `SablierBob::redeem`
vuln_class: []
---

# Use `SafeTransferLib::safeTransferETH` instead of Solidity `call` to send ETH in `SablierBob::redeem`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** Using [SafeTransferLib::safeTransferETH](https://github.com/Vectorized/solady/blob/main/src/utils/SafeTransferLib.sol#L95-L103) instead of Solidity `call` to send ETH in `SablierBob::redeem` is more [gas efficient](https://github.com/devdacian/solidity-gas-optimization?tab=readme-ov-file#10-use-safetransferlibsafetransfereth-instead-of-solidity-call-effective-035-cheaper).

Alternatively use a low-level pattern without introducing any new dependencies such as:
```diff
-        (bool success,) = address(_comptroller).call{ value: msg.value }("");
+        bool success;
+        assembly { success := call(gas(), _comptroller, msg.value, 0, 0, 0, 0) }
```

This low-level call pattern also avoids return-bomb attacks but that isn't an issue here.

**Sabler:**
Acknowledged.
